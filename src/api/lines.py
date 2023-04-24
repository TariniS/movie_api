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

    json_vals = []
    lineId = line_id
    print("inside lines.py", lineId)
    if line_id not in db.lines_by_id.keys():
        x = None
    lineText = db.lines_by_id[line_id]['line_text']
    character_id = db.lines_by_id[lineId]['character_id']
    conversation_id = db.lines_by_id[lineId]['conversation_id']
    movieId = db.lines_by_id[lineId]['movie_id']
    x = {
        "line_id": lineId, 
        "line_text":lineText, 
        "character_id": character_id, 
        "conversation_id": conversation_id, 
        "movie_id": movieId
    }
    json_vals.append(x)
    if x is None:
        raise HTTPException(status_code=404, detail="line not found.")
    return json_vals

   


@router.get("/lines/{char_name}", tags=["lines"])
def get_lines_char(char_name: str):
    """
    This endpoint returns a list of lines by character name. For each line it returns:
    * `line_id`: the internal id of the line.
    * `line_text`: The text of the line.
    * `character_id`: internal id of the given character.
    * `movie_id`: internal id of the given movie in which the character is speaking the line.
    """

    json_vals = []
    char_ids = set()
    if char_name not in db.character_names:
        x = None
    else:
        lst = db.character_names[char_name]
        for id in lst:
            char_ids.add(id["character_id"])

        for id in char_ids:
            for line in db.lines_dict_char[id]:
                x = {
                
                    "line_id": line["line_id"], 
                    "line_text": line["line_text"],
                    "character_id": int(id), 
                    "character_name": db.characters[id]['name'],
                    "movie_id": line["movie_id"]
                    }
                json_vals.append(x)
    if x is None:
        raise HTTPException(status_code=404, detail="line not found.")
    return json_vals
    

@router.get("/lines/conversations/{char_id}", tags=["lines"])
def get_conversations(char_id: str):
    """
    This endpoint returns a list of character names that the given character converses with. For each character it returns:
    * `character_id`: the internal id of the character
    * 'character_name`: the name of the character
    *` movie_title` : title of the movie


    * get a list of conversation id based on character id from lines.py
    * from the list of conversation id's get unique character names and return
    """

    if char_id not in db.lines_dict_char.keys():
        x = None
    conversation_ids = set()
    characters_ids = set()
    json_vals = []
    for line in db.lines_dict_char[char_id]:
        conversation_ids.add(line['conversation_id'])
    
    for id in conversation_ids:
        character1 = db.conversations_id_dict[id]["character1_id"]
        character2 = db.conversations_id_dict[id]["character2_id"]

        if character1 != char_id:
            characters_ids.add(character1)
        if character2 != char_id:
            characters_ids.add(character2)

    characters_ids = sorted(characters_ids, key=int)
    for id in characters_ids:
        x = {
            "character_id": int(id),
            "character_name": db.characters[id]['name'],
            "movie_title": db.movies[db.characters[id]['movie_id']]['title']
        }
        json_vals.append(x)
    
    if x is None:
        raise HTTPException(status_code=404, detail="line not found.")

    return json_vals
