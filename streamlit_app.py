import streamlit as st

pages = {
    "Codes": [
        st.Page("list_authors_struct.py", title="Extraction des auteurs d'un code structure"),
        st.Page("licence_chart.py", title="Répartition des dépôts par licence"),
        st.Page("notice_texte_chart.py", title="Evolution du type de dépôt par date de publi"),
        st.Page("doi_domain_chart.py", title="Pourcentage de Présence des DOI")
    ]
}

pg = st.navigation(pages)
pg.run()
