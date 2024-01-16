import pandas as pd
import logging
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.model_selection import GridSearchCV
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from fastapi import HTTPException

from app.schemas.anomalies import AnomaliesReportOutSchema


logger = logging.getLogger(__name__)


def anomalies_report_isolation_forest() -> AnomaliesReportOutSchema:
    """
    Detect anomalies in a transactions dataset using Isolation Forest.

    Returns:
    - anomalies_report: An object containing a list of dictionaries, each representing an anomaly.
    """

    df = pd.read_csv("app/datasets/transactions_dataset.csv")

    contamination = 0.05
    # Initializing the Isolation Forest model
    model = IsolationForest(
        contamination=contamination
    )  # Adjusting contamination based on expected anomaly rate
    logger.info(
        f"Initialized Isolation Forest model with contamination = {contamination}"
    )

    # Train the model
    model.fit(df[["Transaction_Amount"]])

    # Get anomaly scores for each transaction
    df["anomaly_score"] = model.decision_function(df[["Transaction_Amount"]])

    # Value chosen based on visualization of data
    threshold = -0.17

    # Identify anomalies based on the threshold
    anomalies = df[df["anomaly_score"] < threshold]

    # Building output structure of anomalies
    anomalies_report = anomalies_builder(anomalies)

    logger.info("Anomalies detected using Isolation Forest: {anomalies_report}")

    return anomalies_report


# def anomalies_report_one_class_SVM() -> AnomaliesReportOutSchema:
#     df = pd.read_csv("app/datasets/transactions_dataset.csv")
#     # Standardize the Transaction_Amount feature
#     scaler = StandardScaler()
#     df[["Transaction_Amount_scaler"]] = scaler.fit_transform(df[["Transaction_Amount"]])

#     # Define the parameter grid for grid search
#     param_grid = {"nu": [0.01, 0.05, 0.1, 0.2, 0.5]}

#     # Initialize the OneClassSVM model
#     model = OneClassSVM()

#     # Initialize the GridSearchCV
#     grid_search = GridSearchCV(
#         model, param_grid, cv=5, scoring="accuracy"
#     )  # Adjust scoring based on your evaluation metric

#     # Fit the grid search to the data
#     grid_search.fit(df[["Transaction_Amount_scaler"]])

#     # Get the best parameters from the grid search
#     best_params = grid_search.best_params_

#     # Print the best parameters
#     print("Best Parameters:", best_params)

#     # Access the best model
#     best_model = grid_search.best_estimator_

#     # Get anomaly scores using the decision_function
#     df["anomaly_score"] = best_model.decision_function(
#         df[["Transaction_Amount_scaler"]]
#     )

#     # Set a threshold manually based on the anomaly scores
#     threshold = -0.02  # Adjust based on your analysis

#     # Select anomalies based on the threshold
#     anomalies = df[df["anomaly_score"] < threshold]

#     anomalies_report = anomalies_builder(anomalies)


#     return anomalies_report


def anomalies_report_dbscan() -> AnomaliesReportOutSchema:
    """
    Detect anomalies in a transactions dataset using DBSCAN (Density-Based Spatial Clustering of Applications with Noise).

    Returns:
    - anomalies_report: An object containing a list of dictionaries, each representing an anomaly.
    """

    df = pd.read_csv("app/datasets/transactions_dataset.csv")

    # Standardize the Transaction_Amount feature, might improve model performance
    scaler = StandardScaler()
    df["Transaction_Amount_scaled"] = scaler.fit_transform(df[["Transaction_Amount"]])

    # Parameter grid for grid search
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

    logger.info("Anomalies detected using DBSCAN: {anomalies_report}")

    return anomalies_report


def anomalies_builder(anomalies: pd.DataFrame) -> dict:
    anomalies_report = {"anomalies": []}

    for _, row in anomalies.iterrows():
        anomaly_dict = {
            "Transaction_ID": row["Transaction_ID"],
            "Date": row["Date"],
            "Transaction_Amount": row["Transaction_Amount"],
            "Country": row["Country"],
        }
        anomalies_report["anomalies"].append(anomaly_dict)
    return anomalies_report
