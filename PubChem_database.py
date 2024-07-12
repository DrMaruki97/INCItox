from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests as req
from tqdm import tqdm


uri = "mongodb+srv://lucagiovagnoli:t7g^Fyi7zpN!Liw@ufs13.dsmvdrx.mongodb.net/?retryWrites=true&w=majority&appName=UFS13"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['INCI']

url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/JSON/?source=Hazardous%20Substances%20Data%20Bank%20(HSDB)&heading_type=Compound&heading=Non-Human%20Toxicity%20Values%20(Complete)&page=1'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
url_base = 'https://pubchem.ncbi.nlm.nih.gov/compound/'



response = req.get(url,headers=header)
response = response.json()
lista = response["Annotations"]["Annotation"]

for ingrediente in tqdm(lista):

    nome = ingrediente["Name"]

    try:
        cid = ingrediente["LinkedRecords"]["CID"][0]
    except:
        cid = ''

    if cid:
        link = f'{url_base}{cid}'
    else:
        link = f'{url_base}{nome}'
        if req.get(link,headers=header).status_code != 200:
            link = ''  
    
    dati = ingrediente["Data"]
    valori = []
    fonti = []
    
    for el in dati:

        try:

            fonte = el["Reference"][0]
            valore = el["Value"]["StringWithMarkup"][0]["String"]
            valori.append(valore)
            fonti.append(fonte)
        
        except:
            
            fonte = ''
            valore = ''
        
    oggetto = db.Ingredienti.find_one({"$or":[{"Nome_comune":nome},{"INCI_name":nome}]})

    if oggetto:

        db.Ingredienti.update_one({"_id":oggetto["_id"]},
                                {"$set":{"pbc_data":
                                        {"page":link,
                                            "valori":valori,
                                            "fonti":fonti}}})
    
    else:

        db.Ingredienti.insert_one({"Nome_comune":nome,
                                   "INCI_name":'',
                                   "main_link":'',
                                   "pdf_link":'',
                                   "pdf_date":'',
                                   "pdf_name":'',
                                   "valori_noael":'',
                                   "contesti_noael":'',
                                   "valori_ld50":'',
                                   "contesti_ld50":'',
                                   "pbc_data":
                                      {"page":link,
                                       "valori":valori,
                                       "fonti":fonti}})

    
