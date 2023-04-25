from fastapi.testclient import TestClient

from src.api.server import app
from src import database as db

import json

client = TestClient(app)


def test_get_conversation():

    response = client.get(
        "/characters/5011"
    )
    prevNumLines = 0
    top_conversations = response.json()['top_conversations']
    print(top_conversations)
    for convo in top_conversations:
        if convo['character_id'] == 5016:
            prevNumLines = convo['number_of_lines_together']

    request_body = {
        "character_1_id": 5011,
        "character_2_id": 5016,
        "lines": [
            {
                "character_id": 5011,
                "line_text": "TESTING!"
            }
        ]
    }
    response = client.post("/movies/333/conversations/", json=request_body)
    assert response.status_code == 200
    response = client.get(
        "/characters/5011"
    )
    currentNumLines = 0
    top_conversations = response.json()['top_conversations']
    for convo in top_conversations:
        if convo['character_id'] == 5016:
            currentNumLines = convo['number_of_lines_together']
    assert currentNumLines == prevNumLines +1



def test_get_conversation2():

    new_line_id = int(db.lines[len(db.lines) - 1]['line_id']) + 1
    new_convo_id = int(db.conversations[len(db.conversations) - 1]['conversation_id']) + 1
    request_body = {
        "character_1_id": 5011,
        "character_2_id": 5016,
        "lines": [
            {
                "character_id": 5011,
                "line_text": "TESTING TESTING!"
            }
        ]
    }
    response = client.post("/movies/333/conversations/", json=request_body)
    assert response.status_code == 200
    response = client.get(
        "/lines/?line_id="+str(new_line_id)
    )
    expected_response = [{'line_id': str(new_line_id), 'line_text': 'TESTING TESTING!', 'character_id': '5011', 'conversation_id': str(new_convo_id),
      'movie_id': '333'}]

    assert response.json() == expected_response

