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

    query = """
    SELECT *
FROM movies m
JOIN characters c ON c.movie_id = m.movie_id
WHERE m.movie_id = :movie_id AND (c.character_id = :char1_id OR c.character_id = :char2_id)
    """

    result = db.conn.execute(sqlalchemy.text(query), {'char1_id': int(conversation.character_1_id),
                                                      'char2_id': int(conversation.character_2_id),
                                                      'movie_id': int(movie_id)})

    result2 = db.conn.execute(sqlalchemy.select(db.conversations.c.conversation_id)
                              .order_by(sqlalchemy.desc(db.conversations.c.conversation_id)))

    result3 = db.conn.execute(sqlalchemy.select(db.lines.c.line_id)
                              .order_by(sqlalchemy.desc(db.lines.c.line_id)))



    new_convo_id = int(result2.first()[0])+1
    new_line_id = int(result3.first()[0])+1
    print(new_line_id)
    count = 0
    vals = []

    for row in result:
        count += 1
    if count !=2 :
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
                current_line_sort = i+1
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


    """
    1. if movie_id in db.movies.keys()
    2. if conversation.character1_id in db.characters() and conversation.character2_id in db.characters()
    3. if conversation.character1_id ! = conversation.character2_id
    4. if db.characters(conversation.character1_id)['movie_id'] == move_id
    5. if db.characters(conversation.character2_id)['movie_id'] == movie_id
    6. for i in range(len(lines)):
            currentLine = lines[i]
            if currentLine.character_id == conversation.character1_id or currentLine.character_id == conversation.character2_id:
                currentLineSort = i
                
    
    -lines_dict
    -lines_by_id
    -lines_dict_char
    -lineID_charID
    -conversations_dict
    -conversations_dict2
    -conversations_id_dict
    """

# 2 characters and a series of lines 

# makes sure that all the characters are part of the given movie id
# that the characters are not the same 
# lines of a conversation match the characters involved in the conversation
# lines ordered in which the lines are provided
# returns the id of the resulting conversation that was created
# need to add to conversations.csv
# lines.csv
# update all hash maps that depend on movie, characters, line, etc. 
# only updating lines and conversations (as far as I know) ---> only for POST
# things neccessary:
        # adds 1 entry to conversations.csv
        # adds multiple entries to lines.csv with the same conversation id
        # conversation id 1 + the last id
        # check the db.conversations id which is being read from supabase
        # need to update hash maps?? ( worry about this later)


    # TODO: Remove the following two lines. This is just a placeholder to show
    # how you could implement persistent storage.


