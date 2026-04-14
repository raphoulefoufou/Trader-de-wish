<?php
session_start();
include 'bd.php';
$pdo = getBD();

if (!isset($_SESSION['client']) || empty($_SESSION['panier'])) {
    echo "0"; exit;
}

$pseudo = $_SESSION['client']['pseudo'];
$total_facture = 0;
$transactions_a_faire = [];

// 1. On récupère les prix frais depuis l'API Python pour chaque item
foreach ($_SESSION['panier'] as $ticker => $quantite) {
    $api_url = "http://127.0.0.1:5000/api/prix?ticker=" . $ticker;
    $data = json_decode(file_get_contents($api_url), true);
    
    if (!$data || !isset($data['prix_eur'])) { echo "Erreur API"; exit; }
    
    $prix_actuel = $data['prix_eur'];
    $total_facture += ($prix_actuel * $quantite);
    $transactions_a_faire[] = [
        'ticker' => $ticker,
        'quantite' => $quantite,
        'prix' => $prix_actuel
    ];
}

// 2. Vérifier le solde
$stmt = $pdo->prepare("SELECT monnaie FROM client WHERE pseudo = ?");
$stmt->execute([$pseudo]);
$client = $stmt->fetch();

if ($client['monnaie'] < $total_facture) {
    echo "solde_insuffisant"; exit;
}

// 3. Exécuter les achats
foreach ($transactions_a_faire as $t) {
    // Débiter le solde
    $pdo->prepare("UPDATE client SET monnaie = monnaie - ? WHERE pseudo = ?")
        ->execute([($t['prix'] * $t['quantite']), $pseudo]);

    // Enregistrer la transaction (Historique)
    $pdo->prepare("INSERT INTO transactions (pseudo_client, ticker, quantite, prix_unitaire, type_action) VALUES (?, ?, ?, ?, 'ACHAT')")
        ->execute([$pseudo, $t['ticker'], $t['quantite'], $t['prix']]);

    // Mettre à jour le portefeuille (Profit calculation)
    $stmt = $pdo->prepare("SELECT * FROM portefeuille WHERE pseudo_client = ? AND ticker = ?");
    $stmt->execute([$pseudo, $t['ticker']]);
    $pos = $stmt->fetch();

    if ($pos) {
        // Recalcul du prix moyen : (AncienTotal + NouveauTotal) / NouvelleQuantite
        $nouvelle_qte = $pos['quantite'] + $t['quantite'];
        $nouveau_prix_moyen = (($pos['prix_achat_moyen'] * $pos['quantite']) + ($t['prix'] * $t['quantite'])) / $nouvelle_qte;
        
        $pdo->prepare("UPDATE portefeuille SET quantite = ?, prix_achat_moyen = ? WHERE id = ?")
            ->execute([$nouvelle_qte, $nouveau_prix_moyen, $pos['id']]);
    } else {
        $pdo->prepare("INSERT INTO portefeuille (pseudo_client, ticker, quantite, prix_achat_moyen) VALUES (?, ?, ?, ?)")
            ->execute([$pseudo, $t['ticker'], $t['quantite'], $t['prix']]);
    }
}

$_SESSION['panier'] = []; // Vider le panier
echo "1";