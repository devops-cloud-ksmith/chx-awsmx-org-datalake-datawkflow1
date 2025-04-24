
import pytest
from handlers import lambda_handler

def test_lambda_handler_single_tier(monkeypatch):
    # Patch constants to avoid real AWS calls
    from config import constants
    monkeypatch.setattr(constants, "DRY_RUN", True)
    monkeypatch.setattr(constants, "FAIL_FAST", False)

    # Mock event
    event = {
        "org": "testorg",
        "record": "testrecord",
        "tiers": ["raw"],
        "date": "2025/01/01"
    }

    result = lambda_handler.lambda_handler(event, None)

    assert result["status"] == "complete"
    assert result["executed_for"] == "testorg"
    assert result["record"] == "testrecord"
    assert "raw: OK" in result["results"]

def test_lambda_handler_multiple_tiers(monkeypatch):
    from config import constants
    monkeypatch.setattr(constants, "DRY_RUN", True)
    monkeypatch.setattr(constants, "FAIL_FAST", False)

    event = {
        "org": "demo",
        "record": "data",
        "tiers": ["raw", "processed"],
        "date": "2024/12/31"
    }

    result = lambda_handler.lambda_handler(event, None)

    assert len(result["results"]) == 2
    assert all("OK" in r for r in result["results"])
