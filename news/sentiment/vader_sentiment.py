import os
import csv
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

def train_and_test_vader(dataset_path, k):
    # Initialisation de l'analyseur VADER
    analyzer = SentimentIntensityAnalyzer()
    
    # Mapping des labels pour la comparaison
    label_map = {"negative": -1, "neutral": 0, "positive": 1}

    if not os.path.exists(dataset_path):
        print(f"Erreur : {dataset_path} introuvable.")
        return

    # Chargement des données
    data = []
    with open(dataset_path, encoding="utf-8") as f:
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
    cm_globale = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    idx_map = {-1: 0, 0: 1, 1: 2}

    print(f"Démarrage de l'évaluation VADER (K-Fold, K={k}) sur {len(data)} articles...")

    for fold in range(k):
        # Découpage train/test (Même répartition)
        start, end = fold * fold_size, (fold + 1) * fold_size
        test_data = data[start:end]

        # PHASE DE TEST (VADER n'a pas besoin d'entraînement)
        correct_fold = 0
        for texte, true_label in test_data:
            # VADER utilise le texte brut pour capter la ponctuation/majuscules
            vs = analyzer.polarity_scores(texte)
            compound = vs['compound']
            
            # Seuils standards de VADER
            if compound >= 0.05:
                pred_label = 1
            elif compound <= -0.05:
                pred_label = -1
            else:
                pred_label = 0
                
            cm_globale[idx_map[true_label]][idx_map[pred_label]] += 1
            if pred_label == true_label:
                correct_fold += 1
        
        acc_fold = (correct_fold / len(test_data)) * 100
        accuracies.append(acc_fold)
        print(f"  Fold {fold + 1} : Accuracy = {acc_fold:.2f}%")

    # AFFICHAGE DE LA MATRICE DE CONFUSION GLOBALE
    print("\n" + "="*60)
    print("MATRICE DE CONFUSION CUMULÉE : VADER")
    print("="*60)
    labels_names = ["Négatif", "Neutre", "Positif"]
    header = f"{'Réel \\\\ Prédit':<15} | " + " | ".join([f"{name:<10}" for name in labels_names])
    print(header)
    print("-" * len(header))
    for i, name in enumerate(labels_names):
        row_content = " | ".join([f"{val:<10}" for val in cm_globale[i]])
        print(f"{name:<15} | {row_content}")

    # CALCUL DES MÉTRIQUES FINALES
    def calculate_metrics(class_idx, matrix):
        true_pos = matrix[class_idx][class_idx]
        false_pos = sum(matrix[row][class_idx] for row in range(3)) - true_pos
        false_neg = sum(matrix[class_idx][col] for col in range(3)) - true_pos
        precision = true_pos / (true_pos + false_pos) if (true_pos + false_pos) > 0 else 0
        recall = true_pos / (true_pos + false_neg) if (true_pos + false_neg) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return precision, recall, f1

    print("\n" + "="*30)
    print(f"RÉSULTATS FINAUX VADER (MOYENNE SUR {k} FOLDS)")
    print("="*30)
    print(f"{'Classe':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("-" * 45)
    for i, name in enumerate(labels_names):
        p, r, f = calculate_metrics(i, cm_globale)
        print(f"{name:<10} | {p:<10.2f} | {r:<10.2f} | {f:<10.2f}")
    
    moyenne_acc = sum(accuracies) / k
    print("-" * 45)
    print(f"Accuracy Moyenne Globale : {moyenne_acc:.2f}%")

    # Visualisation
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm_globale, annot=True, fmt='d', cmap='Greens', xticklabels=labels_names, yticklabels=labels_names)
    plt.title(f'Matrice de Confusion VADER (K-Fold, K={k})')
    plt.ylabel('Réalité')
    plt.xlabel('Prédictions')
    plt.savefig("news/sentiment/confusion_matrix_vader.png")

if __name__ == "__main__":
    train_and_test_vader(dataset_path="news/sentiment/sentiment_equilibre.csv", k=10)