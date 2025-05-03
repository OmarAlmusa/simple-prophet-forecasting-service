from pydantic import BaseModel
import pandas as pd
import datetime
import logging

from fastapi import FastAPI
# from registry.mlflow.handler import MLFlowHandler

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
    if begin_date == None:
        begin_date = datetime.datetime.now().replace(tzinfo=None)
    else:
        begin_date = datetime.datetime.strptime(
            begin_date,
            '%Y-%m-%dT%H:%M:%SZ'
        ).replace(tzinfo=None)

    if end_date == None:
        end_date == begin_date + datetime.timedelta(days=7)
    else:
        end_date = datetime.datetime.strptime(
            end_date,
            '%Y-%m-%dT%H:%M:%SZ'
        ).replace(tzinfo=None)

    return pd.date_range(start= begin_date, end = end_date, freq='D')