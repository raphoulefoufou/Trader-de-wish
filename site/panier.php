<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <link href="panier.css" rel="stylesheet" />
    <title>Confirmation d'achat - Trading for Sure</title>
</head>
<body>
<?php
session_start();

// Vérification de la session
if (!isset($_SESSION['client'])) {
    header("Location: login.php");
    exit();
}

$prenom = $_SESSION['client']['pseudo'];
include 'header.php';
include 'bd.php';

$pdo = getBD();
$items_details = [];

// On récupère les infos de la base pour chaque ticker dans le panier
if (isset($_SESSION['panier']) && !empty($_SESSION['panier'])) {
    foreach ($_SESSION['panier'] as $ticker => $quantite) {
        $sql = "SELECT nom FROM marche WHERE ticker = ?";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$ticker]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($row) {
            $items_details[] = [
                'ticker' => $ticker,
                'nom' => $row['nom'],
                'quantite' => $quantite
            ];
        }
    }
} else {
    echo "<div class='container'><p>Votre panier est vide.</p></div>";
    exit();
}
?>

<div class="container">
    <div class="card">
        <h2>Confirmation d'achat</h2>
        <p>Utilisateur : <strong><?php echo htmlspecialchars($prenom); ?></strong></p>
        
        <table style="width:100%; text-align:left; margin-bottom: 20px;">
            <tr>
                <th>Entreprise</th>
                <th>Quantité</th>
                <th>Prix Unitaire (Est.)</th>
            </tr>
            <?php foreach ($items_details as $item): ?>
            <tr>
                <td><?php echo htmlspecialchars($item['nom']); ?> (<?php echo $item['ticker']; ?>)</td>
                <td><?php echo $item['quantite']; ?></td>
                <td class="live-price" data-ticker="<?php echo $item['ticker']; ?>" data-qte="<?php echo $item['quantite']; ?>">Chargement...</td>
            </tr>
            <?php endforeach; ?>
        </table>

        <div class="total-section">
            <h3>Total estimé : <span id="total-final">0.00</span> €</h3>
        </div>

        <form id="form-acheter">
            <button type="submit" id="btn-confirmer" class="btn-primary">Confirmer l'achat en bourse</button>
            <div id="message" style="margin-top:15px; font-weight:bold;"></div>
        </form>
    </div>
</div>

<script>
$(document).ready(function(){
    let totalGlobal = 0;

    // Récupération des prix en temps réel via l'API Flask
    $('.live-price').each(function(){
        let cell = $(this);
        let ticker = cell.data('ticker');
        let quantite = parseInt(cell.data('qte')); // On récupère la quantité
        
        $.getJSON(`http://51.38.225.40:5000/api/prix?ticker=${ticker}`, function(data) {
            if (data.prix_eur) {
                // Affichage du prix unitaire
                cell.text(data.prix_eur.toFixed(2) + " €");
                
                // NOUVEAU : Calcul du sous-total pour cette action et ajout au total global
                let sousTotal = data.prix_eur * quantite;
                totalGlobal += sousTotal;
                
                // Mise à jour de l'affichage du total final
                $('#total-final').text(totalGlobal.toFixed(2));
            }
        }).fail(function() {
            cell.text("Erreur prix");
        });
    });

    // Gestion de la validation
    $('#form-acheter').on('submit', function(e){
        e.preventDefault();
        $('#btn-confirmer').prop('disabled', true).text('Transaction en cours...');

        $.ajax({
            url: 'valider.php',
            type: 'POST',
            data: {
                transaction_type: 'buy_all'
            },
            success: function(response) {
                if (response.trim() === '1') {
                    $('#message').css('color', 'green').text("L'achat a été effectué avec succès ! Redirection...");
                    setTimeout(function() {
                        window.location.href = "index.php";
                    }, 2500);
                } else {
                    $('#message').css('color', 'red').text('Solde insuffisant ou erreur de transaction.');
                    $('#btn-confirmer').prop('disabled', false).text('Réessayer');
                }
            },
            error: function() {
                $('#message').text('Erreur serveur critique.');
                $('#btn-confirmer').prop('disabled', false);
            }
        });
    });
});
</script>

<style>
    .container { display: flex; justify-content: center; padding: 50px; }
    .card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 500px; }
    .btn-primary { background: #2ecc71; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%; font-size: 1.1em; }
    .btn-primary:hover { background: #27ae60; }
    th, td { padding: 10px; border-bottom: 1px solid #eee; }
    .total-section { text-align: right; margin-bottom: 20px; padding-top: 10px; border-top: 2px solid #eee; }
</style>

</body>
</html>