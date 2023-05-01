import sqlalchemy
from sqlalchemy import func
from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db

router = APIRouter()


@router.get("/characters/{id}", tags=["characters"])
def get_character(id: str):
    """
    This endpoint returns a single   character by its identifier. For each character
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

    query = """WITH 
                first_convos AS (
                SELECT c.character_id, c.name, c.gender, m.title, cv.conversation_id AS convo_ids, cv.character2_id AS second_character_ids
                FROM 
                characters c
                JOIN movies m ON c.movie_id = m.movie_id
                JOIN conversations cv ON (cv.character1_id = c.character_id)
                WHERE c.character_id = :character_id
                GROUP BY c.character_id, c.name, c.gender, m.title, cv.character2_id, cv.conversation_id),

                second_convos AS (
                SELECT c.character_id, c.name, c.gender, m.title, cv.conversation_id AS convo_ids, cv.character1_id AS second_character_ids
                FROM 
                characters c
                JOIN movies m ON c.movie_id = m.movie_id
                JOIN conversations cv ON (cv.character2_id = c.character_id)
                WHERE c.character_id = :character_id
                GROUP BY c.character_id, c.name, c.gender, m.title, cv.character1_id, cv.conversation_id),

                total_convos AS (
                SELECT *
                FROM
                first_convos
                UNION ALL
                SELECT *
                FROM
                second_convos), 
                
                lines_convos AS (
                SELECT total_convos.character_id, total_convos.name, total_convos.gender, total_convos.title, total_convos.convo_ids, total_convos.second_character_ids, l.line_id
                FROM 
                total_convos
                JOIN lines l ON total_convos.convo_ids = l.conversation_id),
                
                final_convos AS (
                SELECT lines_convos.character_id, lines_convos.name, lines_convos.gender, lines_convos.title, lines_convos.second_character_ids, COUNT(line_id) AS num_of_lines
                FROM lines_convos
                GROUP BY character_id, name, gender, title, second_character_ids),
                
                final_final_convos AS (
                SELECT final_convos.character_id, final_convos.name, final_convos.gender, final_convos.title, final_convos.second_character_ids, final_convos.num_of_lines, c.name AS secondName, c.gender AS secondGender
                FROM final_convos
                JOIN characters c on c.character_id = final_convos.second_character_ids
                ORDER BY final_convos.num_of_lines DESC, second_character_ids)

    
            SELECT * 
            FROM final_final_convos"""

    result = db.conn.execute(sqlalchemy.text(query), {'character_id': int(id)})
    character_id = 0
    character_name = ""
    movie = ""
    gender = ""
    count = 0

    top_conversations = []
    for row in result:
        count += 1
        character_id = row[0]
        character_name = row[1]
        movie = row[3]
        gender = row[2]
        inner_json = {
            "character_id": row[4],
            "character": row[6],
            "gender": row[7],
            "number_of_lines_together": row[5]
        }
        top_conversations.append(inner_json)

    json = {
        "character_id": character_id,
        "character": character_name,
        "movie": movie,
        "gender": gender,
        "top_conversations": top_conversations
    }
    if count == 0:
        raise HTTPException(status_code=404, detail="character not found.")

    return json


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

    if sort is character_sort_options.character:
        order_by = db.characters.c.name
    elif sort is character_sort_options.movie:
        order_by = db.movies.c.title
    elif sort is character_sort_options.number_of_lines:
        order_by = sqlalchemy.desc(func.count(db.lines.c.line_id))
    else:
        assert False

    stmt = (
        sqlalchemy.select(db.characters.c.character_id,
                          db.characters.c.name,
                          db.movies.c.title,
                          func.count(db.lines.c.line_id).label("count"))
        .select_from(
            db.characters
            .join(db.movies, db.characters.c.movie_id == db.movies.c.movie_id)
            .join(db.lines, db.characters.c.character_id == db.lines.c.character_id)
        )
        .group_by(db.characters.c.character_id, db.movies.c.title)
        .limit(limit)
        .offset(offset)
        .order_by(order_by, db.characters.c.character_id)
    )

    # filter only if name parameter is passed
    if name != "":
        stmt = stmt.where(db.characters.c.name.ilike(f"%{name}%"))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = []
        for row in result:
            json.append(
                {
                    "character_id": row.character_id,
                    "character": row.name,
                    "movie": row.title,
                    "number_of_lines": row.count
                }
            )
    return json
