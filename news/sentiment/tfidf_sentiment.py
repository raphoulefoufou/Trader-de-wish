import os
import csv
import json
import re
import math
import random
import matplotlib.pyplot as plt
import seaborn as sns

def train_and_test_tfidf(dataset_path="sentiment_equilibre.csv", split_ratio=0.9):
    # 1. Chargement des stopwords
    stopwords = []
    stopwords_path = "news/sentiment/stopwords-en.txt"
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
    with open("news/sentiment/sentiment_score_map.json", "w", encoding="utf-8") as f:
        json.dump(score_map, f, ensure_ascii=False)

    # ÉTAPE DE TEST (sur test_data)
    # Initialisation de la matrice 3x3 (lignes = réel, colonnes = prédit)
    cm = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # Index 0: -1 (Neg), Index 1: 0 (Neu), Index 2: 1 (Pos)
    idx_map = {-1: 0, 0: 1, 1: 2}
    
    for texte, true_label in test_data:
        mots = pretraitement(texte)
        score_total = sum(score_map.get(mot, 0) for mot in mots)
        
        # Prédiction
        if score_total > 5:   # Seuil positif
            pred_label = 1
        elif score_total < -5: # Seuil négatif
            pred_label = -1
        else:
            pred_label = 0        # Neutre
            
        cm[idx_map[true_label]][idx_map[pred_label]] += 1

    # Calcul des métriques
    total_samples = len(test_data)
    correct_total = cm[0][0] + cm[1][1] + cm[2][2]
    accuracy = (correct_total / total_samples) * 100

    def calculate_metrics(class_idx):
        true_pos = cm[class_idx][class_idx]
        false_pos = sum(cm[row][class_idx] for row in range(3)) - true_pos
        false_neg = sum(cm[class_idx][col] for col in range(3)) - true_pos
        
        precision = true_pos / (true_pos + false_pos) if (true_pos + false_pos) > 0 else 0
        recall = true_pos / (true_pos + false_neg) if (true_pos + false_neg) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return precision, recall, f1

    # Affichage des résultats
    print("\nMATRICE DE CONFUSION :")
    labels_names = ["Négatif", "Neutre", "Positif"]
    header = f"{'Réel \\ Prédit':<15} | " + " | ".join([f"{name:<10}" for name in labels_names])
    print(header)
    print("-" * len(header))
    for i, name in enumerate(labels_names):
        row_content = " | ".join([f"{val:<10}" for val in cm[i]])
        print(f"{name:<15} | {row_content}")
    print("\n")

    print("-" * 40)
    print(f"{'Classe':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("-" * 40)
    
    labels_names = ["Négatif", "Neutre", "Positif"]
    for i, name in enumerate(labels_names):
        p, r, f = calculate_metrics(i)
        print(f"{name:<10} | {p:<10.2f} | {r:<10.2f} | {f:<10.2f}")

    print("-" * 40)
    print(f"Accuracy du modèle TF-IDF : {accuracy:.2f}%")

    # Visualisation
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels_names, yticklabels=labels_names)
    plt.title('Matrice de Confusion')
    plt.ylabel('Réalité')
    plt.xlabel('Prédictions')
    plt.savefig("news/sentiment/confusion_matrix.png")

if __name__ == "__main__":
    train_and_test_tfidf(dataset_path="news/sentiment/sentiment_equilibre.csv")