import streamlit as st
import pandas as pd
import CosmeticIngredientReview as cir
import redis

r = redis.Redis(
    host='redis-11492.c300.eu-central-1-1.ec2.redns.redis-cloud.com',
    port = 11492,
    password='0ssFnSEhNJ6Hn7JVtznKkpOuAD1ffdtR',
    decode_responses=True
)

ingredienti = r.lrange('list:ingredients',0,-1)

st.title('INCItox')
st.header('Scegli il nome INCI da cercare')

ricerca = st.selectbox('',ingredienti)

valore = r.get(f'pdf:{ricerca}')

valore

