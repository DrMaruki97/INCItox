import streamlit as st
import pandas as pd
import strm_functions as f

st.set_page_config(layout="wide")

db = f.connect()

ingredienti = f.get_ingredients()

if 'noael' not in st.session_state:
    st.session_state.noael = False

if 'ld50' not in st.session_state:
    st.session_state.ld50 = False
    

with st.columns([0.44,0.12,0.44])[1]:

    st.title('INCI:green[tox]')

with st.columns([0.19,0.63,0.18])[1]:

    st.header('Ricerca di valori NOAEL e LD50 da [:blue[CIR]](https://cir-reports.cir-safety.org/) e da [:orange[PubChem]](https://pubchem.ncbi.nlm.nih.gov/)')




st.selectbox('Inserire un ingrediente',
              ingredienti,
              index=None,
              placeholder='',
              key='selectbox'
              )

if st.session_state.selectbox:

    with st.spinner('Caricamento'):

        oggetto = f.get_object(st.session_state.selectbox)

        fonte_cir = oggetto["pdf_link"]
        data_cir = oggetto["pdf_date"]
        nome_fonte_cir = oggetto["pdf_name"]
        valori_noael = oggetto["valori_noael"]
        contesti_noael = oggetto["contesti_noael"]
        valori_ld50 = oggetto["valori_ld50"]
        contesti_ld50 = oggetto["contesti_ld50"]
        link_pbc = oggetto["pbc_data"]["page"]
        values_pbc = oggetto["pbc_data"]["valori"]
        sources_pbc = oggetto["pbc_data"]["fonti"]


        if fonte_cir:
            str_fonte_cir = f'Fonte trovata: [{nome_fonte_cir}]({fonte_cir}) Data: {data_cir}'
        else:
            str_fonte_cir = 'Nessuna fonte :blue[CIR] disponibile per questo ingrediente'

        if link_pbc:
            str_page_pbc = f'Pagina :orange[PubChem]: [link]({link_pbc})'
        else:
            str_page_pbc = 'Nessuna pagina :orange[Pubchem] trovata'


    cir_col,pbc_col = st.columns([0.65,0.45])
    
    with cir_col:

        st.header(':blue[CIR]:')
        st.write(str_fonte_cir)

        noael_col,ld50_col = st.columns(2)

        with noael_col:
            
            def noael_button():
                st.session_state.noael = True
                st.session_state.ld50 = False

            st.button('NOAEL',on_click=noael_button)
            

        with ld50_col:

            def ld50_button():
                st.session_state.ld50 = True
                st.session_state.noael = False

            st.button('LD50',on_click=ld50_button)                

        if st.session_state.noael:

            if not valori_noael:
                st.write(':red[Non siamo riusciti ad estrarre valori NOAEL da questa fonte]')
            
            else:
                tabella = pd.DataFrame({'Noael':valori_noael,'Contesto':contesti_noael})
                st.table(tabella.assign(hack='').set_index('hack'))

        elif st.session_state.ld50:

            if not valori_ld50:
                    st.write(':red[Non siamo riusciti ad estrarre valori LD50 da questa fonte]')

            else:
                tabella = pd.DataFrame({'LD50':valori_ld50,'Contesto':contesti_ld50})
                st.table(tabella.assign(hack='').set_index('hack'))

    
    with pbc_col:

        st.header(':orange[PubChem]:')
        st.write(str_page_pbc)

        for i in range(len(values_pbc)):

            st.write(f':red[Valore]: {values_pbc[i]}')
            st.write(f':orange[Fonte]: {sources_pbc[i]}')