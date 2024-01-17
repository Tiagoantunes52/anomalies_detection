import logging
from fastapi import APIRouter
from starlette.responses import JSONResponse

import app.api.anomalies as anomalies
from app.schemas.anomalies import AnomaliesReportOutSchema


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/api/v1/anomalies_report_isolation_forest", response_model=AnomaliesReportOutSchema
)
def get_anomalies_report():
    try:
        anomalies_report = anomalies.anomalies_report_isolation_forest()
        return anomalies_report
    except Exception as exc:
        logger.error(exc.args, exc_info=True)
        return JSONResponse(
            content={"status": "error", "error": "Internal Server Error"},
            status_code=500,
        )


@router.get("/api/v1/anomalies_report_dbscan", response_model=AnomaliesReportOutSchema)
def get_anomalies_report():
    try:
        anomalies_report = anomalies.anomalies_report_dbscan()
        return anomalies_report
    except Exception as exc:
        logger.error(exc.args, exc_info=True)
        return JSONResponse(
            content={"status": "error", "error": "Internal Server Error"},
            status_code=500,
        )
