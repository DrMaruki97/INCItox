import requests
import redis
import requests as req
from tqdm import tqdm
from bs4 import BeautifulSoup
import string



r = redis.Redis(
    host='redis-11492.c300.eu-central-1-1.ec2.redns.redis-cloud.com',
    port = 11492,
    password='0ssFnSEhNJ6Hn7JVtznKkpOuAD1ffdtR',
    decode_responses=True
)

def get_cid(ingredient):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{ingredient}/cids/TXT"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return None

ingredients = r.lrange('list:ingredients',0,-1)
a = len(ingredients)
print(a)
j = 0
# Open a file to write the CIDs
with open('cids.txt', 'w') as cid_file:
    for ingredient in ingredients:
        cid = get_cid(ingredient)
        if cid:
            cid_file.write(f"{cid}\n")
            j = j + 1
            print(j)
        else:
            j = j + 1
            print(j)

        

print("CIDs have been written to cids.txt")
