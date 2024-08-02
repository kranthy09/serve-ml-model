"""
Unittests for summaries api wih monkeypatch
"""

import json

from datetime import datetime

import pytest

from app.api import crud


def test_create_summary(test_app, monkeypatch):
    """Test create summary successful"""
    test_request_payload = {"url": "https://foo.bar/"}
    test_response_paylaod = {"id": 1, "url": "https://foo.bar/"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/summaries/", data=json.dumps(test_request_payload))
    assert response.status_code == 201
    assert response.json() == test_response_paylaod


def test_create_summaries_invalid_json(test_app):
    """Test raises exception for invalid json"""
    response = test_app.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "url"],
                "msg": "Field required",
                "input": {},
                "url": "https://errors.pydantic.dev/2.8/v/missing",
            }
        ]
    }

    response = test_app.post("/summaries/", data=json.dumps({"url": "invalid://url"}))
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"] == "URL scheme should be 'http' or 'https'"
    )


def test_read_summary(test_app, monkeypatch):
    """Test read summary successful"""

    test_data = {
        "id": 1,
        "url": "https://foo.bar/",
        "summary": "dummy summary",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("summaries/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_app, monkeypatch):
    """Test raise exception with incorrect id"""

    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)
    response = test_app.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app, monkeypatch):
    """Test read all summaries successful"""

    test_data = [
        {
            "id": 1,
            "url": "https://foo.bar",
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": 2,
            "url": "https://testdrivenn.io",
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)
    response = test_app.get("/summaries/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_summary(test_app, monkeypatch):
    """Test remove a summary sucessful"""

    async def mock_get(id):
        return {
            "id": 1,
            "url": "https://foo.bar",
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        }

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    response = test_app.delete("/summaries/1/")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "url": "https://foo.bar/"}


def test_remove_summary_incorrect_id(test_app, monkeypatch):
    """Test raise exception remove summary with incorrect id"""

    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)
    response = test_app.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary(test_app, monkeypatch):
    """Test Update a summary successful"""

    test_request_data = {
        "url": "https://foo.bar",
        "summary": "updated!",
    }
    test_updated_data = {
        "id": 1,
        "url": "https://foo.bar",
        "summary": "updated!",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_put(id, payload):
        return test_updated_data

    monkeypatch.setattr(crud, "put", mock_put)
    response = test_app.put("/summaries/1/", data=json.dumps(test_request_data))
    assert response.status_code == 200
    assert response.json() == test_updated_data


@pytest.mark.parametrize(
    "summary_id, payload, status_code, detail",
    [
        [
            999,
            {"url": "https://foo.bar", "summary": "updated!"},
            404,
            "Summary not found",
        ],
        [
            0,
            {"url": "https://foo.bar", "summary": "updated!"},
            422,
            [
                {
                    "type": "greater_than",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "input": "0",
                    "ctx": {"gt": 0},
                    "url": "https://errors.pydantic.dev/2.8/v/greater_than",
                }
            ],
        ],
        [
            1,
            {},
            422,
            [
                {
                    "type": "missing",
                    "loc": ["body", "url"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.8/v/missing",
                },
                {
                    "type": "missing",
                    "loc": ["body", "summary"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.8/v/missing",
                },
            ],
        ],
        [
            1,
            {"url": "https://foo.bar/"},
            422,
            [
                {
                    "type": "missing",
                    "loc": ["body", "summary"],
                    "msg": "Field required",
                    "input": {"url": "https://foo.bar/"},
                    "url": "https://errors.pydantic.dev/2.8/v/missing",
                }
            ],
        ],
    ],
)
def test_update_summary_invalid(
    test_app, monkeypatch, summary_id, payload, status_code, detail
):
    """Test raise exception update summary invalid payload"""

    async def mock_put(summary_id, payload):
        return None

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(f"/summaries/{summary_id}/", data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_summary_invalid_url(test_app):
    """Test raises expection for update summary in invalid url"""
    response = test_app.put(
        "/summaries/1/",
        data=json.dumps({"url": "invalid://url", "summary": "updated!"}),
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"] == "URL scheme should be 'http' or 'https'"
    )
