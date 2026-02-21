<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="trader.css" rel="stylesheet" />

    <title>Document</title>
</head>
<body>
<?php
session_start();
include 'bd.php';
include 'header.php';
$pdo=getBD();

if (isset($_GET["id_marche"])){
    $id_marche=intval($_GET['id_marche']);
    $stmt=$pdo->prepare("SELECT * FROM marche WHERE id_marche=?");
    $stmt->execute([$id_marche]);
    $marches=$stmt->fetch(PDO::FETCH_ASSOC);

}
?>
<div class="container">

<div class="card">

    <h1><?php echo htmlspecialchars($marches["nom_marche"]); ?></h1>
    <div class="price">
        <?php echo htmlspecialchars($marches["prix"]); ?> €
    </div>

    <?php if (isset($_SESSION['client'])) { ?>

        <form action="acheter.php" method="post">
            <input type="hidden" name="id_marche" value="<?php echo $id_marche; ?>">

            <label for="quantite">Quantité</label>
            <input type="number" name="quantite" min="1" required>

            <button type="submit">Acheter</button>
        </form>

    <?php } else { ?>

        <p class="login-message">
            Vous devez être connecté pour acheter.
        </p>

    <?php } ?>

</div>
</div>

</body>
</html>
