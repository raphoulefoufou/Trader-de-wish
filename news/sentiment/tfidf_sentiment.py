import os
import csv
import json
import re
import math
import random

def train_and_test_tfidf(dataset_path="sentiment_equilibre.csv", split_ratio=0.9):
    # 1. Chargement des stopwords
    stopwords = []
    stopwords_path = "stopwords-en.txt"
    if os.path.exists(stopwords_path):
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            stopwords = f.read().splitlines()

    def pretraitement(texte):
        texte = str(texte).lower()
        texte_nettoye = re.sub(r'[^\w\s]', ' ', texte)
        mots = texte_nettoye.split()
        return [mot for mot in mots if mot not in stopwords]

    # Mapping des labels
    label_map = {"negative": -1, "neutral": 0, "positive": 1}

    if not os.path.exists(dataset_path):
        print(f"Erreur : {dataset_path} introuvable.")
        return

    # 2. Chargement des données avec les en-têtes Sentence et Sentiment
    data = []
    with open(dataset_path, encoding="utf-8") as f:
        # Utilisation de DictReader pour lire via les noms de colonnes
        reader = csv.DictReader(f)
        for row in reader:
            # Adaptation aux nouveaux noms de colonnes
            label_str = row['Sentiment'].strip().lower()
            content = row['Sentence']
            
            if label_str in label_map:
                data.append((content, label_map[label_str]))

    # 3. Mélange et Séparation
    random.seed(74) 
    random.shuffle(data)
    
    split_idx = int(len(data) * split_ratio)
    train_data = data[:split_idx]
    test_data = data[split_idx:]

    print(f"Total : {len(data)} | Entraînement : {len(train_data)} | Test : {len(test_data)}")

    # ÉTAPE D'ENTRAÎNEMENT (sur train_data)
    train_textes = [d[0] for d in train_data]
    train_labels = [d[1] for d in train_data]

    N = len(train_textes)
    df = {}
    for texte in train_textes:
        mots_uniques = set(pretraitement(texte))
        for mot in mots_uniques:
            df[mot] = df.get(mot, 0) + 1

    idf = {mot: math.log(N / nombre) for mot, nombre in df.items()}
    score_map = {mot: 0.0 for mot in idf.keys()}

    for texte, label in zip(train_textes, train_labels):
        mots = pretraitement(texte)
        if not mots: continue
        tf = {}
        for mot in mots:
            tf[mot] = tf.get(mot, 0) + 1
        for mot, freq in tf.items():
            score_tf_idf = (freq / len(mots)) * idf[mot]
            score_map[mot] += score_tf_idf * label

    # Sauvegarde du lexique
    with open("sentiment_score_map.json", "w", encoding="utf-8") as f:
        json.dump(score_map, f, ensure_ascii=False)

    # ÉTAPE DE TEST (sur test_data)
    correct = 0
    
    for texte, true_label in test_data:
        mots = pretraitement(texte)
        score_total = 0
        for mot in mots:
            if mot in score_map:
                score_total += score_map[mot]
        
        # Prédiction
        if score_total > 1:   # Seuil positif
            pred_label = 1
        elif score_total < -1: # Seuil négatif
            pred_label = -1
        else:
            pred_label = 0        # Neutre
            
        if pred_label == true_label:
            correct += 1

    accuracy = (correct / len(test_data)) * 100
    print("-" * 30)
    print(f"Précision du modèle TF-IDF : {accuracy:.2f}%")

if __name__ == "__main__":
    train_and_test_tfidf(dataset_path="sentiment_equilibre.csv")