import pandas as pd
import numpy as np
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm

# On redirige le cache de Hugging Face vers le disque D
os.environ['HF_HOME'] = 'D:/HuggingFaceCache'
# Créer le dossier s'il n'existe pas
if not os.path.exists('D:/HuggingFaceCache'):
    os.makedirs('D:/HuggingFaceCache')

# --- CONFIGURATION ---
PATH_TO_DATASET = 'datasetv6.csv'
PATH_TO_NEWS_FOLDER = 'news/data/'  # Dossier contenant vos fichiers Ticker_News...
OUTPUT_FILE = 'datasetv6_sentiment.csv'

# 1. CHARGEMENT DE FINBERT
print("Chargement de FinBERT (ProsusAI)...")
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

# Utilisation du GPU si disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def get_sentiment_probabilities(texts):
    """ Calcule le score (P_pos - P_neg) pour une liste de textes en batch """
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Softmax pour obtenir les probabilités [Positive, Negative, Neutral]
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1).cpu().numpy()
    
    # Score Net = Prob(Pos) - Prob(Neg)
    net_scores = probs[:, 0] - probs[:, 1]
    return net_scores

def process_all_news():
    # 2. CHARGEMENT DU DATASET PRINCIPAL
    print(f"Chargement de {PATH_TO_DATASET}...")
    df_main = pd.read_csv(PATH_TO_DATASET)
    df_main['Date'] = pd.to_datetime(df_main['Date'], utc=True).dt.date
    
    # Initialisation des colonnes cibles
    df_main['sentiment_score'] = 0.0
    df_main['has_sentiment'] = 0

    # 3. PARCOURS DES FICHIERS DE NEWS
    news_files = [f for f in os.listdir(PATH_TO_NEWS_FOLDER) if f.endswith('.csv')]
    
    all_daily_scores = []

    for filename in news_files:
        ticker = filename.split('_')[0]
        print(f"\n--- Analyse FinBERT pour : {ticker} ---")
        
        df_news = pd.read_csv(os.path.join(PATH_TO_NEWS_FOLDER, filename))
        # Nettoyage des dates (Alpha Vantage format)
        df_news['Date'] = pd.to_datetime(df_news['time_published'], utc=True).dt.date
        
        # On suppose que le texte de l'article est dans une colonne 'content' ou 'title'
        # Adaptez le nom de la colonne si nécessaire
        text_column = 'content' if 'content' in df_news.columns else 'title'
        
        # Traitement par batch pour la rapidité (32 articles à la fois)
        batch_size = 32
        scores = []
        
        texts = df_news[text_column].astype(str).tolist()
        for i in tqdm(range(0, len(texts), batch_size)):
            batch_texts = texts[i:i+batch_size]
            batch_scores = get_sentiment_probabilities(batch_texts)
            scores.extend(batch_scores)
            
        df_news['sentiment_net'] = scores
        
        # Moyenne quotidienne par ticker
        daily_res = df_news.groupby('Date')['sentiment_net'].mean().reset_index()
        daily_res['ticker'] = ticker
        all_daily_scores.append(daily_res)

    # 4. FUSION FINALE
    if all_daily_scores:
        df_all_sentiment = pd.concat(all_daily_scores)
        
        print("\nFusion des scores avec le dataset principal...")
        # On fusionne sur Date et Ticker
        df_main = pd.merge(
            df_main, 
            df_all_sentiment, 
            on=['Date', 'ticker'], 
            how='left',
            suffixes=('', '_new')
        )
        
        # Remplissage des colonnes avec la logique "Expert Flag"
        mask = df_main['sentiment_net'].notna()
        df_main.loc[mask, 'sentiment_score'] = df_main.loc[mask, 'sentiment_net']
        df_main.loc[mask, 'has_sentiment'] = 1
        
        # Suppression de la colonne temporaire
        df_main = df_main.drop(columns=['sentiment_net'])

    # 5. SAUVEGARDE
    print(f"Sauvegarde du dataset enrichi dans {OUTPUT_FILE}...")
    df_main.to_csv(OUTPUT_FILE, index=False)
    print("Terminé !")

if __name__ == "__main__":
    process_all_news()