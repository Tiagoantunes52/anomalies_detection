from pydantic import BaseModel
from typing import List


class Anomaly(BaseModel):
    """
    Represents an anomaly in the transaction dataset.

    Attributes:
    - Transaction_ID (str): Identifier for the transaction.
    - Date (str): Date of the transaction.
    - Transaction_Amount (float): Amount of the transaction.
    - Country (str): Country where the transaction occurred.
    """

    Transaction_ID: str
    Date: str
    Transaction_Amount: float
    Country: str


class AnomaliesReportOutSchema(BaseModel):
    """
    Represents the output schema for a report containing anomalies.

    Attributes:
    - anomalies (List[Anomaly]): A list of Anomaly objects representing detected anomalies.
    """

    anomalies: List[Anomaly]
