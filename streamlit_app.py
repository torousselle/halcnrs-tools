import streamlit as st

pages = {
    "Codes": [
        st.Page("list_authors_struct.py", title="Extraction des auteurs d'un code structure"),
        st.Page("licence_chart.py", title="Répartition des dépôts par licence")
    ]
}

pg = st.navigation(pages)
pg.run()
