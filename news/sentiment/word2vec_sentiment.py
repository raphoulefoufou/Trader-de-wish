import os
import csv
import re
import random
import numpy as np
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

def train_and_test_word2vec(dataset_path, k):
    # Prétraitement
    stopwords = []
    stopwords_path = "news/sentiment/stopwords-en.txt"
    if not os.path.exists(stopwords_path):
        print(f"Erreur : {stopwords_path} introuvable")
        return
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        stopwords = f.read().splitlines()

    def pretraitement(texte):
        texte = str(texte).lower()
        texte_nettoye = re.sub(r'[^\w\s]', ' ', texte)
        mots = texte_nettoye.split()
        return [mot for mot in mots if mot not in stopwords]

    label_map = {"negative": -1, "neutral": 0, "positive": 1}
    
    # Chargement des données
    if not os.path.exists(dataset_path):
        print(f"Erreur : {dataset_path} introuvable")
        return
    data = []
    with open(dataset_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            label_str = row['Sentiment'].strip().lower()
            if label_str in label_map:
                data.append((pretraitement(row['Sentence']), label_map[label_str]))

    # Mélange identique aux tests précédents
    random.seed(47) 
    random.shuffle(data)
    
    # Préparation du K-Fold
    fold_size = len(data) // k
    accuracies = []
    cm_globale = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    idx_map = {-1: 0, 0: 1, 1: 2} 

    print(f"Démarrage de l'évaluation Word2Vec (K-Fold, K={k}) sur {len(data)} articles...")

    for fold in range(k):
        start, end = fold * fold_size, (fold + 1) * fold_size
        test_data = data[start:end]
        train_data = data[:start] + data[end:]

        # A. Entraînement Word2Vec sur le set de train
        sentences_train = [d[0] for d in train_data]
        w2v_model = Word2Vec(sentences=sentences_train, vector_size=100, window=5, min_count=1, workers=4)

        # B. Vectorisation des phrases (Moyenne des vecteurs de mots)
        def get_sentence_vector(mots, model):
            vecteurs = [model.wv[mot] for mot in mots if mot in model.wv]
            if len(vecteurs) > 0:
                return np.mean(vecteurs, axis=0)
            else:
                return np.zeros(model.vector_size)

        X_train = np.array([get_sentence_vector(d[0], w2v_model) for d in train_data])
        y_train = np.array([d[1] for d in train_data])
        X_test = np.array([get_sentence_vector(d[0], w2v_model) for d in test_data])
        y_test = np.array([d[1] for d in test_data])

        # C. Classification (Régression Logistique)
        classifier = LogisticRegression(max_iter=1000)
        classifier.fit(X_train, y_train)

        # D. Prédictions et accumulation pour la matrice
        preds = classifier.predict(X_test)
        for true, pred in zip(y_test, preds):
            cm_globale[idx_map[true]][idx_map[pred]] += 1
        
        acc_fold = (preds == y_test).mean() * 100
        accuracies.append(acc_fold)
        print(f"  Fold {fold + 1} : Accuracy = {acc_fold:.2f}%")

    # AFFICHAGE DES RÉSULTATS
    labels_names = ["Négatif", "Neutre", "Positif"]
    print("\n" + "="*60)
    print("MATRICE DE CONFUSION CUMULÉE : WORD2VEC")
    print("="*60)
    header = f"{'Réel \\\\ Prédit':<15} | " + " | ".join([f"{name:<10}" for name in labels_names])
    print(header)
    print("-" * len(header))
    for i, name in enumerate(labels_names):
        row_content = " | ".join([f"{val:<10}" for val in cm_globale[i]])
        print(f"{name:<15} | {row_content}")

    def calculate_metrics(class_idx, matrix):
        true_pos = matrix[class_idx][class_idx]
        false_pos = sum(matrix[row][class_idx] for row in range(3)) - true_pos
        false_neg = sum(matrix[class_idx][col] for col in range(3)) - true_pos
        precision = true_pos / (true_pos + false_pos) if (true_pos + false_pos) > 0 else 0
        recall = true_pos / (true_pos + false_neg) if (true_pos + false_neg) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return precision, recall, f1

    print("\n" + "="*60)
    print(f"RÉSULTATS FINAUX WORD2VEC (MOYENNE SUR {k} FOLDS)")
    print("="*60)
    print(f"{'Classe':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("-" * 45)
    for i, name in enumerate(labels_names):
        precision, recall, f = calculate_metrics(i, cm_globale)
        print(f"{name:<10} | {precision:<10.2f} | {recall:<10.2f} | {f:<10.2f}")
    
    print("-" * 45)
    print(f"Accuracy Moyenne Globale : {np.mean(accuracies):.2f}%")
    print("="*60 + "\n")

    # Sauvegarde graphique
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm_globale, annot=True, fmt='d', cmap='Oranges', xticklabels=labels_names, yticklabels=labels_names)
    plt.title(f'Matrice de Confusion Word2Vec (K-Fold, K={k})')
    plt.ylabel('Réalité')
    plt.xlabel('Prédictions')
    plt.savefig("news/sentiment/confusion_matrix_word2vec.png")

    #Génération du modèle final
    print("\nEntraînement final du modèle sur 100% du dataset...")
    
    # A. Préparation de l'intégralité des news
    all_sentences = [d[0] for d in data]
    all_labels = np.array([d[1] for d in data])
    
    # B. Création du Word2Vec final
    w2v_final = Word2Vec(sentences=all_sentences, vector_size=100, window=5, min_count=1, workers=4)
    
    # C. Vectorisation de toutes les news
    X_all = np.array([get_sentence_vector(d[0], w2v_final) for d in data])
    
    # D. Entraînement du classifieur final
    classifier_final = LogisticRegression(max_iter=1000)
    classifier_final.fit(X_all, all_labels)
    
    # E. Sauvegarde
    w2v_final.save("news/sentiment/w2v_modele.model")
    joblib.dump(classifier_final, "news/sentiment/w2v_classifier.joblib")
    print("Modèle Word2Vec final (w2v_modele.model) et classifieur (w2v_classifier.joblib) sauvegardés dans news/sentiment/")

if __name__ == "__main__":
    train_and_test_word2vec(dataset_path="news/sentiment/sentiment_equilibre.csv", k=10)