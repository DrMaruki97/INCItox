import toml as tm
from strm_functions import connect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests as req
from tqdm import tqdm


#region Connessione DB

# Ci connettiamo al nostro database Mongodb

db_keys = tm.load('.\\streamlit\\secrets.toml')

db = connect(db_keys['db_user'],db_keys['db_psw'])

#endregion

#region Preparazione

# Prepariamo l'url per ottenere i dati LD50 presenti su PubChem, che vengono tutti dalla fonte dati HSDB, l'header da
# usare nella richiesta e l'url base che completato rimanderà alla pagina PubChem dell'ingrediente

url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/annotations/heading/JSON/?source=Hazardous%20Substances%20Data%20Bank%20(HSDB)&heading_type=Compound&heading=Non-Human%20Toxicity%20Values%20(Complete)&page=1'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
url_base = 'https://pubchem.ncbi.nlm.nih.gov/compound/'

# Prepariamo una lista con anche tutti i nomi degli ingredienti attualmente nel nostro database, ovvero quelli
# ottenuti dal CIR

ingredienti = []
for x in db.Ingredienti.find({}, {"_id":1, "INCI_name": 1, "Nome_comune":1}): 
    ingredienti.append(x)

#endregion

#region Ottenimento dati PubChem

# Effettuiamo la richiesta http per ottenere il json HSDB e lo leggiamo

response = req.get(url,headers=header)
response = response.json()

# Andiamo a prendere la lista di tutti gli ingredienti salvati nel json

lista = response["Annotations"]["Annotation"]

# Cicliamo sulla lista per esaminare un ingrediente alla volta

for ingrediente in tqdm(lista):

    # Salviamo il nome dell'ingrediente

    nome = ingrediente["Name"]

    # Poichè alcuni ingredienti mancano della chiave CID, inseriamo questa richiesta in un try per gestire questa evenienza

    try:
        cid = ingrediente["LinkedRecords"]["CID"][0]
    except:
        cid = ''

    # Componiamo il link alla pagina per gli ingredienti che hanno un valore CID, per gli altri controlliamo se usando il nome
    # della molecola al posto del cid la pagina sia comunque raggiungibile e in caso positivo salviamo questo link completo

    if cid:
        link = f'{url_base}{cid}'
    else:
        link = f'{url_base}{nome}'
        if req.get(link,headers=header).status_code != 200:
            link = ''  
    
    dati = ingrediente["Data"]
    valori = []
    fonti = []
    
    # Ad ogni ingrediente corrispondono più valori registrati, quindi cicliamo su questa lista e ci salviamo tutti i valori
    # con la corrispondente fonte

    for el in dati:

        # Poichè alcuni valori mancano di una fonte, inseriamo questo passaggio in un try e qualora si verifichi questa eventualità
        # scartiamo il valore

        try:

            fonte = el["Reference"][0]
            valore = el["Value"]["StringWithMarkup"][0]["String"]
            valori.append(valore)
            fonti.append(fonte)
        
        except:
            
            fonte = ''
            valore = ''

#endregion

#region Controllo esistenza

    # Dopo aver ottenuto tutti i dati controlliamo se l'ingrediente in esame è già disponibile sul nostro DB
    # Siccome i nomi sono salvati in modo diverso tra i due DB li confrontiamo mettendoli in lowercase

    for el in ingredienti:
        if nome.lower() == el['Nome_comune'].lower() or nome == el['INCI_name'].lower():
            pointer = el['_id']
            break
        else:
            pointer = ''

#endregion

#region Aggiornamento DB

    # Se abbiamo trovato una corrispondenza andiamo a inserire i dati PubChem nel documento già esistente

    if pointer:        

        db.Ingredienti.update_one({"_id":pointer},
                                {"$set":{"pbc_data":
                                        {"page":link,
                                            "valori":valori,
                                            "fonti":fonti}}})
        
    # Se non abbiamo trovato una corrispondenza inseriamo un nuovo documento con all'interno unicamente dai dati PubChem
    
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
        
#endregion

    
