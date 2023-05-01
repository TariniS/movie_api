import sqlalchemy
from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()


@router.get("/lines/", tags=["lines"])
def get_lines(line_id: str):
    """
    This endpoint returns information about a single line. 
    * `line_id`: the internal id of the line.
    * `line_text`: The text of the line.
    * `character_id`: internal id of the given character.
    * `conversation_id`: internal id of the conversation 
    * `movie_id`: internal id of the given movie in which the character is speaking the line.
    """

    query = """SELECT line_id, line_text, character_id, conversation_id, movie_id
               FROM
               lines
               WHERE line_id = :line_id"""

    result = db.conn.execute(sqlalchemy.text(query), {'line_id': int(line_id)})
    count = 0
    json = {}

    for row in result:
        count += 1
        json = {
            "line_id": row[0],
            "line_text": row[1],
            "character_id": row[2],
            "conversation_id": row[3],
            "movie_id": row[4]
        }

    if count == 0:
        raise HTTPException(status_code=404, detail="line not found.")

    return json


@router.get("/lines/{char_name}", tags=["lines"])
def get_lines_char(char_name: str):
    """
    This endpoint returns a list of lines by character name. For each line it returns:
    * `line_id`: the internal id of the line.
    * `line_text`: The text of the line.
    * `character_id`: internal id of the given character.
    * `movie_id`: internal id of the given movie in which the character is speaking the line.
    """

    query = """SELECT c.character_id, c.name, c.movie_id, l.line_id, l.line_text
               FROM
               characters c
               JOIN lines l ON l.character_id = c.character_id
               WHERE c.name ILIKE :char_name
               ORDER BY line_id"""

    result = db.conn.execute(sqlalchemy.text(query), {'char_name': char_name})
    count = 0
    vals = []

    for row in result:
        count += 1
        json = {
            "line_id": row[3],
            "line_text": row[4],
            "character_id": row[0],
            "character_name": row[1],
            "movie_id": row[2]
        }
        vals.append(json)

    if count == 0:
        raise HTTPException(status_code=404, detail="line not found.")

    return vals


@router.get("/lines/conversations/{char_id}", tags=["lines"])
def get_conversations(char_id: str):
    """
    This endpoint returns a list of character names that the given character converses with. For each character it returns:
    * `character_id`: the internal id of the character
    * 'character_name`: the name of the character
    *` movie_id` : id of the movie


    * get a list of conversation id based on character id from lines.py
    * from the list of conversation id's get unique character names and return
    """

    query = """WITH 
                first_convos AS(
                SELECT cv.character1_id AS other_character_id
                FROM
                lines l
                JOIN conversations cv ON cv.conversation_id = l.conversation_id
                WHERE cv.character2_id = :char_id
                GROUP BY other_character_id),

                second_convos AS(
                SELECT cv.character2_id AS other_character_id
                FROM lines l 
                JOIN conversations cv ON cv.conversation_id = l.conversation_id
                WHERE cv.character1_id = :char_id
                GROUP BY other_character_id),

                total_convos AS(
                SELECT *
                FROM
                first_convos
                UNION
                all
                SELECT * FROM
                second_convos),
                
                character_convos AS(
                SELECT *
                FROM
                total_convos
                JOIN characters c ON c.character_id = other_character_id)
                
            SELECT *
            FROM
            character_convos"""

    result = db.conn.execute(sqlalchemy.text(query), {'char_id': int(char_id)})
    count = 0
    vals = []

    for row in result:
        count += 1
        json = {
            "character_id": row[0],
            "character_name": row[2],
            "movie_id": row[3]
        }
        vals.append(json)

    if count == 0:
        raise HTTPException(status_code=404, detail="line not found.")

    return vals
