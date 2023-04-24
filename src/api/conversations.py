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
                
    
    -lines_dict
    -lines_by_id
    -lines_dict_char
    -lineID_charID
    -conversations_dict
    -conversations_dict2
    -conversations_id_dict
    """

    if str(movie_id) in db.movies.keys():
        #movie is valid
        if (str(conversation.character_1_id) in db.characters) and (str(conversation.character_2_id) in db.characters):
            #both the characters are valid
            if conversation.character_1_id != conversation.character_2_id:
                #both charactes are not the same
                if db.characters[str(conversation.character_1_id)]['movie_id'] == str(movie_id):
                    if db.characters[str(conversation.character_2_id)]['movie_id'] == str(movie_id):
                        #both the characters are in the provided movie
                        #this is a valid conversation, so add a conversation
                        new_convo_id = int(db.conversations[len(db.conversations)-1]['conversation_id']) + 1
                        newConversation = {"conversation_id": str(new_convo_id), "character1_id": str(conversation.character_1_id),
                                        "character2_id": str(conversation.character_2_id), "movie_id": str(movie_id)}

                        db.conversations.append(newConversation)
                        db.upload_new_conversation()

                        ## updating conversations hash maps

                        if str(conversation.character_1_id) not in db.conversations_dict.keys():
                            db.conversations_dict[str(conversation.character_1_id)] = [newConversation]
                        else:
                            val: list = db.conversations_dict[str(conversation.character_1_id)]
                            val.append(newConversation)
                            db.conversations_dict[str(conversation.character_1_id)] = val
                        if str(conversation.character_2_id) not in db.conversations_dict2.keys():
                            db.conversations_dict2[str(conversation.character_2_id)] = [newConversation]
                        else:
                            val: list = db.conversations_dict2[str(conversation.character_2_id)]
                            val.append(newConversation)
                            db.conversations_dict2[str(conversation.character_2_id)] = val

                        db.conversations_id_dict[str(new_convo_id)] = newConversation


                        # lines
                        # for each line in coversationJson.lines, create a new line id, line sort
                        # each line already has what character is saying that line
                        #line_id, character_id, movie_id, conversation_id, line_sort, line_text

                        new_line_id = int(db.lines[len(db.lines)-1]['line_id']) + 1
                        for i in range(len(conversation.lines)):
                            currentLine = conversation.lines[i]
                            current_line_id = new_line_id + i
                            current_character_id = currentLine.character_id
                            current_movie_id = movie_id
                            current_conversation_id = new_convo_id
                            current_line_sort = i+1
                            current_line_text = currentLine.line_text
                            newLine = {"line_id": str(current_line_id),
                                               "character_id": str(current_character_id),
                                               "movie_id": str(current_movie_id), "conversation_id": str(current_conversation_id),
                                       "line_sort": str(current_line_sort), "line_text": str(current_line_text)}
                            print("hello")
                            db.lines.append(newLine)
                            db.upload_new_line()

                            # updating hash maps
                            db.lines_by_id[str(current_line_id)] = newLine


                            if str(current_character_id) not in db.lines_dict_char.keys():
                                db.lines_dict_char[str(current_character_id)] = [newLine]
                            else:
                                val: list = db.lines_dict_char[str(current_character_id)]
                                val.append(newLine)
                                db.lines_dict_char[str(current_character_id)] = val

                            char_movie = (str(current_character_id), str(current_movie_id))
                            if char_movie not in db.lineID_charID.keys():
                                db.lineID_charID[char_movie] = [newLine]
                            else:
                                val: list = db.lineID_charID[char_movie]
                                val.append(newLine)
                                db.lineID_charID[char_movie] = val

                        # updating hash maps
                        db.lines_dict[str(new_convo_id)] = conversation.lines
                        print("updating db_lines_dict", str(new_convo_id))


                        return new_convo_id

    return 0

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

    print(conversation)

