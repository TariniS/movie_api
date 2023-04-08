import csv

# TODO: You will want to replace all of the code below. It is just to show you
# an example of reading the CSV files where you will get the data to complete
# the assignment.

print("reading movies")

# with open("movies.csv", mode="r", encoding="utf8") as csv_file:
#     movies = [
#         {k: v for k, v in row.items()}
#         for row in csv.DictReader(csv_file, skipinitialspace=True)
#     ]

with open("movies.csv", mode="r", encoding="utf8") as csv_file:
    reader = csv.DictReader(csv_file)
    movies = {row.pop('movie_id'): row for row in reader}

# with open("characters.csv", mode="r", encoding="utf8") as csv_file:
#     characters2 = [
#         {k: v for k, v in row.items()}
#         for row in csv.DictReader(csv_file, skipinitialspace=True)
#     ]

with open("characters.csv", mode="r", encoding="utf8") as csv_file:
    reader = csv.DictReader(csv_file)
    characters = {row.pop('character_id'): row for row in reader}




# with open("characters.csv", mode="r", encoding="utf8") as csv_file:
#     reader = csv.DictReader(csv_file)
#     characters_names = {row.pop('name'): row for row in reader}


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

# with open("conversations.csv", mode="r", encoding="utf8") as csv_file:
#     reader = csv.DictReader(csv_file)
#     conversations = {row.pop('character1_id'): row for row in reader}

with open("lines.csv", mode="r", encoding="utf8") as csv_file:
    lines = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(csv_file, skipinitialspace=True)
    ]


# with open("lines.csv", mode="r", encoding="utf8") as csv_file:
#     reader = csv.DictReader(csv_file)
#     lines = {row.pop('conversation_id'): row for row in reader}
  
# re read in all of them to make them into dictionary by key of movie id
            
# can combine characters and movie information through movie id
# for each movie id, t
# character id, movie id as keys - > movie information, conversations based on character id, lines based on conversations
# for each character the top conversations needs to be 
# conversations based on character id -> another character id
# for those conversations can combine into number of lines
# 


# character i1_id. 


character_names = dict()

for id in characters:
    name = characters[id]['name']
    if name not in character_names.keys():
        character_names[name] = [characters[id]]
    else:
        val: list = character_names[name] 
        val.append(characters[id])
        character_names[name] = val

print("names")
print(character_names)


lines_dict = dict()

for line in lines:
    conversationId = line["conversation_id"]
    if conversationId not in lines_dict.keys():
        # no character 1 information is found, then add
        lines_dict[conversationId] = [line]
    else:
        val: list = lines_dict[conversationId] 
        val.append(line)
        lines_dict[conversationId] = val



conversations_dict = dict()
for conversation in conversations:
    character1ID = conversation["character1_id"]
    if character1ID not in conversations_dict.keys():
        # no character 1 information is found, then add
        conversations_dict[character1ID] = [conversation]
    else:
        val: list = conversations_dict[character1ID] 
        val.append(conversation)
        conversations_dict[character1ID] = val

conversations_dict2 = dict()
for conversation in conversations2:
    character2ID = conversation["character2_id"]
    if character2ID not in conversations_dict2.keys():
        # no character 1 information is found, then add
        conversations_dict2[character2ID] = [conversation]
    else:
        val: list = conversations_dict2[character2ID] 
        val.append(conversation)
        conversations_dict2[character2ID] = val




