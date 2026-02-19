from dec_rendbrut import builder_uni as bu #Classe de construction
import yfinance as yf 
import pandas as pd
from tqdm import tqdm #pour voir où en est de la création du dataset

tickers = [
    "AAPL",    # Apple
    "MSFT",    # Microsoft
    "NVDA",    # NVIDIA
    "GOOGL",   # Alphabet (Google)
    "AMZN",    # Amazon
    "META",    # Meta (Facebook)
    "005930.KS",  # Samsung Electronics
    "TCEHY",   # Tencent
    "BABA",    # Alibaba
    "TSM",     # TSMC
    "AVGO",    # Broadcom
    "TSLA",    # Tesla
    "INTC",    # Intel
    "SAP",     # SAP
    "CRM",     # Salesforce
    "ADBE",    # Adobe
    "QCOM",    # Qualcomm
    "AMD",     # AMD
    "ORCL",    # Oracle
    "CSCO",    # Cisco
    "DELL",    # Dell
    "HPQ",     # HP
    "0992.HK", # Lenovo
    "SONY",    # Sony
    "066570.KS", # LG Electronics
    "MU",      # Micron
    "000660.KS", # SK Hynix
    "1810.HK", # Xiaomi
    "UBER",    # Uber
    "ZM",      # Zoom
    "SHOP",    # Shopify
    "EBAY",    # eBay
    "PYPL",    # PayPal
    "TEAM",    # Atlassian
    "DBX",     # Dropbox
    "WDAY",    # Workday
    "OKTA",    # Okta
    "PDD",     # Pinduoduo
    "BIDU",    # Baidu
    "0763.HK"  # ZTE
]

datasets = []

for ticker in tqdm(tickers, desc="Construction des datasets"):
    try:
        builder = bu(ticker)
        df = builder.launch()
        df["ticker"] = ticker
        datasets.append(df)
    except Exception as e:
        print(f"Erreur avec {ticker}: {e}") #si il y a un problème ne stop pas tout le processus


final_dataset = pd.concat(datasets)
final_dataset = final_dataset.dropna() #On enlève les lignes avec des valeurs manquantes 


final_dataset.reset_index().to_csv(
    "datasetv3.csv",
    index=False,
    float_format="%.6f"
)

print("Dataset exporté : dataset_tech_4j.csv")
print("Shape :", final_dataset.shape)
print(final_dataset.head())        