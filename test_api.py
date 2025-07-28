from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

def test_empty_code():
    res = client.post("/find-bug", json={"language": "python", "code": ""})
    assert res.status_code == 400

@patch("bdetect.get_bug_report")
def test_valid_code(mock_get_bug_report):
    mock_get_bug_report.return_value = {
        "bug_type": "Logical Bug",
        "description": "Returns True for odd numbers instead of even.",
        "suggestion": "Use n % 2 == 0 instead."
    }

    res = client.post("/find-bug", json={
        "language": "python",
        "code": "def is_even(n): return n % 2 == 1"
    })

    assert res.status_code == 200
    data = res.json()
    assert data["bug_type"] == "Logical Bug"
    assert "description" in data
    assert "suggestion" in data

def test_sample_cases():
    res = client.get("/sample-cases")
    assert res.status_code == 200
    cases = res.json()
    assert isinstance(cases, list)
    assert len(cases) >= 3
    assert "bug_type" in cases[0]
    assert "description" in cases[0]
