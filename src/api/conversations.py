import sqlalchemy
from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
from typing import List
from datetime import datetime


# FastAPI is inferring what the request body should look like
# based on the following two classes.
class LinesJson(BaseModel):
    character_id: int
    line_text: str


class ConversationJson(BaseModel):
    character_1_id: int
    character_2_id: int
    lines: List[LinesJson]


router = APIRouter()


@router.post("/movies/{movie_id}/conversations/", tags=["movies"])
def add_conversation(movie_id: int, conversation: ConversationJson):
    """
    This endpoint adds a conversation to a movie. The conversation is represented
    by the two characters involved in the conversation and a series of lines between
    those characters in the movie.

    The endpoint ensures that all characters are part of the referenced movie,
    that the characters are not the same, and that the lines of a conversation
    match the characters involved in the conversation.

    Line sort is set based on the order in which the lines are provided in the
    request body.

    The endpoint returns the id of the resulting conversation that was created.

    """

    query = """SELECT *
               FROM 
               movies m
               JOIN characters c ON c.movie_id = m.movie_id
               WHERE m.movie_id = :movie_id AND (c.character_id = :char1_id OR c.character_id = :char2_id)"""

    result = db.conn.execute(sqlalchemy.text(query), {'char1_id': int(conversation.character_1_id),
                                                      'char2_id': int(conversation.character_2_id),
                                                      'movie_id': int(movie_id)})

    result2 = db.conn.execute(sqlalchemy.select(db.conversations.c.conversation_id)
                              .order_by(sqlalchemy.desc(db.conversations.c.conversation_id)))

    result3 = db.conn.execute(sqlalchemy.select(db.lines.c.line_id)
                              .order_by(sqlalchemy.desc(db.lines.c.line_id)))

    new_convo_id = int(result2.first()[0]) + 1
    new_line_id = int(result3.first()[0]) + 1
    count = 0

    for row in result:
        count += 1
    # this is just to check the length of the returned result
    if count != 2:
        # if the query isnt of size 2, that means that either/both the characters were not in the specified movie
        # or the movie wasnt a valid id
        # or the character ids are both the same
        raise HTTPException(status_code=404, detail="line not found.")
    else:
        with db.engine.begin() as conn:
            conn.execute(
                sqlalchemy.insert(db.conversations),
                [
                    {
                        "conversation_id": new_convo_id,
                        "character1_id": conversation.character_1_id,
                        "character2_id": conversation.character_2_id,
                        "movie_id": movie_id
                    }
                ],
            )
        with db.engine.begin() as conn:
            for i in range(len(conversation.lines)):
                currentLine = conversation.lines[i]
                current_line_id = new_line_id + i
                current_character_id = currentLine.character_id
                current_movie_id = movie_id
                current_conversation_id = new_convo_id
                current_line_sort = i + 1
                current_line_text = currentLine.line_text
                conn.execute(
                    sqlalchemy.insert(db.lines),
                    [
                        {
                            "line_id": current_line_id,
                            "character_id": current_character_id,
                            "movie_id": current_movie_id,
                            "conversation_id": current_conversation_id,
                            "line_sort": current_line_sort,
                            "line_text": current_line_text
                        }
                    ],
                )
