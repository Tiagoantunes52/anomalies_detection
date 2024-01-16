# Anomalies Detection project

Minimal REST API built with FastAPI framework to detect anomalies in financial transactions.

## Setup
In order to setup this application you'll need docker and docker-compose plugin installed on your local machine.
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose plugin](https://docs.docker.com/compose/install/linux/#install-using-the-repository)


To build and start the container simply run:

```bash
docker-compose up -d --build
```

After the container is up and running the documentation is accessible via http://localhost:5050/docs



## How to use

There are two GET endpoints provided for fetching the anomalies with diferent implementations, both are acessible and testable via the documentation page http://localhost:5050/docs or via curl request.


* Isolation Forest (unsupervised learning algorithm used for anomaly detection)
  * /api/v1/anomalies_report_isolation_forest
    

* DBSCAN (Density-Based Spatial Clustering of Applications with Noise is a clustering algorithm used for data analysis and pattern recognition)
  * /api/v1/anomalies_report_dbscan
  