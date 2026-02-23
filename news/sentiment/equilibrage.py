import pandas as pd

def equilibrer_nouveau_dataset(input_file, output_file):
    # 1. Charger le fichier
    # On précise 'on_bad_lines' au cas où le texte contient des caractères spéciaux
    df = pd.read_csv(input_file, on_bad_lines='skip')
    
    # 2. Nettoyage des noms de colonnes
    df.columns = df.columns.str.strip()
    
    # 3. Nettoyage des labels dans la colonne 'Sentiment'
    df['Sentiment'] = df['Sentiment'].astype(str).str.strip().str.lower()
    
    # 4. Vérification des labels présents
    counts = df['Sentiment'].value_counts()
    print(f"Distribution initiale :\n{counts}")
    
    # On définit les labels
    labels_valides = ['neutral', 'positive', 'negative']
    df = df[df['Sentiment'].isin(labels_valides)]

    # 5. Calcul du nombre minimal pour l'équilibrage
    min_count = df['Sentiment'].value_counts().min()
    print(f"\nÉquilibrage sur la base de {min_count} articles par classe")

    # 6. Échantillonnage
    df_neg = df[df['Sentiment'] == 'negative'].sample(n=min_count, random_state=42)
    df_pos = df[df['Sentiment'] == 'positive'].sample(n=min_count, random_state=42)
    df_neu = df[df['Sentiment'] == 'neutral'].sample(n=min_count, random_state=42)

    # 7. Fusion
    df_balanced = pd.concat([df_neg, df_pos, df_neu])
    df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

    # 8. Sauvegarde
    df_balanced.to_csv(output_file, index=False)
    print(f"Terminé : {len(df_balanced)} articles enregistrés dans {output_file}")

# --- EXÉCUTION ---
if __name__ == "__main__":
    equilibrer_nouveau_dataset("news/sentiment/data.csv", "news/sentiment/sentiment_equilibre.csv")