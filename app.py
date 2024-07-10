import streamlit as st
import pandas as pd
import CosmeticIngredientReview as cir
import redis
import pypdf as pdf
import re
import requests as req
from io import BytesIO

r = redis.Redis(
    host='redis-11492.c300.eu-central-1-1.ec2.redns.redis-cloud.com',
    port = 11492,
    password='0ssFnSEhNJ6Hn7JVtznKkpOuAD1ffdtR',
    decode_responses=True
)

def sorting_func(el):
    return el[0].split(' ')[0]


ingredienti = r.lrange('list:ingredients',0,-1)

st.set_page_config(layout="wide")

st.title('INCI:green[tox]')
st.header(f'Ricerca di valori NOAEL e LD50 da [CIR]({'https://cir-reports.cir-safety.org/'})')

ricerca = st.selectbox('Inserire un ingrediente',ingredienti,index=None)

if ricerca:

    fonte = r.get(f'pdf:{ricerca}')
    data = r.get(f'data_pdf:{ricerca}')



    if fonte:

        tab_fonte = pd.DataFrame({'Fonte':[fonte],'Data di rilascio':[data]})

        st.dataframe(tab_fonte,
                     hide_index=True,
                     column_config={'Fonte':st.column_config.LinkColumn(
                                    display_text= 'Clicca per andare alla fonte'),
                                    'Data di rilascio':st.column_config.TextColumn(width='medium')},
                     use_container_width=False
                     )

        try:
            response = req.get(fonte)
            file = BytesIO(response.content)            
            pdf_text=pdf.PdfReader(file)
            print(len(pdf_text.pages))
            text = ''.join([x.extract_text() for x in pdf_text.pages])
            text = text.replace('\n','').replace('\r','')
            noael_pattern = r'(.{0,100}\bNOAEL\b.{0,100})'
            ld50_pattern = r'(.{0,100}\bLD\s*50\b.{0,100})'
            noael_values = re.findall(noael_pattern,text,re.IGNORECASE)
            ld50_values = re.findall(ld50_pattern,text,re.IGNORECASE)
            ld50_final_values = []
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
            
            if noael_final_values:

                noael_final_values.sort(key=sorting_func,reverse=True)
                valori_noael = [x[0] for x in noael_final_values]
                contesti_noael = [x[1] for x in noael_final_values]

            if ld50_final_values:
                ld50_final_values.sort(key=sorting_func,reverse=True)
                valori_ld50 = [x[0] for x in ld50_final_values]
                contesti_ld50 = [x[1] for x in ld50_final_values]

            if noael_final_values:
                noaels = pd.DataFrame({'NOAEL':valori_noael,'Contesto':contesti_noael})
            if ld50_final_values:
                ld50s = pd.DataFrame({'LD50':valori_ld50,'Contesto':contesti_ld50})

            
            
            st.write(noaels,ld50s)
        
        
        except Exception as e:
                        st.error(f"ERRORE: {e}")

    else:
        st.write('Nessuna fonte disponibile per questo ingrediente')



