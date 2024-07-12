from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests as req
from tqdm import tqdm
from bs4 import BeautifulSoup
import json

uri = "mongodb+srv://lucagiovagnoli:t7g^Fyi7zpN!Liw@ufs13.dsmvdrx.mongodb.net/?retryWrites=true&w=majority&appName=UFS13"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['INCI']
col = db['Ingredienti']

INGRED = []
for x in col.find({}, {"_id":1, "INCI_name": 1, "Nome_comune":1}): 
    INGRED.append(x)
#print(INGRED)
with open('hsdb database.json', 'r') as file:
    data = json.load(file)

# Filter the JSON data to only include the compounds listed in the text file
filtered_data = {
    "Annotations": {
        "Annotation": [annotation for annotation in data["Annotations"]["Annotation"] if annotation["Name"].upper() in INGRED]
    }
}

# Save the filtered data to a new JSON file
with open('inci_mongo_database.json', 'w') as file:
    json.dump(filtered_data, file, indent=4)

print("Filtered data saved to json")