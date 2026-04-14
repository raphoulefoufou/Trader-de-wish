<?php
session_start();

// Redirection si non connecté
if (!isset($_SESSION['client'])) {
    header("Location: connexion.php");
    exit();
}

include 'bd.php';
include 'header.php';

$pdo = getBD();
$pseudo = $_SESSION['client']['pseudo'];

// ==========================================
// TRAITEMENT DES ACTIONS (Ajout fonds & Reset)
// ==========================================
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action_type'])) {
    
    // 1. Ajouter des fonds (+ 5 000 €)
    if ($_POST['action_type'] === 'add_funds') {
        $pdo->prepare("UPDATE client SET monnaie = monnaie + 5000 WHERE pseudo = ?")->execute([$pseudo]);
        header("Location: dashboard.php");
        exit();
    }
    
    // 2. Réinitialiser le compte (Remise à zéro)
    if ($_POST['action_type'] === 'reset_account') {
        // Vider le portefeuille
        $pdo->prepare("DELETE FROM portefeuille WHERE pseudo_client = ?")->execute([$pseudo]);
        // Vider l'historique des transactions
        $pdo->prepare("DELETE FROM transactions WHERE pseudo_client = ?")->execute([$pseudo]);
        // Remettre l'argent à 10 000 € et effacer les gains historiques
        $pdo->prepare("UPDATE client SET monnaie = 10000, gain_realise = 0 WHERE pseudo = ?")->execute([$pseudo]);
        
        header("Location: dashboard.php");
        exit();
    }
}
// ==========================================

// 1. Récupération du solde
$stmt = $pdo->prepare("SELECT monnaie FROM client WHERE pseudo = ?");
$stmt->execute([$pseudo]);
$client = $stmt->fetch();
$solde = $client['monnaie'] ?? 0;

// 2. Statistiques du joueur
$stmt = $pdo->prepare("SELECT COUNT(*) as total_trades FROM transactions WHERE pseudo_client = ?");
$stmt->execute([$pseudo]);
$stats_trades = $stmt->fetch();

$stmt = $pdo->prepare("SELECT COUNT(DISTINCT ticker) as diversif FROM portefeuille WHERE pseudo_client = ? AND quantite > 0");
$stmt->execute([$pseudo]);
$stats_div = $stmt->fetch();

// 3. Historique récent
$stmt = $pdo->prepare("SELECT * FROM transactions WHERE pseudo_client = ? ORDER BY date_transaction DESC LIMIT 5");
$stmt->execute([$pseudo]);
$historique = $stmt->fetchAll(PDO::FETCH_ASSOC);

// 4. L'Action du jour
$stmt = $pdo->prepare("SELECT ticker, nom, info FROM marche ORDER BY RAND() LIMIT 1");
$stmt->execute();
$action_du_jour = $stmt->fetch(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Centre de Commandes - Trading for Sure</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b1220; color: #e5e7eb; margin: 0; padding: 20px; }
        
        /* Layout de l'en-tête pour aligner titre et boutons */
        .header-container { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px; flex-wrap: wrap; gap: 15px; }
        .dashboard-header h1 { color: #fff; margin-bottom: 5px; margin-top: 0; }
        .dashboard-header p { color: #9ca3af; font-size: 1.1em; margin: 0; }
        
        /* Style des nouveaux boutons d'action */
        .btn-action { background: #3b82f6; color: white; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: 0.2s; font-size: 0.9em; display: inline-flex; align-items: center; gap: 5px; }
        .btn-action:hover { background: #2563eb; transform: translateY(-2px); }
        .btn-danger { background: #ef4444; }
        .btn-danger:hover { background: #dc2626; }
        .actions-group { display: flex; gap: 10px; }

        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .kpi-card { background: linear-gradient(135deg, #1e293b, #0f172a); padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border-left: 4px solid #3b82f6; }
        .kpi-card h3 { margin: 0 0 10px 0; color: #9ca3af; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px; }
        .kpi-card .value { font-size: 2em; font-weight: bold; color: #fff; }

        .main-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
        @media (max-width: 900px) { .main-grid { grid-template-columns: 1fr; } }

        .panel { background: #111827; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .panel h2 { margin-top: 0; border-bottom: 1px solid #374151; padding-bottom: 10px; font-size: 1.2em; }

        .history-table { width: 100%; border-collapse: collapse; }
        .history-table th, .history-table td { padding: 12px; text-align: left; border-bottom: 1px solid #1f2937; }
        .badge-achat { background: #064e3b; color: #34d399; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; }
        .badge-vente { background: #7f1d1d; color: #f87171; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; }

        .suggestion-card { background: linear-gradient(135deg, #2563eb, #1d4ed8); border: none; color: white; }
        .suggestion-card h2 { border-bottom-color: rgba(255,255,255,0.2); }
        .btn-trader { display: inline-block; background: white; color: #1d4ed8; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: 15px; transition: all 0.2s; }
        .btn-trader:hover { background: #f3f4f6; transform: translateY(-2px); }
    </style>
</head>
<body>

<div class="header-container">
    <div class="dashboard-header">
        <h1>Bienvenue, <?php echo htmlspecialchars($pseudo); ?></h1>
        <p>Voici le résumé de votre activité d'investisseur.</p>
    </div>
    
    <div class="actions-group">
        <form method="POST">
            <input type="hidden" name="action_type" value="add_funds">
            <button type="submit" class="btn-action">Ajouter 5 000 € à votre compte</button>
        </form>
        
        <form method="POST" onsubmit="return confirm('Attention ! Cela va vider votre portefeuille, supprimer votre historique et remettre votre solde à 10 000 €. Voulez-vous continuer ?');">
            <input type="hidden" name="action_type" value="reset_account">
            <button type="submit" class="btn-action btn-danger">⚠️ Réinitialiser le compte</button>
        </form>
    </div>
</div>

<div class="kpi-grid">
    <div class="kpi-card" style="border-left-color: #22c55e;">
        <h3>💰 Capacité d'Investissement</h3>
        <div class="value"><?php echo number_format($solde, 2); ?> €</div>
    </div>
    
    <div class="kpi-card" style="border-left-color: #a855f7;">
        <h3>📊 Transactions Totales</h3>
        <div class="value"><?php echo $stats_trades['total_trades']; ?></div>
    </div>

    <div class="kpi-card" style="border-left-color: #f59e0b;">
        <h3>🎯 Diversification</h3>
        <div class="value"><?php echo $stats_div['diversif']; ?> <span style="font-size:0.4em; font-weight:normal; color:#9ca3af;">actifs détenus</span></div>
    </div>
</div>

<div class="main-grid">
    <div class="panel">
        <h2>Dernières Transactions</h2>
        <?php if (empty($historique)): ?>
            <p style="color: #9ca3af; text-align: center; padding: 20px;">Aucune transaction récente. Il est temps d'investir !</p>
        <?php else: ?>
            <table class="history-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Action</th>
                        <th>Type</th>
                        <th>Quantité</th>
                        <th>Prix U.</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($historique as $tx): ?>
                        <tr>
                            <td style="color: #9ca3af; font-size: 0.9em;"><?php echo date('d/m/Y H:i', strtotime($tx['date_transaction'])); ?></td>
                            <td><strong><?php echo htmlspecialchars($tx['ticker']); ?></strong></td>
                            <td>
                                <?php if ($tx['type_action'] == 'ACHAT'): ?>
                                    <span class="badge-achat">ACHAT</span>
                                <?php else: ?>
                                    <span class="badge-vente">VENTE</span>
                                <?php endif; ?>
                            </td>
                            <td><?php echo $tx['quantite']; ?></td>
                            <td><?php echo number_format($tx['prix_unitaire'], 2); ?> €</td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        <?php endif; ?>
    </div>

    <div class="panel suggestion-card">
        <h2>💡 L'Action à Découvrir</h2>
        <?php if ($action_du_jour): ?>
            <h3 style="font-size: 1.5em; margin: 15px 0 5px 0;"><?php echo htmlspecialchars($action_du_jour['nom']); ?></h3>
            <span style="background: rgba(255,255,255,0.2); padding: 3px 8px; border-radius: 4px; font-size: 0.8em;"><?php echo htmlspecialchars($action_du_jour['ticker']); ?></span>
            
            <p style="margin-top: 15px; line-height: 1.5; font-size: 0.95em; opacity: 0.9;">
                <?php echo htmlspecialchars($action_du_jour['info']); ?>
            </p>
            
            <a href="trader.php?ticker=<?php echo urlencode($action_du_jour['ticker']); ?>" class="btn-trader">
                Voir ce marché &rarr;
            </a>
        <?php else: ?>
            <p>Le marché est actuellement vide.</p>
        <?php endif; ?>
    </div>
</div>

</body>
</html>