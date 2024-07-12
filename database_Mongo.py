from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests as req
from tqdm import tqdm
from bs4 import BeautifulSoup


uri = "mongodb+srv://lucagiovagnoli:t7g^Fyi7zpN!Liw@ufs13.dsmvdrx.mongodb.net/?retryWrites=true&w=majority&appName=UFS13"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['INCI']


    


request = 'https://cir-reports.cir-safety.org/FetchCIRReports/?&pagingcookie=%26lt%3bcookie%20page%3d%26quot%3b1%26quot%3b%26gt%3b%26lt%3bpcpc_name%20last%3d%26quot%3bPEG-50%20Stearate%26quot%3b%20first%3d%26quot%3b1%2c10-Decanediol%26quot%3b%20%2f%26gt%3b%26lt%3bpcpc_ingredientidname%20last%3d%26quot%3bPEG-50%20Stearate%26quot%3b%20first%3d%26quot%3b1%2c10-Decanediol%26quot%3b%20%2f%26gt%3b%26lt%3bpcpc_cirrelatedingredientsid%20last%3d%26quot%3b%7bC223037E-F278-416D-A287-2007B9671D0C%7d%26quot%3b%20first%3d%26quot%3b%7b940AF697-52B5-4A3A-90A6-B9DB30EF4A7E%7d%26quot%3b%20%2f%26gt%3b%26lt%3b%2fcookie%26gt%3b&page='
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
url_base = 'https://cir-reports.cir-safety.org/' 


for i in range(1,3):

    table = req.get(f'{request}{i}',headers=header)
    table = table.json()
    for el in tqdm(table['results']):
            if not db.Ingredienti.find_one({"Nome_comune":f"{el['pcpc_ingredientname']}"}):

                
                Nome_comune = el['pcpc_ingredientname']
                INCI_name = el['pcpc_ciringredientname']
                link = f'https://cir-reports.cir-safety.org/cir-ingredient-status-report/?id={el['pcpc_ingredientid']}'
                web_page = req.get(link,headers=header)
                page = BeautifulSoup(web_page.text,'html.parser')
                righe = page.find_all('tr')
                if len(righe)>1:
                    for i in range(1,len(righe)):
                        riga = i      
                        report = righe[i].a['href']
                        if report[0] == '.':
                            break
                    if report[0] == '.':
                            final_url = url_base + report[report.index('/')+1:]
                            date = righe[riga].find_all('td')[-1].text
                            pdf_name = righe[riga].find_all('td')[-2].text
                    else:
                        final_url = ''
                else:
                    final_url = ''

                
                db.Ingredienti.insert_one({"Nome_comune":Nome_comune,
                                           "INCI_name":INCI_name,
                                           "main_link":link,
                                           "pdf_link":final_url,
                                           "pdf_date":date,
                                           "pdf_name":pdf_name,
                                           "pbc_data":{"page":'',
                                                       "valori":'',
                                                       "fonti":''}})
                        
                   
                    
                