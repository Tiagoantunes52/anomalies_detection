import pandas as pd
import logging
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import GridSearchCV
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from app.schemas.anomalies import AnomaliesReportOutSchema


logger = logging.getLogger(__name__)


def anomalies_report_isolation_forest() -> AnomaliesReportOutSchema:
    """
    Detect anomalies in a transactions dataset using Isolation Forest.

    Returns:
    - AnomaliesReportOutSchema: An object containing a list of Anomaly objects,
      each representing a detected anomaly.
    """

    df = pd.read_csv("app/datasets/transactions_dataset.csv")

    # Adjusting contamination based on expected anomaly rate
    # Value chosen based on visualization of data
    contamination = 0.02
    # Initializing the Isolation Forest model
    model = IsolationForest(contamination=contamination)
    logger.info(
        f"Initialized Isolation Forest model with contamination = {contamination}"
    )

    # Train the model
    model.fit(df[["Transaction_Amount"]])

    # Get anomaly scores for each transaction
    df["anomaly_score"] = model.decision_function(df[["Transaction_Amount"]])
    # Outliers will be marked as -1
    df["anomaly"] = model.predict(df[["Transaction_Amount"]])

    anomalies = df[df["anomaly"] == -1]

    # Building output structure of anomalies
    anomalies_report = anomalies_builder(anomalies)

    logger.info(f"Anomalies detected using Isolation Forest: {anomalies_report}")

    return AnomaliesReportOutSchema(**anomalies_report)


def anomalies_report_dbscan() -> AnomaliesReportOutSchema:
    """
    Detect anomalies in a transactions dataset using DBSCAN (Density-Based Spatial Clustering of Applications with Noise).

    Returns:
    - AnomaliesReportOutSchema: An object containing a list of Anomaly objects, each representing a detected anomaly.
    """

    df = pd.read_csv("app/datasets/transactions_dataset.csv")

    # Standardize the Transaction_Amount feature, might improve model performance
    scaler = StandardScaler()
    df["Transaction_Amount_scaled"] = scaler.fit_transform(df[["Transaction_Amount"]])

    # Parameter grid for grid search
    # eps: distance between points to define a neighborhood
    # min_samples: minimum number of points required to form a dense region
    param_grid = {"eps": [0.3, 0.5, 1.0], "min_samples": [10, 15, 20]}

    # Initializing the DBSCAN model
    model = DBSCAN()
    logger.info(f"Initialized DBSCAN model")

    # Initializing the GridSearchCV
    # neg_mean_squared_error scoring function seems to work well for this particular case
    scoring_fucntion = "neg_mean_squared_error"
    grid_search = GridSearchCV(model, param_grid, scoring=scoring_fucntion, cv=5)
    logger.info(f"Grid search started with {scoring_fucntion}")

    # Fit the grid search to the data
    grid_search.fit(df[["Transaction_Amount_scaled"]])
    logger.info(f"Best params: {grid_search.best_params_}")

    # Access the best model
    best_model = grid_search.best_estimator_

    # Fitting the model
    df["cluster"] = best_model.fit_predict(df[["Transaction_Amount_scaled"]])

    # Getting anomalies from the cluster, -1 refers to outliers
    anomalies = df[df["cluster"] == -1]

    # Building output structure of anomalies
    anomalies_report = anomalies_builder(anomalies)

    logger.info(f"Anomalies detected using DBSCAN: {anomalies_report}")

    return AnomaliesReportOutSchema(**anomalies_report)


def anomalies_builder(anomalies: pd.DataFrame) -> dict:
    # converting the DataFrame directly into a list of dictionaries
    anomalies_report = {"anomalies": anomalies.to_dict(orient="records")}
    return anomalies_report
