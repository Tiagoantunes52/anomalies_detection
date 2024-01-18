# Anomalies Detection project

Minimal REST API built with FastAPI framework to detect anomalies in financial transactions.
The implemented endpoints will return a list of anomalies.

## Setup
In order to setup this application you'll need docker and docker-compose plugin installed on your local machine.
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose plugin](https://docs.docker.com/compose/install/linux/#install-using-the-repository)


To build and start the container simply run:

```bash
sudo docker-compose up -d --build
```

After the container is up and running the documentation is accessible via http://localhost:5050/docs



## How to use

There are two GET endpoints provided for fetching the anomalies with diferent implementations, both are acessible and testable via the documentation page http://localhost:5050/docs or via curl request.

* DBSCAN (Density-Based Spatial Clustering of Applications with Noise is a clustering algorithm used for data analysis and pattern recognition)
  * /api/v1/anomalies_report_dbscan
  ```bash
  curl -X 'GET' \
  'http://localhost:5050/api/v1/anomalies_report_dbscan' \
  -H 'accept: application/json'
  ```


* Isolation Forest (unsupervised learning algorithm used for anomaly detection)
  * /api/v1/anomalies_report_isolation_forest
  ```bash
  curl -X 'GET' \
  'http://localhost:5050/api/v1/anomalies_report_isolation_forest' \
  -H 'accept: application/json'
  ```

## Exploratory data analysis
To ascertain the anticipated result of model predictions, exploratory data analysis was employed to pinpoint outliers within the dataset. Using Jupyter notebooks, a data distribution was visualized, based on the "Transaction_Amount" column, revealing a distinct cluster of points noticeably segregated from the overwhelming majority of data points. While most data points converge around 1000, another group of data points can be detected at around 3000. The jupyter notebook can be found in the exploratory_data_analysis folder.

## Tests
Some minimal unit tests, using pytest, have been included to test the api funtionality.

First check your container name:
```bash
sudo docker ps
```

Access a bash terminal inside the container:
```bash
sudo docker exec -it <YOUR-CONTIANER-NAME> bash
```

Then run the following command to run the tests:
```bash
pytest -p no:warnings
```
