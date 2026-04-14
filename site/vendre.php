<?php
session_start();

if (!isset($_SESSION['client'])) {
    header("Location: connexion.php");
    exit();
}

include 'bd.php';
$pdo = getBD();
$pseudo = $_SESSION['client']['pseudo'];
$message = "";

// 1. TRAITEMENT DE LA VENTE (Quand on clique sur le bouton)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $ticker = $_POST['ticker'];
    $quantite_a_vendre = intval($_POST['quantite']);

    // Vérifier combien d'actions possède le client
    $stmt = $pdo->prepare("SELECT * FROM portefeuille WHERE pseudo_client = ? AND ticker = ?");
    $stmt->execute([$pseudo, $ticker]);
    $pos = $stmt->fetch();

    if (!$pos || $pos['quantite'] < $quantite_a_vendre || $quantite_a_vendre <= 0) {
        $message = "<div style='color: #f87171; background: #7f1d1d; padding: 10px; border-radius: 5px;'>Erreur : Quantité invalide.</div>";
    } else {
        // Récupérer le prix en direct depuis ton API Flask
        $api_url = "http://127.0.0.1:5000/api/prix?ticker=" . urlencode($ticker);
        $data = json_decode(file_get_contents($api_url), true);

        if ($data && isset($data['prix_eur'])) {
            $prix_actuel = $data['prix_eur'];
            
            // Calculs
            $montant_recu = $prix_actuel * $quantite_a_vendre;
            $profit_realise = ($prix_actuel - $pos['prix_achat_moyen']) * $quantite_a_vendre;

            // Mettre à jour la monnaie et le gain_realise dans la table client
            $pdo->prepare("UPDATE client SET monnaie = monnaie + ?, gain_realise = gain_realise + ? WHERE pseudo = ?")
                ->execute([$montant_recu, $profit_realise, $pseudo]);

            // Mettre à jour le portefeuille (retirer les actions)
            $nouvelle_qte = $pos['quantite'] - $quantite_a_vendre;
            if ($nouvelle_qte == 0) {
                $pdo->prepare("DELETE FROM portefeuille WHERE id = ?")->execute([$pos['id']]);
            } else {
                $pdo->prepare("UPDATE portefeuille SET quantite = ? WHERE id = ?")->execute([$nouvelle_qte, $pos['id']]);
            }

            // Ajouter à l'historique
            $pdo->prepare("INSERT INTO transactions (pseudo_client, ticker, quantite, prix_unitaire, type_action) VALUES (?, ?, ?, ?, 'VENTE')")
                ->execute([$pseudo, $ticker, $quantite_a_vendre, $prix_actuel]);

            // Rediriger vers le portefeuille
            header("Location: wallet.php");
            exit();
        } else {
            $message = "<div style='color: #f87171; background: #7f1d1d; padding: 10px; border-radius: 5px;'>Erreur API : Impossible de récupérer le prix.</div>";
        }
    }
}

// 2. AFFICHAGE DE LA PAGE
$ticker = $_GET['ticker'] ?? '';
if (empty($ticker)) {
    header("Location: wallet.php");
    exit();
}

// Récupérer les infos de l'entreprise et la quantité possédée
$stmt = $pdo->prepare("
    SELECT p.quantite, p.prix_achat_moyen, m.nom 
    FROM portefeuille p 
    JOIN marche m ON p.ticker = m.ticker 
    WHERE p.pseudo_client = ? AND p.ticker = ?
");
$stmt->execute([$pseudo, $ticker]);
$action = $stmt->fetch();

if (!$action) {
    echo "Vous ne possédez pas cette action.";
    exit();
}

include 'header.php';
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Vendre - <?php echo htmlspecialchars($action['nom']); ?></title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0b1220; color: #e5e7eb; padding: 30px; }
        .vendre-card { background: #111827; padding: 30px; border-radius: 12px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.4); }
        .input-qte { width: 100%; padding: 12px; margin: 15px 0; border-radius: 6px; border: 1px solid #374151; background: #1f2937; color: white; font-size: 1.1em; }
        .btn-vendre { background: #ef4444; color: white; border: none; padding: 12px 20px; border-radius: 6px; width: 100%; font-size: 1.1em; font-weight: bold; cursor: pointer; transition: 0.2s; }
        .btn-vendre:hover { background: #dc2626; }
    </style>
</head>
<body>

<div class="vendre-card">
    <h1 style="margin-bottom: 10px;">Vendre des actions</h1>
    <h2 style="color: #60a5fa; margin-bottom: 20px;"><?php echo htmlspecialchars($action['nom']); ?> (<?php echo htmlspecialchars($ticker); ?>)</h2>
    
    <?php if($message) echo $message; ?>

    <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
        <p>Prix d'achat moyen : <strong><?php echo number_format($action['prix_achat_moyen'], 2); ?> €</strong></p>
        <p>Quantité possédée : <strong style="color: #22c55e; font-size: 1.2em;"><?php echo $action['quantite']; ?></strong></p>
        <p>Prix actuel du marché : <strong id="live-price" style="color: #facc15;">Chargement...</strong></p>
    </div>

    <form method="POST" action="vendre.php?ticker=<?php echo htmlspecialchars($ticker); ?>">
        <input type="hidden" name="ticker" value="<?php echo htmlspecialchars($ticker); ?>">
        
        <label>Combien d'actions voulez-vous vendre ?</label>
        <input type="number" name="quantite" class="input-qte" min="1" max="<?php echo $action['quantite']; ?>" value="1" required>
        
        <button type="submit" class="btn-vendre">Confirmer la vente</button>
    </form>
    
    <div style="text-align: center; margin-top: 15px;">
        <a href="wallet.php" style="color: #9ca3af; text-decoration: none;">Annuler et retourner au portefeuille</a>
    </div>
</div>

<script>
    // Récupérer le prix en direct pour l'affichage visuel
    const ticker = "<?php echo htmlspecialchars($ticker); ?>";
    async function fetchPrice() {
        try {
            const res = await fetch(`http://51.38.225.40:5000/api/prix?ticker=${ticker}`);
            const data = await res.json();
            if (data.prix_eur) {
                document.getElementById('live-price').innerText = data.prix_eur.toFixed(2) + " €";
            }
        } catch(e) {
            document.getElementById('live-price').innerText = "Erreur réseau";
        }
    }
    fetchPrice();
</script>

</body>
</html>