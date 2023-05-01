from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
import sqlalchemy
#
router = APIRouter()
#
#
# # include top 3 actors by number of lines
@router.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: str):
    """
    This endpoint returns a single movie by its identifier. For each movie it returns:
    * `movie_id`: the internal id of the movie.
    * `title`: The title of the movie.
    * `top_characters`: A list of characters that are in the movie. The characters
      are ordered by the number of lines they have in the movie. The top five
      characters are listed.

    Each character is represented by a dictionary with the following keys:
    * `character_id`: the internal id of the character.
    * `character`: The name of the character.
    * `num_lines`: The number of lines the character has in the movie.

    """
    # need a single sql statement to return all rows

    query = """SELECT c.name, c.character_id, m.title, m.movie_id, COUNT(l.line_id)
                        FROM movies m
                        JOIN characters c ON m.movie_id = c.movie_id
                        JOIN lines l ON (c.character_id = l.character_id) AND (m.movie_id = l.movie_id)
                        WHERE m.movie_id = :movie_id
                        GROUP BY c.name, c.character_id, m.title, m.movie_id
                        ORDER BY count DESC
                        LIMIT 5"""

    result = db.conn.execute(sqlalchemy.text(query), {'movie_id': int(movie_id)})
    title = ""
    count = 0

    top_characters = []
    for row in result:
        count +=1
        title = row[2]
        inner_json = {
            "character_id": row[1],
            "character": row[0],
            "num_lines": row[4]
        }
        top_characters.append(inner_json)
    if count ==0:
        raise HTTPException(status_code=404, detail="movie not found.")

    json = {
        "movie_id": int(movie_id), "title": title,
        "top_characters": top_characters
    }

    return json


class movie_sort_options(str, Enum):
    movie_title = "movie_title"
    year = "year"
    rating = "rating"
#
#
# Add get parameters
@router.get("/movies/", tags=["movies"])
def list_movies(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: movie_sort_options = movie_sort_options.movie_title,
):
    """
    This endpoint returns a list of movies. For each movie it returns:
    * `movie_id`: the internal id of the movie. Can be used to query the
      `/movies/{movie_id}` endpoint.
    * `movie_title`: The title of the movie.
    * `year`: The year the movie was released.
    * `imdb_rating`: The IMDB rating of the movie.
    * `imdb_votes`: The number of IMDB votes for the movie.

    You can filter for movies whose titles contain a string by using the
    `name` query parameter.

    You can also sort the results by using the `sort` query parameter:
    * `movie_title` - Sort by movie title alphabetically.
    * `year` - Sort by year of release, earliest to latest.
    * `rating` - Sort by rating, highest to lowest.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """
    if sort is movie_sort_options.movie_title:
        order_by = db.movies.c.title
    elif sort is movie_sort_options.year:
        order_by = db.movies.c.year
    elif sort is movie_sort_options.rating:
        order_by = sqlalchemy.desc(db.movies.c.imdb_rating)
    else:
        assert False

    stmt = (
        sqlalchemy.select(
            db.movies.c.movie_id,
            db.movies.c.title,
            db.movies.c.year,
            db.movies.c.imdb_rating,
            db.movies.c.imdb_votes,
        )
        .limit(limit)
        .offset(offset)
        .order_by(order_by, db.movies.c.movie_id)
    )

    # filter only if name parameter is passed
    if name != "":
        stmt = stmt.where(db.movies.c.title.ilike(f"%{name}%"))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = []
        for row in result:
            json.append(
                {
                    "movie_id": int(row.movie_id),
                    "movie_title": row.title,
                    "year": row.year,
                    "imdb_rating": row.imdb_rating,
                    "imdb_votes": row.imdb_votes,
                }
            )
    return json