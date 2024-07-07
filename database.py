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



request = 'https://cir-reports.cir-safety.org/FetchCIRReports/?&pagingcookie=%26lt%3bcookie%20page%3d%26quot%3b1%26quot%3b%26gt%3b%26lt%3bpcpc_name%20last%3d%26quot%3bPEG-50%20Stearate%26quot%3b%20first%3d%26quot%3b1%2c10-Decanediol%26quot%3b%20%2f%26gt%3b%26lt%3bpcpc_ingredientidname%20last%3d%26quot%3bPEG-50%20Stearate%26quot%3b%20first%3d%26quot%3b1%2c10-Decanediol%26quot%3b%20%2f%26gt%3b%26lt%3bpcpc_cirrelatedingredientsid%20last%3d%26quot%3b%7bC223037E-F278-416D-A287-2007B9671D0C%7d%26quot%3b%20first%3d%26quot%3b%7b940AF697-52B5-4A3A-90A6-B9DB30EF4A7E%7d%26quot%3b%20%2f%26gt%3b%26lt%3b%2fcookie%26gt%3b&page='
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
url_base = 'https://cir-reports.cir-safety.org/' 


for i in range(1,3):

    table = req.get(f'{request}{i}',headers=header)
    table = table.json()
    for el in tqdm(table['results']):
            if not r.get(f'Ingredient:{el['pcpc_ingredientname']}'):
                  
                r.set(f'Ingredient:{el['pcpc_ingredientname']}',f'https://cir-reports.cir-safety.org/cir-ingredient-status-report/?id={el['pcpc_ingredientid']}')
                r.set(f'Ingredient:{el['pcpc_ciringredientname']}',f'https://cir-reports.cir-safety.org/cir-ingredient-status-report/?id={el['pcpc_ingredientid']}')
                r.rpush('list:ingredients',f'{el['pcpc_ingredientname']}',f'{el['pcpc_ciringredientname']}')

ingredienti = r.lrange('list:ingredients',0,-1)


for el in tqdm(ingredienti[:101]):
    link = r.get(f'Ingredient:{el}')
    web_page = req.get(link,headers=header)
    page = BeautifulSoup(web_page.text,'html.parser')
    righe = page.find_all('tr')
    for i in range(1,len(righe)):
        riga = i      
        report = righe[i].a['href']
        if report[0] == '.':
            break
    final_url = url_base + report[report.index('/')+1:]
    r.set(f'pdf:{el}',final_url)
    date = righe[riga].find_all('td')[-1]       
    r.set(f'data_pdf:{el}',date.text)

      



