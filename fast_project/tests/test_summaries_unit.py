import json
from datetime import datetime, timezone

import pytest

from fast_app.api import crud, summaries


def test_create_summary(test_app, monkeypatch):
    def mock_generate_summary(summary_id, url):
        return None

    monkeypatch.setattr(summaries, "generate_summary", mock_generate_summary)

    test_request_payload = {"url": "https://koltemugdha.wordpress.com/"}
    test_response_payload = {"id": 1, "url": "https://koltemugdha.wordpress.com/"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        "/summaries/",
        data=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_summaries_invalid_json(test_app):
    response = test_app.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "url"],
                "msg": "Field required",
                "input": {},
                "url": "https://errors.pydantic.dev/2.7/v/missing",
            }
        ]
    }

    response = test_app.post("/summaries/", data=json.dumps({"url": "invalid://url"}))
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"] == "URL scheme should be 'http' or 'https'"
    )


def test_read_summary(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "url": "https://koltemugdha.wordpress.com/",
        "summary": "summary",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "url": "https://koltemugdha.wordpress.com/",
            "summary": "summary",
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        },
        {
            "id": 2,
            "url": "https://www.linkedin.com/in/mugdha-kolte-43472ab3/",
            "summary": "summary",
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/summaries/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_summary(test_app, monkeypatch):
    async def mock_get(id):
        return {
            "id": 1,
            "url": "https://koltemugdha.wordpress.com/",
            "summary": "summary",
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "url": "https://koltemugdha.wordpress.com/"}


def test_remove_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary(test_app, monkeypatch):
    test_request_payload = {
        "url": "https://koltemugdha.wordpress.com/",
        "summary": "updated",
    }
    test_response_payload = {
        "id": 1,
        "url": "https://koltemugdha.wordpress.com/",
        "summary": "summary",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    async def mock_put(id, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/summaries/1/", data=json.dumps(test_request_payload))
    assert response.status_code == 200
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "summary_id, payload, status_code, detail",
    [
        [
            999,
            {"url": "https://koltemugdha.wordpress.com/", "summary": "updated!"},
            404,
            "Summary not found",
        ],
        [
            0,
            {"url": "https://koltemugdha.wordpress.com/", "summary": "updated!"},
            422,
            [
                {
                    "type": "greater_than",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "input": "0",
                    "ctx": {"gt": 0},
                    "url": "https://errors.pydantic.dev/2.7/v/greater_than",
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
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                },
                {
                    "type": "missing",
                    "loc": ["body", "summary"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                },
            ],
        ],
        [
            1,
            {"url": "https://koltemugdha.wordpress.com/"},
            422,
            [
                {
                    "type": "missing",
                    "loc": ["body", "summary"],
                    "msg": "Field required",
                    "input": {"url": "https://koltemugdha.wordpress.com/"},
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                }
            ],
        ],
    ],
)
def test_update_summary_invalid(
    test_app, monkeypatch, summary_id, payload, status_code, detail
):
    async def mock_put(id, payload):
        return None

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(f"/summaries/{summary_id}/", data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_summary_invalid_url(test_app):
    response = test_app.put(
        "/summaries/1/",
        data=json.dumps({"url": "invalid://url", "summary": "updated!"}),
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"] == "URL scheme should be 'http' or 'https'"
    )
