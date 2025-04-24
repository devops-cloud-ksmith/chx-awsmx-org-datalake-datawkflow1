import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from handlers.lambda_handler import lambda_handler
from config import constants
import pytest

def test_lambda_dry_run(monkeypatch):
    monkeypatch.setattr(constants, "DRY_RUN", True)
    monkeypatch.setattr(constants, "FAIL_FAST", False)

    event = {
        "org": "mzq",
        "record": "contacts",
        "tiers": ["raw", "processed"],
        "date": "2025/04/23"
    }

    result = lambda_handler(event, None)
    assert result["status"] == "complete"
    assert result["executed_for"] == "mzq"
    assert "raw: OK" in result["results"]
    assert "processed: OK" in result["results"]