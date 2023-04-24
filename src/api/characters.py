from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()


@router.get("/characters/{id}", tags=["characters"])
def get_character(id: str):
    """
    This endpoint returns a single character by its identifier. For each character
    it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `gender`: The gender of the character.
    * `top_conversations`: A list of characters that the character has the most
      conversations with. The characters are listed in order of the number of
      lines together. These conversations are described below.

    Each conversation is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `gender`: The gender of the character.
    * `number_of_lines_together`: The number of lines the character has with the
      originally queried character.
    """
    conversations_list_ids = set()
    conversations_list_lines = dict()

    total_conversations = dict()
    x = None

    character_id = id
    
    if character_id in db.characters.keys():
      character_name = db.characters[character_id]['name']
      movie_name = db.movies[db.characters[character_id]['movie_id']]['title']
      gender = db.characters[character_id]['gender']
      if gender == '':
          gender = None

      if character_id in db.conversations_dict.keys():
        for conversation in db.conversations_dict[character_id]:
          conversations_list_ids.add(conversation["character2_id"])
          if conversation["character2_id"] in total_conversations.keys():
            val: list = total_conversations[conversation["character2_id"]]
            val.append(conversation["conversation_id"])
            total_conversations[conversation["character2_id"]] = val
          else:
            total_conversations[conversation["character2_id"]] = [conversation["conversation_id"]]

          
      if character_id in db.conversations_dict2.keys():
        for conversation in db.conversations_dict2[character_id]:
          conversations_list_ids.add(conversation["character1_id"])
          if conversation["character1_id"] in total_conversations.keys():
            val: list = total_conversations[conversation["character1_id"]]
            val.append(conversation["conversation_id"])
            total_conversations[conversation["character1_id"]] = val
          else:
            total_conversations[conversation["character1_id"]] = [conversation["conversation_id"]]


      for charId in total_conversations:
        listConvoIds = total_conversations[charId]
        sum = 0
        for convoId in listConvoIds:
          sum = sum + len(db.lines_dict[convoId])
        conversations_list_lines[charId] = sum
      

      top_conversationsSorted = sorted(conversations_list_lines.items(), key=lambda x: (-x[1], x[0]))
      sortedFinal = dict(top_conversationsSorted)
      
      top_convosJson = []

      for charId in sortedFinal.keys():
        charName = db.characters[charId]['name']
        gen = db.characters[charId]['gender']
        if gen == '':
          gen = None
        numLines = sortedFinal[charId]
        val = {
          "character_id":int(charId), 
          "character":charName, 
          "gender":gen, 
          "number_of_lines_together": numLines
        }
        top_convosJson.append(val)
      x = {
        "character_id": int(character_id),
        "character": character_name,
        "movie": movie_name,
        "gender": gender,
        "top_conversations": top_convosJson
      }
    if x is None:
        raise HTTPException(status_code=404, detail="movie not found.")

    return x


class character_sort_options(str, Enum):
    character = "character"
    movie = "movie"
    number_of_lines = "number_of_lines"


@router.get("/characters/", tags=["characters"])
def list_characters(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: character_sort_options = character_sort_options.character,
):



    """
    This endpoint returns a list of characters. For each character it returns:
    * `character_id`: the internal id of the character. Can be used to query the
      `/characters/{character_id}` endpoint.
    * `character`: The name of the character.
    * `movie`: The movie the character is from.
    * `number_of_lines`: The number of lines the character has in the movie.

    

    You can filter for characters whose name contains a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `character` - Sort by character name alphabetically.
    * `movie` - Sort by movie title alphabetically.
    * `number_of_lines` - Sort by number of lines, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    json = None
    offsetReduction = offset

    json_vals = []

    if sort == character_sort_options.character:
      myKeys = list(db.character_names.keys())
      myKeys.sort()
      sorted_dict = {i: db.character_names[i] for i in myKeys}
    elif sort == character_sort_options.movie:
      myKeys = list(db.movies_names.keys())
      myKeys.sort()
      sorted_dict = {i: db.movies_names[i] for i in myKeys}
    else:
      lines_sorted = sorted(db.lineID_charID.items(), key=lambda x: (-len(x[1])))
      sorted_dict = dict(lines_sorted)

      for key in sorted_dict:
        row : list  = sorted_dict[key]
        x = {
          "character_id":int(key[0]),
          "character":db.characters[key[0]]['name'], 
          "movie":db.movies[key[1]]['title'], 
          "number_of_lines":len(row)
        }

        
        
        if len(json_vals) < limit:
          if name == "":
            json_vals.append(x)
          else:
            if name.lower() in (db.characters[key[0]]['name']).lower():
              json_vals.append(x)
        


      json = json_vals[offset: len(json_vals)]
        

    
    if sort == character_sort_options.character or sort == character_sort_options.movie:
      for key in sorted_dict:
        row : list = sorted_dict[key]
        for item in row: 
          x = {
            "character_id":int(item['character_id']),
            "character":db.characters[item['character_id']]['name'], 
            "movie":db.movies[item['movie_id']]['title'], 
            "number_of_lines":len(db.lineID_charID[(item['character_id'], item['movie_id'])])
          }
          if len(json_vals)<limit and offsetReduction<=0:
            if name == "":
              json_vals.append(x)
            else:
              if name.lower() in (item['name']).lower():
                json_vals.append(x)
            offsetReduction -=1
          json = json_vals[offset: len(json_vals)]

    return json