# Commentez ces lignes si vous n'avez pas de contrainte de stockage ou de téléchargement, sinon assurez-vous que le chemin est correct et accessible
import os
# Définir le cache Hugging Face pour éviter les problèmes de téléchargement et de stockage

from flask import Flask, request, render_template, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import feedparser
import urllib.parse
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

print("Chargement de FinBERT en mémoire (patientez)...")
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
print("Modèle chargé !")

def get_exchange_rate(from_currency):
    """Récupère le taux de change pour convertir vers l'Euro"""
    if from_currency == 'EUR':
        return 1.0
    try:
        ticker_pair = f"{from_currency}EUR=X"
        data = yf.Ticker(ticker_pair)
        return data.fast_info['last_price']
    except:
        rates = {"USD": 0.92, "HKD": 0.12, "KRW": 0.00069}
        return rates.get(from_currency, 1.0)

def get_google_news_headlines(ticker, max_results=10):
    query = urllib.parse.quote(f"{ticker} stock news")
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    headlines = []
    for entry in feed.entries[:max_results]:
        clean_title = entry.title.rsplit(' - ', 1)[0]
        headlines.append(clean_title)
    return headlines

def get_sentiment_score(headlines):
    if not headlines:
        return 0.0
    inputs = tokenizer(headlines, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    pos_probs = predictions[:, 0].numpy()
    neg_probs = predictions[:, 1].numpy()
    scores = pos_probs - neg_probs
    return float(scores.mean())

# --- Route utilisée par server.js (Express) ---
@app.route('/api/sentiment')
def api_sentiment():
    """Retourne le score FinBERT + les titres d'articles en JSON."""
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return jsonify({"error": "Paramètre ticker manquant"}), 400
    try:
        headlines = get_google_news_headlines(ticker)
        if not headlines:
            return jsonify({"error": "Aucune actualité trouvée pour " + ticker}), 404
        score = get_sentiment_score(headlines)
        return jsonify({
            "ticker": ticker,
            "score": round(score, 4),
            "headlines": headlines
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Route HTML pour l'interface Flask autonome (inchangée) ---
@app.route('/')
def index():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return render_template('index.html', ticker=None)
    try:
        headlines = get_google_news_headlines(ticker)
        if not headlines:
            return render_template('index.html', ticker=ticker, error="Aucune actualité trouvée.")
        score = get_sentiment_score(headlines)
        position_pourcentage = ((score + 1) / 2) * 100
        score_arrondi = round(score, 2)
        return render_template('index.html',
                               ticker=ticker,
                               score=score_arrondi,
                               position=position_pourcentage,
                               headlines=headlines)
    except Exception as e:
        return render_template('index.html', ticker=ticker, error=str(e))

@app.route('/api/prix')
def get_prix_actuel():
    ticker_symbol = request.args.get('ticker').upper()
    try:
        stock = yf.Ticker(ticker_symbol)
        prix_origine = stock.fast_info['last_price']
        devise = stock.fast_info['currency']
        taux = get_exchange_rate(devise)
        prix_euros = prix_origine * taux
        return jsonify({
            "ticker": ticker_symbol,
            "prix_origine": round(prix_origine, 2),
            "devise_origine": devise,
            "prix_eur": round(prix_euros, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
