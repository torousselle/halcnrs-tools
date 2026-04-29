import streamlit as st

pages = {
    "Export Auteurs": [
        st.Page("list_authors_struct.py", title="Extraction des auteurs d'un code structure"),
        st.Page("list_authors_struct.py", title="Extraction des auteurs deuxieme test"),
    ]
}

pg = st.navigation(pages)
pg.run()
