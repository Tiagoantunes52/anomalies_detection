from fastapi.testclient import TestClient

from main import app


# Define a test client
client = TestClient(app)


def test_get_anomalies_report_isolation_forest():
    response = client.get("/api/v1/anomalies_report_isolation_forest")

    # Asserting response status code is 200
    assert response.status_code == 200

    response_data = response.json()

    # Asserting response contains the expected key
    assert "anomalies" in response_data

    # From exploratory data analysis there are 20 expected outliers
    assert len(response_data["anomalies"]) == 20


def test_get_anomalies_report_dbscan():
    response = client.get("/api/v1/anomalies_report_dbscan")

    # Asserting response status code is 200
    assert response.status_code == 200

    response_data = response.json()

    # Asserting response contains the expected key
    assert "anomalies" in response_data

    # From exploratory data analysis there are 20 expected outliers
    assert len(response_data["anomalies"]) == 20
