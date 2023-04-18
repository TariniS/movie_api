import csv

# TODO: You will want to replace all of the code below. It is just to show you
# an example of reading the CSV files where you will get the data to complete
# the assignment.

print("reading movies")

with open("movies.csv", mode="r", encoding="utf8") as csv_file:
    movies2 = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(csv_file, skipinitialspace=True)
    ]

with open("movies.csv", mode="r", encoding="utf8") as csv_file:
    reader = csv.DictReader(csv_file)
    movies = {row.pop('movie_id'): row for row in reader}

with open("characters.csv", mode="r", encoding="utf8") as csv_file:
    characters2 = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(csv_file, skipinitialspace=True)
    ]

with open("characters.csv", mode="r", encoding="utf8") as csv_file:
    reader = csv.DictReader(csv_file)
    characters = {row.pop('character_id'): row for row in reader}


with open("conversations.csv", mode="r", encoding="utf8") as csv_file:
    conversations = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(csv_file, skipinitialspace=True)
    ]

with open("conversations.csv", mode="r", encoding="utf8") as csv_file:
    conversations2 = [
    {k: v for k, v in row.items()}
    for row in csv.DictReader(csv_file, skipinitialspace=True)
]

with open("lines.csv", mode="r", encoding="utf8") as csv_file:
    lines = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(csv_file, skipinitialspace=True)
    ]
  
movie_by_name = dict()
count = 0

for id in movies2:
    name = id['title']
    if name not in movie_by_name.keys():
        movie_by_name[name] = [id]
    else:
        val: list = movie_by_name[name] 
        val.append(id)
        count += 1
        movie_by_name[name] = val

movie_by_year = dict()
count = 0

for id in movies2:
    year = id['year']
    if year not in movie_by_year.keys():
        movie_by_year[year] = [id]
    else:
        val: list = movie_by_year[year] 
        val.append(id)
        count += 1
        movie_by_year[year] = val

movie_by_imdb_rating = dict()
count = 0

for id in movies2:
    rating = id['imdb_rating']
    if rating not in movie_by_imdb_rating.keys():
        movie_by_imdb_rating[rating] = [id]
    else:
        val: list = movie_by_imdb_rating[rating] 
        val.append(id)
        count += 1
        movie_by_imdb_rating[rating] = val

character_names = dict()
count = 0

for id in characters2:
    name = id['name']
    if name.lower() not in character_names.keys():
        character_names[name.lower()] = [id]
    else:
        val: list = character_names[name.lower()] 
        val.append(id)
        count += 1
        character_names[name.lower()] = val

movies_names = dict()
count = 0

for id in characters2:
    characterId = id['character_id']
    movieId = id['movie_id']
    name = movies[movieId]['title']
    if name not in movies_names.keys():
        movies_names[name] = [id]
    else:
        val: list = movies_names[name] 
        val.append(id)
        movies_names[name] = val


lines_dict = dict()


for line in lines:
    conversationId = line["conversation_id"]
    if conversationId not in lines_dict.keys():

        lines_dict[conversationId] = [line]
    else:
        val: list = lines_dict[conversationId] 
        val.append(line)
        
        lines_dict[conversationId] = val


lines_dict_char = dict()


lines_by_id = dict()


for line in lines:
    lineId = line["line_id"]
    if lineId not in lines_by_id.keys():

        lines_by_id[lineId] = line


lines_dict_char = dict()

count = 0
for line in lines:
    charId = line["character_id"]
    if charId not in lines_dict_char.keys():
        lines_dict_char[charId] = [line]
    else:
        val: list = lines_dict_char[charId] 
        val.append(line)
        count +=1
        lines_dict_char[charId] = val

lineID_charID = dict()

for charId in lines_dict_char.keys():
    currentLines = lines_dict_char[charId]
    for line in currentLines:
        movie_id = line['movie_id']
        char_movie = (charId, movie_id)
        if char_movie not in lineID_charID.keys():
            lineID_charID[char_movie] = [line]
        else:
            val : list = lineID_charID[char_movie]
            val.append(line)
            lineID_charID[char_movie] = val



conversations_dict = dict()
for conversation in conversations:
    character1ID = conversation["character1_id"]
    if character1ID not in conversations_dict.keys():
        conversations_dict[character1ID] = [conversation]
    else:
        val: list = conversations_dict[character1ID] 
        val.append(conversation)
        conversations_dict[character1ID] = val

conversations_dict2 = dict()
for conversation in conversations2:
    character2ID = conversation["character2_id"]
    if character2ID not in conversations_dict2.keys():
        conversations_dict2[character2ID] = [conversation]
    else:
        val: list = conversations_dict2[character2ID] 
        val.append(conversation)
        conversations_dict2[character2ID] = val


conversations_id_dict = dict()
for conversation in conversations2:
    convoId = conversation["conversation_id"]
    if convoId not in conversations_id_dict.keys():
        conversations_id_dict[convoId] = conversation








