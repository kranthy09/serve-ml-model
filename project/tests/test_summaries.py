"""
Tests for /summaries endpoint
"""

import json

import pytest


def test_create_summary(test_app_with_db):
    """Test Create summary"""

    response = test_app_with_db.post(
        "/summaries", data=json.dumps({"url": "https://foo.bar"})
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_create_summaries_invalid_json(test_app_with_db):
    """Test raise error with invalid json"""

    response = test_app_with_db.post("/summaries", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "Field required",
                "type": "missing",
                "input": {},
                "url": "https://errors.pydantic.dev/2.8/v/missing",
            }
        ]
    }


def test_read_summary(test_app_with_db):
    """Test to read the summary"""

    response = test_app_with_db.post(
        "/summaries", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    """Test return Not found for incorrect summary id."""

    response = test_app_with_db.get("/summaries/12345")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summmary not found"


def test_read_all_summaries(test_app_with_db):
    """Test read all summaries"""

    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    assert (
        len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1
    )
