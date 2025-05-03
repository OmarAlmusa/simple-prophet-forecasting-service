import logging
from contextlib import asynccontextmanager
from pydantic import BaseModel
import pandas as pd
import datetime
from typing import List

from fastapi import FastAPI
from registry.mlflow.handler import MLFlowHandler



log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format = log_format, level=logging.INFO)

handlers = {}
models = {}
MODEL_BASE_NAME = f"prophet-retail-forecaster-store-"


class ForecastRequest(BaseModel):
    store_id: str
    begin_date: str | None = None
    end_date: str | None = None


def create_forecast_index(begin_date: str = None, end_date: str = None):
    if begin_date is None:
        begin_date = datetime.datetime.now().replace(tzinfo=None)
    else:
        begin_date = datetime.datetime.strptime(
            begin_date,
            '%Y-%m-%dT%H:%M:%SZ'
        ).replace(tzinfo=None)

    if end_date is None:
        end_date = begin_date + datetime.timedelta(days=7)
    else:
        end_date = datetime.datetime.strptime(
            end_date,
            '%Y-%m-%dT%H:%M:%SZ'
        ).replace(tzinfo=None)

    return pd.date_range(start=begin_date, end=end_date, freq='D')


async def get_service_handlers():
    mlflow_handler = MLFlowHandler()
    global handlers
    handlers['mlflow'] = mlflow_handler
    logging.info("Retrieving mlflow handler {}".format(mlflow_handler))
    return handlers


async def get_model(store_id: str):
    global handlers
    global models
    model_name = MODEL_BASE_NAME + f"{store_id}"
    if model_name not in models:
        models[model_name] = handlers['mlflow'].get_production_model(store_id=store_id)

    return models[model_name]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await get_service_handlers()
    logging.info("Updated global service handlers")
    yield
    # Clean up the ML models and release the resources

app = FastAPI(lifespan=lifespan)

@app.get("/health/", status_code=200)
async def healthcheck():
    global handlers
    logging.info("Got handlers in healthcheck.")
    return {
        "serviceStatus": "OK",
        "modelTrackingHealth": handlers["mlflow"].check_mlflow_health()
    }


@app.post("/forecast/", status_code=200)
async def return_forecast(forecast_request: List[ForecastRequest]):
    forecasts = []
    
    for item in forecast_request:
        model = await get_model(item.store_id)
        forecast_input = create_forecast_index(
            begin_date=item.begin_date,
            end_date=item.end_date
        )
        forecast_result = {}
        forecast_result['request'] = item.model_dump()

        # if not isinstance(forecast_input, pd.DataFrame):
        #     forecast_input = pd.DataFrame({'ds': forecast_input})

        # if 'ds' not in forecast_input.columns:
        #     raise ValueError("Missing 'ds' column in input data")

        forecast_input = pd.DataFrame({'ds': forecast_input})

        forecast_input['ds'] = pd.to_datetime(forecast_input['ds'], errors='coerce')

        print("Forecast input:")
        print(forecast_input)
        print(type(forecast_input))

        model_prediction = model.predict(forecast_input)[['ds', 'yhat']]\
            .rename(columns={'ds': 'timestamp', 'yhat': 'value'})
        model_prediction['value'] = model_prediction['value'].astype(int)
        forecast_result['forecast'] = model_prediction.to_dict('records')
        forecasts.append(forecast_result)

    return forecasts