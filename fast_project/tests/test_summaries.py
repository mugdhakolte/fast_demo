import json


def test_create_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://koltemugdha.wordpress.com/"})
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://koltemugdha.wordpress.com/"


def test_create_summaries_invalid_json(test_app):
    response = test_app.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "url"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.7/v/missing",
            }
        ]
    }


def test_read_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://koltemugdha.wordpress.com/"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://koltemugdha.wordpress.com/"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get(
        "/summaries/999",
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.get("/summaries/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"gt": 0},
                "input": "0",
                "loc": ["path", "id"],
                "msg": "Input should be greater than 0",
                "type": "greater_than",
                "url": "https://errors.pydantic.dev/2.7/v/greater_than",
            }
        ]
    }


def test_read_all_summaries(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://koltemugdha.wordpress.com/"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1


def test_remove_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries", data=json.dumps({"url": "https://koltemugdha.wordpress.com/"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.delete(f"summaries/{summary_id}/")
    assert response.status_code == 200
    assert response.json() == {
        "id": summary_id,
        "url": "https://koltemugdha.wordpress.com/",
    }


def test_remove_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries", data=json.dumps({"url": "https://koltemugdha.wordpress.com/"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/{summary_id}/",
        data=json.dumps(
            {"url": "https://koltemugdha.wordpress.com/", "summary": "updated!"}
        ),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://koltemugdha.wordpress.com/"
    assert response_dict["summary"] == "updated!"
    assert response_dict["created_at"]


def test_update_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        "/summaries/999/",
        data=json.dumps(
            {"url": "https://koltemugdha.wordpress.com/", "summary": "updated!"}
        ),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary_invalid_json(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries", data=json.dumps({"url": "https://koltemugdha.wordpress.com/"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/{summary_id}/",
        data=json.dumps({}),
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "url"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.7/v/missing",
            },
            {
                "input": {},
                "loc": ["body", "summary"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.7/v/missing",
            },
        ]
    }


def test_update_summary_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://koltemugdha.wordpress.com/"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/{summary_id}/",
        data=json.dumps({"url": "https://koltemugdha.wordpress.com/"}),
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {"url": "https://koltemugdha.wordpress.com/"},
                "loc": ["body", "summary"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.7/v/missing",
            }
        ]
    }
