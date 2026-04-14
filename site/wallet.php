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

// 1. On récupère le gain réalisé depuis la table client
$stmt_client = $pdo->prepare("SELECT gain_realise FROM client WHERE pseudo = ?");
$stmt_client->execute([$pseudo]);
$client_info = $stmt_client->fetch(PDO::FETCH_ASSOC);
$gain_realise = $client_info ? $client_info['gain_realise'] : 0.00;

// 2. On joint la table portefeuille avec la table marche pour récupérer le nom de l'entreprise 
$sql = "
    SELECT p.ticker, p.quantite, p.prix_achat_moyen, m.nom 
    FROM portefeuille p
    JOIN marche m ON p.ticker = m.ticker
    WHERE p.pseudo_client = ? AND p.quantite > 0
";
$stmt = $pdo->prepare($sql);
$stmt->execute([$pseudo]);
$portefeuille = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mon Portefeuille - Trading for Sure</title>
    <link href="wallet.css" rel="stylesheet" />
</head>
<body>

<div class="wallet-container">
    <h1>Mon Portefeuille Boursier</h1>
    <h2>Utilisateur : <?php echo htmlspecialchars($pseudo); ?></h2>
    
    <div style="display: flex; gap: 20px; margin-top: 20px; flex-wrap: wrap;">
        
        <div style="flex: 1; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); min-width: 250px;">
            <span style="font-size: 1.1em; opacity: 0.9;">Valeur Totale Actuelle :</span>
            <div id="portfolio-total-display" style="font-size: 2.2em; font-weight: bold;">Chargement...</div>
        </div>

        <div style="flex: 1; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); min-width: 250px;">
            <span style="font-size: 1.1em; opacity: 0.9;">Gain/Perte Total Réalisé :</span>
            <div style="font-size: 2.2em; font-weight: bold; color: <?php echo $gain_realise >= 0 ? '#22c55e' : '#f87171'; ?>;">
                <?php echo ($gain_realise > 0 ? "+" : "") . number_format($gain_realise, 2); ?> €
            </div>
        </div>

    </div>
</div>

<?php if (empty($portefeuille)) : ?>
    <div class="login-message">
        Votre portefeuille est actuellement vide. Allez sur les marchés pour acheter des actions !
    </div>
<?php else : ?>
    <table class="marches">
        <thead>
            <tr>
                <th>Entreprise</th>
                <th>Quantité</th>
                <th>Prix Achat Moyen</th>
                <th>Prix Actuel</th>
                <th>Profit / Perte</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($portefeuille as $p) : ?>
            <tr class="stock-row" data-ticker="<?php echo htmlspecialchars($p['ticker']); ?>" data-achat="<?php echo htmlspecialchars($p['prix_achat_moyen']); ?>" data-qte="<?php echo htmlspecialchars($p['quantite']); ?>">
                <td><strong><?php echo htmlspecialchars($p['nom']); ?></strong> <br><span style="font-size:0.85em; color:#9ca3af;"><?php echo htmlspecialchars($p['ticker']); ?></span></td>
                <td><?php echo htmlspecialchars($p['quantite']); ?></td>
                <td><?php echo number_format($p['prix_achat_moyen'], 2); ?> €</td>
                <td class="live-price" style="font-weight: bold;">Chargement...</td>
                <td class="profit-val" style="font-weight: bold;">--</td>
                
                <td>
                    <a href="vendre.php?ticker=<?php echo urlencode($p['ticker']); ?>"
                       style="background-color: #ef4444; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block; text-align: center; transition: 0.2s;">
                       Vendre
                    </a>
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
<?php endif; ?>

<script>
    async function updatePortfolio() {
        const rows = document.querySelectorAll('.stock-row');
        let totalPortefeuilleGlobal = 0; 
        
        for (let row of rows) {
            const ticker = row.dataset.ticker;
            const prixAchat = parseFloat(row.dataset.achat);
            const qte = parseInt(row.dataset.qte);

            try {
                const res = await fetch(`http://51.38.225.40:5000/api/prix?ticker=${ticker}`);
                const data = await res.json();
                
                if (data.prix_eur) {
                    const prixActuel = data.prix_eur;
                    
                    const valeurPosition = prixActuel * qte;
                    totalPortefeuilleGlobal += valeurPosition;

                    const profitUnitaire = prixActuel - prixAchat;
                    const profitTotal = profitUnitaire * qte;

                    row.querySelector('.live-price').innerText = prixActuel.toFixed(2) + " €";
                    const profitCell = row.querySelector('.profit-val');
                    profitCell.innerText = (profitTotal > 0 ? "+" : "") + profitTotal.toFixed(2) + " €";
                    profitCell.style.color = profitTotal >= 0 ? "#22c55e" : "#f87171"; 
                }
            } catch (error) {
                console.error("Erreur API pour " + ticker, error);
                row.querySelector('.live-price').innerText = "Erreur";
            }
        }

        const displayTotal = document.getElementById('portfolio-total-display');
        if (displayTotal) {
            displayTotal.innerText = totalPortefeuilleGlobal.toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €";
        }
    }

    updatePortfolio();
</script>

</body>
</html>