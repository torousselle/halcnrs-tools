import streamlit as st

pages = {
    "Export Auteurs": [
        st.Page("list_authors.py", title="Extraction des auteurs d'un code structure"),
    ]
}

pg = st.navigation(pages)
pg.run()
