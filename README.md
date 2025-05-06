<h1>Prophet Forecasting Service (Kubernetes Deployment)</h1>

<p>
This project builds and deploys a scalable forecasting service using Facebook Prophet, orchestrated with Ray, tracked with MLflow, served via FastAPI, and deployed on Kubernetes.

This project was done with the help of the chapter 8 of the book "Python Machine Learning Engineering with Python 2nd Edition" Authored by Andrew P. McMahon.
</p>



<h2>✅ What’s Inside</h2>

<ui>
    <li>Distributed training with Ray across all store IDs from the Rossmann dataset</li>
    <li>MLflow tracking + model registry for managing Prophet models</li>
    <li>FastAPI service to serve forecasts on demand using production-registered models</li>
    <li>Dockerized setup with Kubernetes deployment</li>
    <li>Supports dynamic model loading via model name and store ID</li>
    <li>Connects to locally hosted MLflow server from inside K8s</li>
</ui>



<h2>🧱 Stack</h2>

<ul>
    <li>Python 3.10</li>
    <li>Ray for distributed orchestration</li>
    <li>FastAPI for serving predictions</li>
    <li>MLflow for experiment tracking and model registry</li>
    <li>Docker for containerizing the application</li>
    <li>Kubernetes (kubectl + Docker Desktop or Minikube)</li>
    <li>Prophet for time-series forecasting</li>
</ul>



<h2>🛠️ What was done</h2>

<ol>
    <li>
        <p>Data processing & training orchestration with Ray:</p>
        <ul>
            <li>
                Loaded Rossmann store sales dataset
            </li>
            <li>
                Used Ray to parallelize Prophet training per store
            </li>
            <li>
                Each store’s model was trained, predicted, and returned as a Ray object
            </li>
        </ul>
    </li>
    <li>
        <p>Logged & versioned models with MLflow:</p>
        <ul>
            <li>
                Registered each store-specific Prophet model
            </li>
            <li>
                Automatically promoted models to "Production" stage via MLflow’s Model Registry API
            </li>
        </ul>
    </li>
    <li>
        <p>Built a FastAPI microservice:</p>
        <ul>
            <li>
                Reads model from MLflow by store ID
            </li>
            <li>
                Supports prediction via a simple /forecast/ endpoint
            </li>
        </ul>
    </li>
    <li>
        <p>Containerized the service:</p>
        <ul>
            <li>
                Dockerized with clean environment setup
            </li>
            <li>
                Used host.docker.internal trick to access local MLflow from inside the container
            </li>
        </ul>
    </li>
    <li>
        <p>Deployed with Kubernetes:</p>
        <ul>
            <li>
                Created a direct-kube-deploy.yaml to run multiple FastAPI replicas
            </li>
            <li>
                Exposed service using minikube tunnel
            </li>
            <li>
                Tuned pod resources to avoid overkill or OOMs
            </li>
            <li>
                Managed pods using force-deletion or selective cleanup
            </li>
        </ul>
    </li>
</ol>
