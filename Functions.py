import re
import requests as req
import pypdf as pdf
from io import BytesIO
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Funzione di connessione al database

def connect():

    uri = "mongodb+srv://lucagiovagnoli:t7g^Fyi7zpN!Liw@ufs13.dsmvdrx.mongodb.net/?retryWrites=true&w=majority&appName=UFS13"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['INCI']
    return db

db = connect()

# Funzione per sortare i valorei estratti dai pdf

def sorting_func(el):
    num = ''
    for char in el[0]:
        if char.isnumeric():
            num = num+char
        else:
            break
             
    return int(num)

# Funzione per recuperare dal DB la lista degli ingredienti disponibili, sia per nome comune
# che per nome INCI

def get_ingredients():

    puntatore = db.Ingredienti.find({},{"_id":0,"Nome_comune":1,"INCI_name":1})
    ingredienti = []

    for el in puntatore:
        if el['Nome_comune'] == el['INCI_name'] or not el['INCI_name']:
            ingredienti.append(el["Nome_comune"])
        else:
            ingredienti.append(el['Nome_comune'])
            ingredienti.append(el['INCI_name'])
    
    return ingredienti

# Funzione per recuperare l'oggetto corrispondente all'elemento cercato

def get_object(ingrediente):

    oggetto = db.Ingredienti.find_one({"$or":[
                            {"Nome_comune":ingrediente},
                            {"INCI_name":ingrediente}     
                            ]},{"_id":0})
    return oggetto

# Funzione per recuperare il testo da una fonte CIR, valido solo con i PDF

def source_text(url):
    try:
        response = req.get(url)
        file = BytesIO(response.content)            
        pdf_text=pdf.PdfReader(file)
        text = ''.join([x.extract_text() for x in pdf_text.pages])
        text = text.replace('\n','').replace('\r','')
        return text
    except:
        return False

# Funzione di ricerca di valori NOAEL da un testo

def get_noaels(text):    
            
    noael_pattern = r'(.{0,100}\bNOAEL\b.{0,100})'            
    noael_values = re.findall(noael_pattern,text)            
    noael_final_values = []
    if noael_values:
        for i in range(len(noael_values)):
            noael_value_pattern = r'\b\d+\s*[\.,]*\d*\s*.g/kg[\s*bw|body\s*weight]*[\/d.*]* \b'
            noael = re.findall(noael_value_pattern,noael_values[i])
            if noael:
                if len(noael) == 1:
                    noael_final_values.append((noael[0],noael_values[i]))
                else:
                    for el in noael:
                        noael_final_values.append((el,noael_values[i]))
    
    
    if noael_final_values:

        noael_final_values.sort(key=sorting_func)
        valori_noael = [x[0] for x in noael_final_values]
        contesti_noael = [x[1] for x in noael_final_values]
        return valori_noael,contesti_noael
    else:
        return False,False
            
# Funzione di ricerca di valori NOAEL da un testo

def get_ld50s(text):
     
    ld50_pattern = r'(.{0,100}\bLD\s*50\b.{0,100})'
    ld50_values = re.findall(ld50_pattern,text)
    ld50_final_values = []

    if ld50_values:
                
        for i in range(len(ld50_values)):
            ld50_value_pattern = r'\b\d+\s*[\.,]*\d*\s*.g/kg[\s*bw|body\s*weight]*\b'
            ld50 = re.findall(ld50_value_pattern,ld50_values[i])
            if ld50:
                if len(ld50) == 1:
                    ld50_final_values.append((ld50[0],ld50_values[i]))
                else:
                    for el in ld50:
                        ld50_final_values.append((el,ld50_values[i]))
            
    if ld50_final_values:
        ld50_final_values.sort(key=sorting_func)
        valori_ld50 = [x[0] for x in ld50_final_values]
        contesti_ld50 = [x[1] for x in ld50_final_values]
        return valori_ld50,contesti_ld50
    else:
        return False,False