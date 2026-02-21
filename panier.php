<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
                    <link href="panier.css" rel="stylesheet" />


    <title>Document</title>
</head>
<body>
<?php
session_start();
$prenom=$_SESSION['client']['pseudo'];
include 'header.php';
include 'bd.php';

$pdo=getBD();
foreach ($_SESSION['panier'] as $id_marche => $quantite) {
    $sql = "SELECT nom_marche, prix FROM marche WHERE id_marche = ?";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$id_marche]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($row) {
        $nom = $row['nom_marche'];
        $prix = $row['prix'];
        $prix_total = $prix * $quantite;
    }}
?>
<div class="container">
    <div class="card">
        <h2>Confirmation d'achat</h2>

        <p>Entreprise :</p>
        <strong><?php echo($nom); ?></strong>

        <div class="total">
            <?php echo ($prix_total); ?> €
        </div>

        <form id="acheter">
            <button type="submit">Confirmer l'achat</button>
            <div id="message"></div>
        </form>
    </div>
</div>
<script>
var prix_total = <?php echo json_encode($prix_total); ?>;
var id_marche = <?php echo json_encode($id_marche); ?>;
var nom = <?php echo json_encode($nom); ?>;

$(document).ready(function(){
    $('#acheter').on('submit', function(e){
        e.preventDefault();

        $.ajax({
            url: 'valider.php',
            type: 'POST',
            data: {
                prix_total: prix_total,
                id_marche: id_marche,
                nom: nom
            },
            success: function(response) {
                if (response.trim() === '1') {
                    $('#message').text("L'achat en bourse a pu etre effectue !");
                    setTimeout(function() {
                        window.location.href = "home.php";
                    }, 3000);
                } else {
                    $('#message').text('Solde insufisant');
                }
            },
            error: function() {
                $('#message').text('Erreur serveur');
            }
        });
    });
});
</script>
</body>
</html>