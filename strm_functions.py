import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Funzione di connessione al database

def connect(user,password):

    uri = f"mongodb+srv://{user}:{password}@ufs13.dsmvdrx.mongodb.net/?retryWrites=true&w=majority&appName=UFS13"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['INCI']
    return db

db = connect(st.secrets['db_user'],st.secrets['db_psw'])

# Funzione per recuperare dal DB la lista degli ingredienti disponibili, sia per nome comune
# che per nome INCI

def get_ingredients():

    puntatore = db.Ingredienti.find({},{"_id":0,"Nome_comune":1,"INCI_name":1})
    ingredienti = []

    for el in puntatore:
        if el["Nome_comune"] == el["INCI_name"] or not el["INCI_name"]:
            ingredienti.append(el["Nome_comune"])
        else:
            ingredienti.append(el["Nome_comune"])
            ingredienti.append(el["INCI_name"])
    
    return ingredienti

# Funzione per recuperare l'oggetto corrispondente all'elemento cercato

def get_object(ingrediente):

    oggetto = db.Ingredienti.find_one({"$or":[
                            {"Nome_comune":ingrediente},
                            {"INCI_name":ingrediente}     
                            ]},{"_id":0})
    return oggetto            