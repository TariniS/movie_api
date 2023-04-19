from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query

router = APIRouter()


@router.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: int):
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

    x = None

    if movie_id in db.movies.keys():
        print("movie found")
    
    
        lines_sorted = sorted(db.lineID_charID.items(), key=lambda x: (-len(x[1])))
        sorted_dict = dict(lines_sorted) 

        top_characters = []

        for key in sorted_dict:
            if key[1] == movie_id:
                currentRow = sorted_dict[key]
                x = {
                    "character_id":int(key[0]),
                    "character":db.characters[key[0]]['name'], 
                    "num_lines": len(currentRow)
                }
                if len(top_characters) < 5:
                    top_characters.append(x)
    

        x = {
            "movie_id":int(movie_id), 
            "title": db.movies[movie_id]['title'],
            "top_characters": top_characters

        }

    if x is None:
        raise HTTPException(status_code=404, detail="movie not found.")

    return x


class movie_sort_options(str, Enum):
    movie_title = "movie_title"
    year = "year"
    rating = "rating"


# Add get parameters
@router.get("/movies/", tags=["movies"])
def list_movies(
    name: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
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
<<<<<<< HEAD
    x = None

    json_vals = []

    if sort == movie_sort_options.movie_title:

      myKeys = list(db.movie_by_name.keys())
      myKeys.sort()
      sorted_dict = {i: db.movie_by_name[i] for i in myKeys}
    
    elif sort == movie_sort_options.year:

      myKeys = list(db.movie_by_year.keys())
      myKeys.sort()
      sorted_dict = {i: db.movie_by_year[i] for i in myKeys}
    
    elif sort == movie_sort_options.rating:

      myKeys = list(db.movie_by_imdb_rating.keys())
      myKeys.sort(reverse=True)
      sorted_dict = {i: db.movie_by_imdb_rating[i] for i in myKeys}

    for key in sorted_dict:
        row : list = sorted_dict[key]
        for item in row: 
            x = {
            "movie_id":int(item['movie_id']),
            "movie_title": item['title'], 
            "year":item['year'], 
            "imdb_rating":float(item['imdb_rating']),
            "imdb_votes":int(item['imdb_votes'])
            }
            if len(json_vals)<limit:
                if name == "":
                    json_vals.append(x)
                else:
                    if name.lower() in (item['title']).lower():
                        json_vals.append(x)
            
            json = json_vals[offset: len(json_vals)]
=======
    if name:

        def filter_fn(m):
            return m.title and name.lower() in m.title

    else:

        def filter_fn(_):
            return True

    items = list(filter(filter_fn, db.movies.values()))
    if sort == movie_sort_options.movie_title:
        items.sort(key=lambda m: m.title)
    elif sort == movie_sort_options.year:
        items.sort(key=lambda m: m.year)
    elif sort == movie_sort_options.rating:
        items.sort(key=lambda m: m.imdb_rating, reverse=True)

    json = (
        {
            "movie_id": m.id,
            "movie_title": m.title,
            "year": m.year,
            "imdb_rating": m.imdb_rating,
            "imdb_votes": m.imdb_votes,
        }
        for m in items[offset : offset + limit]
    )
>>>>>>> upstream/main

    return json
