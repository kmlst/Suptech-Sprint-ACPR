import numpy as np
import pandas as pd


currency = "EUR"
equiv_NaN = ['Non spécifié', 'Non fourni']

def data_cleaning(df):
    cols_num = ["montant_minimum_investissement", "niveau_garantie", 
            "niveau_barriere_desactivante", "niveau_risque", "frais_ponctuels_entree", 
            "frais_ponctuels_sortie_echeance", "frais_ponctuels_sortie_anticipee", 
            "frais_recurrents", "frais_accessoires", "performance_tension", 
            "performance_maximale", "espérance_maximale_rendement"]    
    cat_cols = ["mention_complexite", "produit_sous_jacent", "nature_sous_jacent", "code_ISIN_sous_jacent",
            "code_ISIN", "nom_du_produit", "emetteur_du_produit"]
    df[cat_cols] = df[cat_cols].map(traitement_cat)
    df[cols_num] = df[cols_num].map(traitement_num)
    return df

def traitement_num(x):
    if isinstance(x, str):
        if currency in x: 
            x = x[:-4]
        if x in equiv_NaN:
            x = np.nan
        if '%' in str(x):
            x = str(x)[:-1]
    elif isinstance(x, float):
        x = x
    try:
        return float(x)
    except ValueError:
        return np.nan

def traitement_cat(x):
    # name disambiguiation
    if x in equiv_NaN:
        x = np.nan
    elif isinstance(x, float):
        x = str(x)
    elif x != np.nan:
        x = x.strip()
    return x

if __name__ == '__main__':
    raw_data = pd.read_csv('output/bdd_DIC_raw.csv')
    clean_data = data_cleaning(raw_data)
    clean_data.to_csv('output/bdd_DIC.csv')