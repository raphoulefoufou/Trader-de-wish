import sys
import os
import joblib
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import warnings

warnings.filterwarnings("ignore")

def make_prediction(symbol):
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_path, 'xgb_model_2s.pkl')
        
        data_loaded = joblib.load(model_path)

        if isinstance(data_loaded, dict) and 'model' in data_loaded:
            model = data_loaded['model']
        else:
            model = data_loaded

        ticker = yf.Ticker(symbol)
        df = ticker.history(period="6mo")

        if df.empty or len(df) < 55:
            return f"Erreur : Pas assez de données historiques pour {symbol}."

        # Features
        df['RSI_14'] = ta.rsi(df['Close'], length=14)
        df['RSI_4'] = ta.rsi(df['Close'], length=4)
        df['ATR_14'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
        df['ATR_4'] = ta.atr(df['High'], df['Low'], df['Close'], length=4)
        macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
        df['MACD_12_26_9'] = macd['MACD_12_26_9']
        df['MACDs_12_26_9'] = macd['MACDs_12_26_9']
        df['MACDh_12_26_9'] = macd['MACDh_12_26_9']
        df['SMA_20'] = ta.sma(df['Close'], length=20)
        df['SMA_50'] = ta.sma(df['Close'], length=50)
        df['Rendement_14'] = df['Close'].pct_change(14)
        df['Rendement_4'] = df['Close'].pct_change(4)
        df['Volume_norm_20'] = df['Volume'] / ta.sma(df['Volume'], length=20)

        FEATURES = [
            'RSI_14', 'RSI_4', 'ATR_14', 'ATR_4',
            'MACD_12_26_9', 'MACDs_12_26_9', 'MACDh_12_26_9',
            'SMA_20', 'SMA_50', 'Rendement_14', 'Rendement_4',
            'Volume_norm_20'
        ]

        last_row = df[FEATURES].tail(1)

        if last_row.isnull().values.any():
            return "Erreur : Indicateurs NaN. Reessayez."

        prediction_code = model.predict(last_row)[0]
        
        try:
            prob = model.predict_proba(last_row)[0][1]
            confiance = f"{prob*100:.1f}%"
        except:
            confiance = "N/A"

        # ON UTILISE DU TEXTE SIMPLE ICI (Pas d'emojis)
        resultat = "HAUSSIER" if prediction_code == 1 else "BAISSIER"
        dernier_prix = df['Close'].iloc[-1]

        return f"{resultat} (Confiance : {confiance}) - Dernier cours : {dernier_prix:.2f}$"

    except Exception as e:
        return f"Erreur IA : {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ticker_to_predict = sys.argv[1]
        # On force l'encodage de sortie en UTF-8 pour être sûr
        sys.stdout.reconfigure(encoding='utf-8') 
        print(make_prediction(ticker_to_predict))