import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Convertisseur CSV → XLSX")

# Upload du fichier CSV
uploaded_file = st.file_uploader("Téléversez un fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Lire le CSV
    try:
        df = pd.read_csv(uploaded_file)
        st.success("Fichier CSV chargé avec succès.")
        st.dataframe(df.head())

        # Convertir en XLSX
        def convert_df_to_xlsx(dataframe):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, index=False, sheet_name='Feuille1')
            processed_data = output.getvalue()
            return processed_data

        xlsx_data = convert_df_to_xlsx(df)

        # Bouton de téléchargement
        st.download_button(
            label="📥 Télécharger le fichier XLSX",
            data=xlsx_data,
            file_name="converted_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier CSV : {e}")
else:
    st.info("Veuillez importer un fichier CSV pour commencer.")
