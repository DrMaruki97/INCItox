# Funzioni di ricerca pdf su CIR

import requests as req
import string 
from bs4 import BeautifulSoup

def aggiorna_database(database:dict):

    request = 'https://cir-reports.cir-safety.org/FetchCIRReports/?&pagingcookie=%26lt%3bcookie%20page%3d%26quot%3b1%26quot%3b%26gt%3b%26lt%3bpcpc_name%20last%3d%26quot%3bPEG-50%20Stearate%26quot%3b%20first%3d%26quot%3b1%2c10-Decanediol%26quot%3b%20%2f%26gt%3b%26lt%3bpcpc_ingredientidname%20last%3d%26quot%3bPEG-50%20Stearate%26quot%3b%20first%3d%26quot%3b1%2c10-Decanediol%26quot%3b%20%2f%26gt%3b%26lt%3bpcpc_cirrelatedingredientsid%20last%3d%26quot%3b%7bC223037E-F278-416D-A287-2007B9671D0C%7d%26quot%3b%20first%3d%26quot%3b%7b940AF697-52B5-4A3A-90A6-B9DB30EF4A7E%7d%26quot%3b%20%2f%26gt%3b%26lt%3b%2fcookie%26gt%3b&page='
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    
    for i in range(1,3):

        table = req.get(f'{request}{i}',headers=header)
        table = table.json()

        for el in table['results']:

            database[(el['pcpc_ciringredientname'],el['pcpc_ingredientname'])] = [el['pcpc_ingredientid']]


def get_source(chiave : tuple, database : dict):

    url_base = 'https://cir-reports.cir-safety.org/'    
    web_page = req.get(f'{url_base}cir-ingredient-status-report/?id={database[chiave][0]}')
    page = BeautifulSoup(web_page.text)
    righe = page.find_all('tr')        
    report = righe[1].a['href']
    final_url = url_base + report[report.index('/')+1:]
    database[chiave].append(final_url)
    date = righe[1].find_all('td')[-1]
    date = date.text[-4:]
    database[chiave].append(date)