#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------
# UI STREAMLIT
# ---------------------------------------

st.set_page_config(page_title="HAL DOI Dashboard", layout="wide")

st.title("📊 Analyse HAL : Avec / Sans DOI")

st.sidebar.header("Filtres")

coll_code = st.sidebar.text_input("collCode_s", "CNRS")
doc_type = st.sidebar.text_input("docType_s", "ART")
domain = st.sidebar.text_input("primaryDomain_s", "shs")

year_start = st.sidebar.number_input("Année début", 2000, 2100, 2016)
year_end = st.sidebar.number_input("Année fin", 2000, 2100, 2025)

# ---------------------------------------
# API BUILDER
# ---------------------------------------

def hal_query(fq_extra):
    return (
        "https://api.archives-ouvertes.fr/search/"
        "?q=*:*"
        "&rows=0"
        "&facet=true"
        "&facet.field=publicationDateY_i"
        f"&fq=collCode_s:{coll_code}"
        f"&fq=docType_s:{doc_type}"
        f"&fq=primaryDomain_s:{domain}"
        f"&fq=publicationDateY_i:[{year_start} TO {year_end}]"
        f"{fq_extra}"
        "&facet.sort=index"
        "&wt=json"
    )

# ---------------------------------------
# REQUESTS
# ---------------------------------------

url_with_doi = hal_query("&fq=doiId_s:*")
url_without_doi = hal_query("&fq=!doiId_s:*")

data_with = requests.get(url_with_doi).json()
data_without = requests.get(url_without_doi).json()

# ---------------------------------------
# EXTRACTION FACET
# ---------------------------------------

facet_with = data_with["facet_counts"]["facet_fields"]["publicationDateY_i"]
facet_without = data_without["facet_counts"]["facet_fields"]["publicationDateY_i"]

# conversion liste HAL -> dict
def parse_facet(facet):
    return {facet[i]: facet[i+1] for i in range(0, len(facet), 2)}

with_doi = parse_facet(facet_with)
without_doi = parse_facet(facet_without)

# ---------------------------------------
# DATAFRAME
# ---------------------------------------

years = sorted(set(with_doi.keys()) | set(without_doi.keys()))

df = pd.DataFrame({
    "Année": years,
    "Avec DOI": [with_doi.get(y, 0) for y in years],
    "Sans DOI": [without_doi.get(y, 0) for y in years],
})

df["Total"] = df["Avec DOI"] + df["Sans DOI"]
df["% DOI"] = (df["Avec DOI"] / df["Total"]) * 100

# ---------------------------------------
# TABLEAU
# ---------------------------------------

st.subheader("📋 Tableau des données")
st.dataframe(df, use_container_width=True)

# ---------------------------------------
# GRAPHIQUE
# ---------------------------------------

fig = go.Figure()

# Barres empilées
fig.add_trace(go.Bar(
    x=df["Année"],
    y=df["Sans DOI"],
    name="Sans DOI"
))

fig.add_trace(go.Bar(
    x=df["Année"],
    y=df["Avec DOI"],
    name="Avec DOI"
))

# Courbe %
fig.add_trace(go.Scatter(
    x=df["Année"],
    y=df["% DOI"],
    name="% DOI",
    mode="lines+markers",
    yaxis="y2"
))

# Layout double axe
fig.update_layout(
    barmode="stack",
    title="HAL : DOI vs non DOI",
    xaxis_title="Année",
    yaxis_title="Nombre de publications",
    yaxis2=dict(
        title="% DOI",
        overlaying="y",
        side="right",
        range=[0, 100]
    ),
    legend=dict(orientation="h"),
    height=600
)

st.subheader("📊 Graphique")
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------
# EXPORT
# ---------------------------------------

st.download_button(
    "📥 Télécharger CSV",
    df.to_csv(index=False).encode("utf-8"),
    "hal_doi_stats.csv",
    "text/csv"
)

