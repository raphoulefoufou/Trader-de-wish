import pandas as pd

# 1. Chargement du dataset (v7)
df = pd.read_csv('datasetv6_sentiment.csv')
df['Date'] = pd.to_datetime(df['Date'], utc=True)
df = df.sort_values(['ticker', 'Date'])

# 2. Calcul de la Moyenne Mobile (Trend)
# Nous utilisons une fenêtre de 7 jours pour capturer la "tendance de la semaine"
window = 7

print("Calcul de la tendance du sentiment (EMA 7 jours)...")

# On groupe par ticker pour que la moyenne d'une entreprise ne bave pas sur une autre
df['sentiment_trend'] = df.groupby('ticker')['sentiment_score'].transform(
    lambda x: x.ewm(span=window, adjust=False).mean()
)


# 4. Sauvegarde
output_file = 'datasetv6_sentiment_trend.csv'
df.to_csv(output_file, index=False)
print(f"Nouveau dataset sauvegardé : {output_file}")