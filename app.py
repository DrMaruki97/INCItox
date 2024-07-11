import streamlit as st
import pandas as pd
import Functions as f

st.set_page_config(layout="wide")

db = f.connect()

ingredienti = f.get_ingredients()

    

with st.columns([0.44,0.12,0.44])[1]:

    st.title('INCI:green[tox]')

with st.columns([0.28,0.46,0.26])[1]:

    st.header(f'Ricerca di valori NOAEL e LD50 da [CIR]({'https://cir-reports.cir-safety.org/'})')

ricerca = st.selectbox('Inserire un ingrediente',
                       ingredienti,
                       index=None,
                       placeholder='')

if ricerca:

    with st.spinner('Caricamento'):

        oggetto = f.get_object(ricerca)

    cir_col,pbc_col = st.columns([0.65,0.45])
    
    with cir_col:

        st.write(':blue[CIR]:')

        fonte = oggetto["pdf_link"]
        data = oggetto["pdf_date"]
        nome_fonte = oggetto["pdf_name"]

        if fonte:

            tab_fonte = pd.DataFrame({'Fonte':[fonte],'Data di rilascio':[data]})

            st.dataframe(tab_fonte,
                        hide_index=True,
                        column_config={'Fonte':st.column_config.LinkColumn(
                                        display_text= nome_fonte,
                                        width='medium'),
                                        'Data di rilascio':st.column_config.TextColumn(width='medium')},
                        use_container_width=False
                        )

            source = f.source_text(fonte)

            valori_noael,contesti_noael = f.get_noaels(source)
            valori_ld50,contesti_ld50 = f.get_ld50s(source)

            if valori_noael:
                noaels = pd.DataFrame({'NOAEL':valori_noael,'Contesto':contesti_noael})
            else:
                noaels = 'Impossibile estrarre i dati di NOAEL da questa fonte'
                
            if valori_ld50:
                ld50s = pd.DataFrame({'LD50':valori_ld50,'Contesto':contesti_ld50})
            else:
                ld50s = 'Impossibile estrarre i dati di LD50 da questa fonte'

            st.write(noaels,ld50s)
        
        else:
            st.write('Nessuna fonte :blue[CIR] disponibile per questo ingrediente')
    
    with pbc_col:

        st.write(':orange[PubChem]:')
                
                
       
                        




