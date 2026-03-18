# Commentez ces lignes si vous n'avez pas de contrainte de stockage ou de téléchargement, sinon assurez-vous que le chemin est correct et accessible
import os
# Définir le cache Hugging Face pour éviter les problèmes de téléchargement et de stockage
os.environ['HF_HOME'] = 'D:/HuggingFaceCache'

import csv
import random
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Vérification du GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def evaluation_finbert(dataset_path="news/sentiment/sentiment_equilibre.csv", k=10):
    # Chargement du modèle et du tokenizer FinBERT
    model_name = "ProsusAI/finbert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
    
    # Mapping FinBERT : 0 -> positive, 1 -> negative, 2 -> neutral
    # Ton mapping : -1 -> neg, 0 -> neu, 1 -> pos
    label_map_finbert = {0: 1, 1: -1, 2: 0}
    label_map_data = {"negative": -1, "neutral": 0, "positive": 1}

    # Chargement des données (Même méthode que TF-IDF)
    data = []
    with open(dataset_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lbl = row['Sentiment'].strip().lower()
            if lbl in label_map_data:
                data.append((row['Sentence'], label_map_data[lbl]))

    random.seed(47) # Constante pour la comparaison
    random.shuffle(data)
    
    fold_size = len(data) // k
    accuracies = []
    cm_globale = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    idx_map = {-1: 0, 0: 1, 1: 2}

    print(f"Démarrage de l'évaluation FinBERT sur {device} (K={k})...")

    model.eval()
    with torch.no_grad():
        for fold in range(k):
            start, end = fold * fold_size, (fold + 1) * fold_size
            test_data = data[start:end]
            
            correct_fold = 0
            for texte, true_label in test_data:
                # Tokenisation
                inputs = tokenizer(texte, padding=True, truncation=True, return_tensors="pt").to(device)
                outputs = model(**inputs)
                
                # Récupération de la prédiction
                pred_idx = torch.argmax(outputs.logits, dim=1).item()
                pred_label = label_map_finbert[pred_idx]
                
                cm_globale[idx_map[true_label]][idx_map[pred_label]] += 1
                if pred_label == true_label:
                    correct_fold += 1
            acc_fold = (correct_fold/len(test_data))*100
            accuracies.append(acc_fold)
            print(f"  Fold {fold + 1} : Accuracy = {acc_fold:.2f}%")

    # Affichage des résultats
    labels_names = ["Négatif", "Neutre", "Positif"]
    print("\n" + "="*60 + "\nRÉSULTATS FINBERT\n" + "="*60)
    
    # Calcul des métriques
    for i, name in enumerate(labels_names):
        true_pos = cm_globale[i][i]
        false_pos = sum(cm_globale[row][i] for row in range(3)) - true_pos
        false_neg = sum(cm_globale[i][col] for col in range(3)) - true_pos
        precision = true_pos/(true_pos+false_pos) if (true_pos+false_pos)>0 else 0
        recall = true_pos/(true_pos+false_neg) if (true_pos+false_neg)>0 else 0
        f1_score = 2*(precision*recall)/(precision+recall) if (precision+recall)>0 else 0
        print(f"{name:<10} | F1-Score: {f1_score:.2f} (Precision: {precision:.2f}, Recall: {recall:.2f})")
    
    print("-" * 60)
    print(f"Accuracy Moyenne Globale FinBERT : {np.mean(accuracies):.2f}%")
    print("="*60 + "\n")

    # Graphique
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm_globale, annot=True, fmt='d', cmap='Purples', xticklabels=labels_names, yticklabels=labels_names)
    plt.title(f'Matrice de Confusion FinBERT (K-Fold, K={k})')
    plt.savefig("news/sentiment/confusion_matrix_finbert.png")

if __name__ == "__main__":
    evaluation_finbert()