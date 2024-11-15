import streamlit as st
import pandas as pd  # type: ignore

pd.read_json("../scraper/json/links.json")

df = pd.read_json("../scraper/json/links.json")

tags = list(set(tag for tags_list in df["tags"] for tag in tags_list))

filter_tags = st.pills("Filtrar por tags", tags, selection_mode="multi")
st.write("Lista de APIs disponibilizadas pelo catalógo do ConectaAPI")
st.write(df)
