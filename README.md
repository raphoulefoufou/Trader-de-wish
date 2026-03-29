# 📈 Trading for sure : Algorithmique Boursière

    Système d'aide à la décision boursière basé sur l'analyse technique profonde et l'intelligence artificielle.

Trading for sure est un projet de finance quantitative visant à prédire les mouvements directionnels du marché. Le cœur du projet repose sur une exploitation des indicateurs techniques, complétée par une analyse de sentiment sémantique pour capter l'humeur des marchés.

## 🛠 Architecture des Données

La force du projet réside dans la transformation des données brutes (OHLCV) en un ensemble de features expertes. Nous avons priorisé l'analyse quantitative pour fournir une base solide à nos modèles.
### 1. Indicateurs Techniques Avancés

Le dataset intègre plus de 15 variables techniques calculées sur un historique de 8 ans (2018-2026) :

* Momentum : RSI (4 et 14 jours) pour détecter les zones de surachat/survente.

* Suivi de Tendance : Moyennes Mobiles Simples (SMA 20 et 50) et MACD (12, 26, 9).

* Volatilité : Average True Range (ATR 4 et 14) pour mesurer l'expansion du risque.

* Volume : Volume normalisé sur 20 jours pour identifier la force des mouvements.

* Rendements : Calcul des rendements bruts sur plusieurs horizons (1j, 4j, 1s, 2s).

### 2. Indices de Conviction "Experts"

Nous avons développé des colonnes composites pour aider les modèles à identifier les régimes de marché :

* Bullish Index : Score combiné (tendance SMA + Momentum RSI + MACD haussier).

* Bearish Index : Score inverse détectant la pression vendeuse.

## 🤖 Benchmark des Modèles d'IA

L'objectif central de ce projet est de réaliser une étude comparative des performances de différentes architectures pour déterminer laquelle offre l'avantage statistique le plus élevé.

Nous comparons les modèles suivants sur les mêmes jeux de données :

* Modèles Linéaires : Régression Linéaire Multiple (Baseline).

* Ensembles d'Arbres : Random Forest, Decision Tree (Random Tree).

* Gradient Boosting (SOTA) : LightGBM, CatBoost, XGBoost.

* Deep Learning : Réseaux de neurones Fully Connected (FCNN).



Bien que le projet soit piloté par la technique, nous intégrons une dimension sémantique via le Deep Learning :

* NLP : Utilisation de FinBERT pour scorer les news financières journalières.

## 📊 Protocole d'Évaluation

* Période : 2018 - 2026.

* Validation : Rolling Window (7 ans d'entraînement / 1 an de test glissant).

* Tickers : 40 actifs.

* Cibles : Prédiction de la direction du rendement à 1j, 4j, 1 semaine et 2 semaines.


## 👥 Composition du Groupe
Le projet est réalisé par :
* **Alexandre Aboubakar**
* **Albert Bednarz**
* **Raphael Capristo**
* **Théo Sales**

---
*Ce projet est réalisé dans un cadre académique et ne constitue pas un conseil en investissement.*