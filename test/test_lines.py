from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_line():
    response = client.get("/lines/?line_id=49")
    assert response.status_code == 200

    with open("test/lines/49.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_line_name():
    response = client.get("/lines/chastity")
    assert response.status_code == 200

    with open("test/lines/linesbynamechastity.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_conversatinos():
    response = client.get("/lines/conversations/0")
    assert response.status_code == 200

    with open("test/lines/conversationsbylineid0.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_404():
    response = client.get("/lines/400")
    assert response.status_code == 404
