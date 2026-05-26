#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# -----------------------------------
# Interface Streamlit
# -----------------------------------

st.title("Statistiques HAL")

st.sidebar.header("Paramètres")

# Champs modulables
coll_code = st.sidebar.text_input(
    "Collection HAL (collCode_s)",
    value="CNRS"
)

year_start = st.sidebar.number_input(
    "Année début",
    min_value=1990,
    max_value=2100,
    value=2016
)

year_end = st.sidebar.number_input(
    "Année fin",
    min_value=1990,
    max_value=2100,
    value=2025
)

doc_type = st.sidebar.text_input(
    "Type de document (docType_s)",
    value="ART"
)

# -----------------------------------
# Construction de l'URL
# -----------------------------------

url = (
    "https://api.archives-ouvertes.fr/search/"
    f"?q=*:*"
    "&rows=0"
    "&facet=true"
    "&facet.pivot=submittedDateY_i,submitType_s"
    f"&fq=collCode_s:{coll_code}"
    f"&fq=submittedDateY_i:[{year_start} TO {year_end}]"
    f"&fq=docType_s:{doc_type}"
    "&facet.sort=index"
    "&wt=json"
)

# Affichage URL
st.code(url)

# -----------------------------------
# Requête API
# -----------------------------------

response = requests.get(url)

if response.status_code != 200:
    st.error("Erreur API HAL")
    st.stop()

data = response.json()

# -----------------------------------
# Extraction des données
# -----------------------------------

pivot_data = data["facet_counts"]["facet_pivot"]["submittedDateY_i,submitType_s"]

results = []

for year_entry in pivot_data:

    year = year_entry["value"]

    notice_annex = 0
    file_count = 0

    if "pivot" in year_entry:

        for sub in year_entry["pivot"]:

            submit_type = sub["value"]
            count = sub["count"]

            if submit_type in ["notice", "annex"]:
                notice_annex += count

            elif submit_type == "file":
                file_count += count

    results.append({
        "Année": year,
        "notice+annex": notice_annex,
        "file": file_count
    })

# -----------------------------------
# DataFrame
# -----------------------------------

df = pd.DataFrame(results)

if not df.empty:

    df = df.sort_values("Année")

    # Tableau
    st.subheader("Tableau des données")
    st.dataframe(df)

    # -----------------------------------
    # Graphique
    # -----------------------------------

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(
        df["Année"],
        df["notice+annex"],
        label="notice+annex"
    )

    ax.bar(
        df["Année"],
        df["file"],
        bottom=df["notice+annex"],
        label="file"
    )

    ax.set_xlabel("Année")
    ax.set_ylabel("Nombre de dépôts")
    ax.set_title("Dépôts HAL par année")

    ax.legend()

    ax.set_xticks(df["Année"])

    st.subheader("Graphique")
    st.pyplot(fig)

else:
    st.warning("Aucune donnée trouvée.")


# In[ ]:




