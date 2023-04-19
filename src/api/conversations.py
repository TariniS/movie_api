from fastapi import APIRouter
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

    """
    1. if movie_id in db.movies.keys()
    2. if conversation.character1_id in db.characters() and conversation.character2_id in db.characters()
    3. if conversation.character1_id ! = conversation.character2_id
    4. if db.characters(conversation.character1_id)['movie_id'] == movie_id
    5. if db.characters(conversation.character2_id)['movie_id'] == movie_id
    6. for i in range(len(lines)):
            currentLine = lines[i]
            if currentLine.character_id == conversation.character1_id or currentLine.character_id == conversation.character2_id:
                currentLineSort = i
    
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
#


    # TODO: Remove the following two lines. This is just a placeholder to show
    # how you could implement persistent storage.

    print(conversation)
    db.logs.append({"post_call_time": datetime.now(), "movie_id_added_to": movie_id})
    db.upload_new_log()