import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("datasetv3.csv")

decision = data["decision"]

variables = [
    "RSI(4)", "RSI(14)", "rendement(4)", "rendement(14)",
    "MACD", "ATR(4)", "ATR(14)",
    "SMA(20)", "SMA(50)",
    "Ratio[SMA(20)/SMA(50)]",
    "Volume_norm(20)"
]

plt.figure(figsize=(15, 10))

for i, var in enumerate(variables):
    plt.subplot(4, 3, i+1)  # 4 lignes, 3 colonnes
    plt.scatter(data[var], decision)
    plt.xlabel(var)
    plt.ylabel("decision")

plt.tight_layout()
plt.show()
