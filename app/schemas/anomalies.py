from pydantic import BaseModel
from typing import Union, List


class Anomaly(BaseModel):
    Transaction_ID: str
    Date: str
    Transaction_Amount: float
    Country: str


class AnomaliesReportOutSchema(BaseModel):
    anomalies: List[Anomaly]
