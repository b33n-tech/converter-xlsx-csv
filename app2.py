import streamlit as st
import pandas as pd
import numpy as np

st.title("📈 Analyse des financements ESS")

# Étape 1 : Upload
uploaded_file = st.file_uploader("📁 Upload ton fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Fichier chargé avec succès !")

    st.subheader("🔧 Configuration des colonnes")

    # Étape 2 : Sélection des colonnes
    date_col = st.selectbox("🗓️ Colonne contenant la **date du projet**", df.columns)
    montant_col = st.selectbox("💶 Colonne contenant le **montant collecté**", df.columns)

    # Choix du type de période
    periode = st.radio("📆 Regrouper par :", ["Trimestre", "Année"])

    if date_col and montant_col:
        # Conversion de la colonne date
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col, montant_col])

        if periode == "Trimestre":
            df["Période"] = df[date_col].dt.to_period("Q").astype(str)
        else:
            df["Période"] = df[date_col].dt.year.astype(str)

        df[montant_col] = pd.to_numeric(df[montant_col], errors='coerce')
        df = df.dropna(subset=[montant_col])

        # Calculs agrégés
        grouped = df.groupby("Période")[montant_col].agg(
            Nb_projets="count",
            Montant_total="sum",
            Montant_moyen="mean",
            Montant_médian="median"
        ).reset_index()

        # Formatage
        grouped["Montant_total"] = grouped["Montant_total"].round(2)
        grouped["Montant_moyen"] = grouped["Montant_moyen"].round(2)
        grouped["Montant_médian"] = grouped["Montant_médian"].round(2)

        st.subheader("📊 Résultats")
        st.dataframe(grouped)

        csv = grouped.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger les résultats (.csv)", data=csv, file_name="bilan_financements.csv")

