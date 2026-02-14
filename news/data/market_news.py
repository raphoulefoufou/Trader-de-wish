import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configuration
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")
TICKER = "NVDA"

# Fonctions

# Extrait le relevance_score pour le TICKER choisi
def get_relevance(ticker_list):
    for item in ticker_list:
        if item['ticker'] == TICKER:
            return float(item['relevance_score'])
    return 0.0

# Fonction pour appeler l'API News Sentiment
def fetch_api_news(start_date, end_date):
    url = (f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT"
           f"&tickers={TICKER}&time_from={start_date}&time_to={end_date}"
           f"&limit=1000&apikey={API_KEY}")
    try:
        response = requests.get(url)
        data = response.json()
        if "Information" in data:
            print(f"Quota atteint. Arrêt du script.")
            return None
        return data.get("feed", [])
    except Exception as e:
        print(f"Erreur lors de la requête : {e}")
        return []

# Filtre pour ne garder que 2 articles max par jour
def trier_et_filtrer_quotidien(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Fichier {input_file} introuvable pour le filtrage.")
        return

    print(f"Filtrage quotidien de {input_file}...")
    df = pd.read_csv(input_file)
    
    # Préparation des dates
    df['date_dt'] = pd.to_datetime(df['time_published'], format='%Y%m%dT%H%M%S')
    df['date_only'] = df['date_dt'].dt.date

    # Tri par date et par pertinence décroissante
    df_sorted = df.sort_values(by=['date_only', 'relevance_score'], ascending=[True, False])

    # Sélection : Max 2 articles par jour
    df_final = df_sorted.groupby('date_only').head(2)

    # Nettoyage des colonnes techniques
    df_final = df_final.drop(columns=['date_dt', 'date_only'])
    
    df_final.to_csv(output_file, index=False)
    print(f"Terminé : {len(df_final)} articles conservés dans {output_file}")

# ÉTAPE 1 : COLLECTE 2022 - 2024 (ANNUELLE)
file_raw_22_24 = f"news/data/{TICKER}_Raw_News_2022_2024.csv"

if not os.path.exists(file_raw_22_24):
    print(f"Collecte 2022-2024...")
    all_data_22_24 = []
    for year in [2022, 2023, 2024]:
        print(f"  Requête pour l'année {year}...")
        news = fetch_api_news(f"{year}0101T0000", f"{year}1231T2359")
        if news is None: break
        all_data_22_24.extend(news)
        time.sleep(15) # Pause pour respecter les limites de l'API
    
    if all_data_22_24:
        df = pd.DataFrame(all_data_22_24)
        df['relevance_score'] = df['ticker_sentiment'].apply(get_relevance)
        columns_to_keep = ['time_published', 'title', 'summary', 'overall_sentiment_score', 'relevance_score']
        df[columns_to_keep].to_csv(file_raw_22_24, index=False)
        print(f"Fichier brut généré : {file_raw_22_24}")
else:
    print(f"Étape 1 : {file_raw_22_24} existe déjà. On passe à la suite.")

# ÉTAPE 2 : COLLECTE 2025 - 2026 (MENSUELLE)
file_raw_25_26 = f"news/data/{TICKER}_Raw_News_2025_2026.csv"

if not os.path.exists(file_raw_25_26):
    print(f"Collecte 2025-2026...")
    periodes = [(2025, m) for m in range(1, 13)] + [(2026, m) for m in range(1, 3)]
    all_data_25_26 = []
    
    for y, m in periodes:
        print(f"  Récupération {y}-{m:02d}...")
        news = fetch_api_news(f"{y}{m:02d}01T0000", f"{y}{m:02d}28T2359") # On prend 28 jours pour éviter les soucis de fin de mois
        if news is None: break
        all_data_25_26.extend(news)
        time.sleep(15)
    
    if all_data_25_26:
        df = pd.DataFrame(all_data_25_26)
        df['relevance_score'] = df['ticker_sentiment'].apply(get_relevance)
        columns_to_keep = ['time_published', 'title', 'summary', 'overall_sentiment_score', 'relevance_score']
        df[columns_to_keep].to_csv(file_raw_25_26, index=False)
        print(f"Fichier brut généré : {file_raw_25_26}")
else:
    print(f"Étape 2 : {file_raw_25_26} existe déjà.")

# ÉTAPE 3 : FILTRAGE QUOTIDIEN
print("Étape 3 : Filtrage par pertinence (Max 2 par jour)...")
file_final_22_24 = f"news/data/{TICKER}_News_2022_2024.csv"
file_final_25_26 = f"news/data/{TICKER}_News_2025_2026.csv"

trier_et_filtrer_quotidien(file_raw_22_24, file_final_22_24)
trier_et_filtrer_quotidien(file_raw_25_26, file_final_25_26)

# ÉTAPE 4 : FUSION FINALE (MASTER)
print("Étape 4 : Fusion des fichiers finaux...")
if os.path.exists(file_final_22_24) and os.path.exists(file_final_25_26):
    df_22_24 = pd.read_csv(file_final_22_24)
    df_25_26 = pd.read_csv(file_final_25_26)

    # Fusion
    df_master = pd.concat([df_22_24, df_25_26], ignore_index=True)

    # Tri chronologique
    df_master['dt_temp'] = pd.to_datetime(df_master['time_published'], format='%Y%m%dT%H%M%S')
    df_master = df_master.sort_values(by='dt_temp')
    df_master = df_master.drop(columns=['dt_temp'])

    # Sauvegarde finale
    output_name = f"news/data/{TICKER}_News_2022_2026.csv"
    df_master.to_csv(output_name, index=False)

    print("-" * 30)
    print(f"Dataset créé : {output_name}")
    print(f"Nombre total d'articles : {len(df_master)}")
    print(f"Période : du {df_master['time_published'].iloc[0]} au {df_master['time_published'].iloc[-1]}") #
else:
    print("Fusion impossible : certains fichiers finaux manquent.")