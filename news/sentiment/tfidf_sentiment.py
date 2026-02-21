import os
import csv
import json
import re
import math
import random
import matplotlib.pyplot as plt
import seaborn as sns

def train_and_test_tfidf(dataset_path, k):
    # Chargement des stopwords
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

    # Chargement des données avec les en-têtes Sentence et Sentiment
    data = []
    with open(dataset_path, encoding="utf-8") as f:
        # Utilisation de DictReader pour lire via les noms de colonnes
        reader = csv.DictReader(f)
        for row in reader:
            label_str = row['Sentiment'].strip().lower()
            content = row['Sentence']
            
            if label_str in label_map:
                data.append((content, label_map[label_str]))

    # Mélange initial
    random.seed(47) 
    random.shuffle(data)
    
    # Préparation du K-Fold
    fold_size = len(data) // k
    accuracies = []
    # Initialisation de la matrice 3x3 (lignes = réel, colonnes = prédit)
    cm_globale = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # Index 0: -1 (Neg), Index 1: 0 (Neu), Index 2: 1 (Pos)
    idx_map = {-1: 0, 0: 1, 1: 2}

    print(f"Démarrage de la validation croisée (K={k}) sur {len(data)} articles...")

    for fold in range(k):
        # Découpage train/test pour ce pli
        start, end = fold * fold_size, (fold + 1) * fold_size
        test_data = data[start:end]
        train_data = data[:start] + data[end:]

        # PHASE D'ENTRAÎNEMENT DU PLI
        train_textes = [d[0] for d in train_data]
        train_labels = [d[1] for d in train_data]
        N = len(train_textes)
        
        # Calcul IDF spécifique au set d'entraînement actuel
        df_count = {}
        for texte in train_textes:
            for mot in set(pretraitement(texte)):
                df_count[mot] = df_count.get(mot, 0) + 1

        idf = {mot: math.log(N / nombre) for mot, nombre in df_count.items()}
        score_map = {mot: 0.0 for mot in idf.keys()}

        for texte, label in zip(train_textes, train_labels):
            mots = pretraitement(texte)
            if not mots: continue
            tf = {}
            for mot in mots: tf[mot] = tf.get(mot, 0) + 1
            for mot, freq in tf.items():
                score_map[mot] += (freq / len(mots)) * idf[mot] * label

        # PHASE DE TEST DU PLI
        correct_fold = 0
        for texte, true_label in test_data:
            mots = pretraitement(texte)
            score_total = sum(score_map.get(mot, 0) for mot in mots)
            
            # Prédiction
            if score_total > 5:     #seuil positif
                pred_label = 1
            elif score_total < -5: 
                pred_label = -1     #seuil négatif
            else: 
                pred_label = 0      #neutre
                
            cm_globale[idx_map[true_label]][idx_map[pred_label]] += 1
            if pred_label == true_label:
                correct_fold += 1
        
        acc_fold = (correct_fold / len(test_data)) * 100
        accuracies.append(acc_fold)
        print(f"  Fold {fold + 1} : Accuracy = {acc_fold:.2f}%")

    # Calcul des métriques finales (moyennes)
    moyenne_acc = sum(accuracies) / k
    
    def calculate_metrics(class_idx, matrix):
        true_pos = matrix[class_idx][class_idx]
        false_pos = sum(matrix[row][class_idx] for row in range(3)) - true_pos
        false_neg = sum(matrix[class_idx][col] for col in range(3)) - true_pos
        precision = true_pos / (true_pos + false_pos) if (true_pos + false_pos) > 0 else 0
        recall = true_pos / (true_pos + false_neg) if (true_pos + false_neg) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return precision, recall, f1

    # Affichage des résultats
    print("\n" + "="*60)
    print("MATRICE DE CONFUSION CUMULÉE")
    print("="*60)
    labels_names = ["Négatif", "Neutre", "Positif"]
    header = f"{'Réel \\\\ Prédit':<15} | " + " | ".join([f"{name:<10}" for name in labels_names])
    print(header)
    print("-" * len(header))
    for i, name in enumerate(labels_names):
        row_content = " | ".join([f"{val:<10}" for val in cm_globale[i]])
        print(f"{name:<15} | {row_content}")
    
    print("\n" + "="*30)
    print(f"RÉSULTATS FINAUX (MOYENNE SUR {k} FOLDS)")
    print("="*30)
    labels_names = ["Négatif", "Neutre", "Positif"]
    print(f"{'Classe':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("-" * 45)
    for i, name in enumerate(labels_names):
        precision, recall, f = calculate_metrics(i, cm_globale)
        print(f"{name:<10} | {precision:<10.2f} | {recall:<10.2f} | {f:<10.2f}")
    
    print("-" * 45)
    print(f"Accuracy Moyenne Globale : {moyenne_acc:.2f}%")

    # Visualisation
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm_globale, annot=True, fmt='d', cmap='Blues', xticklabels=labels_names, yticklabels=labels_names)
    plt.title(f'Matrice de Confusion Cumulée (K-Fold, K={k})')
    plt.ylabel('Réalité')
    plt.xlabel('Prédictions')
    plt.savefig("news/sentiment/confusion_matrix_tfidf.png")

    # GÉNÉRATION DU MODÈLE FINAL
    print("\nGénération du lexique final sur 100% des données...")
    N_final = len(data)
    df_final = {}
    for texte, _ in data:
        for mot in set(pretraitement(texte)):
            df_final[mot] = df_final.get(mot, 0) + 1

    idf_final = {mot: math.log(N_final / count) for mot, count in df_final.items()}
    score_map_final = {mot: 0.0 for mot in idf_final.keys()}

    for texte, label in data:
        mots = pretraitement(texte)
        if not mots: continue
        tf = {}
        for mot in mots: tf[mot] = tf.get(mot, 0) + 1
        for mot, freq in tf.items():
            score_map_final[mot] += (freq / len(mots)) * idf_final[mot] * label

    # Sauvegarde finale pour utilisation sur les tickers
    with open("news/sentiment/sentiment_score_map.json", "w", encoding="utf-8") as f:
        json.dump(score_map_final, f, ensure_ascii=False)
    print("Modèle sauvegardé dans news/sentiment/sentiment_score_map.json")

if __name__ == "__main__":
    train_and_test_tfidf(dataset_path="news/sentiment/sentiment_equilibre.csv", k=10)