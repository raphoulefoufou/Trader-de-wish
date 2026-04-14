import yfinance as yf
import pandas as pd
import pandas_ta as ta


class builder_uni():
    def __init__(self, name):
        ticker = yf.Ticker(name)
        self.historique = ticker.history(period="8y").reset_index()
        self.historique_anterieur = ticker.history(period="9y").reset_index()

        self.historique_anterieur["RSI_14"] = ta.rsi(self.historique_anterieur["Close"], length=14)
        self.historique_anterieur["RSI_4"]  = ta.rsi(self.historique_anterieur["Close"], length=4)

        self.historique_anterieur["ATR_14"] = ta.atr(
            high=self.historique_anterieur["High"],
            low=self.historique_anterieur["Low"],
            close=self.historique_anterieur["Close"],
            length=14)
        self.historique_anterieur["ATR_4"] = ta.atr(
            high=self.historique_anterieur["High"],
            low=self.historique_anterieur["Low"],
            close=self.historique_anterieur["Close"],
            length=4)  # corrigé : était "lenght"

        macd = ta.macd(self.historique_anterieur["Close"], fast=12, slow=26, signal=9)
        self.historique_anterieur = pd.concat(
            [self.historique_anterieur, macd],
            axis=1)

        self.historique_anterieur["SMA_20"] = ta.sma(self.historique_anterieur["Close"], length=20)
        self.historique_anterieur["SMA_50"] = ta.sma(self.historique_anterieur["Close"], length=50)

        self.historique_anterieur["Rendement_14"] = self.historique_anterieur["Close"].pct_change(14)
        self.historique_anterieur["Rendement_4"]  = self.historique_anterieur["Close"].pct_change(4)

        self.historique_anterieur["SMA_Volume_20"]  = ta.sma(self.historique_anterieur["Volume"], length=20)
        self.historique_anterieur["Volume_norm_20"] = (
            self.historique_anterieur["Volume"] / self.historique_anterieur["SMA_Volume_20"])

    def launch(self):
        histo_filtered = pd.merge(
            self.historique,
            self.historique_anterieur[[
                "Date",
                "RSI_14",
                "RSI_4",
                "ATR_14",
                "ATR_4",
                "MACD_12_26_9",
                "MACDs_12_26_9",
                "MACDh_12_26_9",
                "SMA_20",
                "SMA_50",
                "Rendement_14",
                "Rendement_4",
                "Volume_norm_20",
            ]],
            on="Date",
            how="left",
        )

        close = histo_filtered["Close"]

        histo_filtered["decision(rendement_brut_1j)"]  = (close.shift(-1)  - close) / close
        histo_filtered["decision(rendement_brut_4j)"]  = (close.shift(-4)  - close) / close
        histo_filtered["decision(rendement_brut_1s)"]  = (close.shift(-7)  - close) / close
        histo_filtered["decision(rendement_brut_2s)"]  = (close.shift(-14) - close) / close

        histo_filtered = histo_filtered.iloc[:-14].reset_index(drop=True)

        return histo_filtered