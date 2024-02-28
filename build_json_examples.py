import pandas as pd
import json


examples_df = pd.read_excel('Exemples + résumés méca.xlsx')
examples_df.columns = [
    "code_ISIN", 
    "nom_du_produit", 
    "emetteur_du_produit", 
    "date_emission", 
    "date_remboursement", 
    "mention_complexite", 
    "montant_minimum_investissement", 
    "niveau_garantie", 
    "niveau_barriere_desactivante", 
    "niveau_risque", 
    "produit_sous_jacent", 
    "nature_sous_jacent", 
    "code_ISIN_sous_jacent", 
    "frais_ponctuels_entree", 
    "frais_ponctuels_sortie_echeance", 
    "frais_ponctuels_sortie_anticipee", 
    "frais_recurrents", 
    "frais_accessoires", 
    "performance_tension", 
    "performance_maximale", 
    "espérance_maximale_rendement",
    "resume_mecanisme"]

examples_json = examples_df.astype(str).to_dict(orient='index')

for i in range(len(examples_json)):
    with open('example' + str(i + 1) + '.json', "w") as f:
        json.dump(examples_json[i], f, default=str)
    i += 1