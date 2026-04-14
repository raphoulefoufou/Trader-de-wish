<?php
session_start();
include 'bd.php';
include 'header.php';
$pdo = getBD();

if (isset($_GET["ticker"])) {
    $ticker = $_GET['ticker'];
    $stmt = $pdo->prepare("SELECT * FROM marche WHERE ticker = ?");
    $stmt->execute([$ticker]);
    $marche = $stmt->fetch(PDO::FETCH_ASSOC);
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <link href="trader.css" rel="stylesheet" />
    <title>Trader - <?php echo $ticker; ?></title>
</head>
<body>
<div class="container">
    <div class="card">
        <h1><?php echo htmlspecialchars($marche['nom']); ?> (<?php echo $ticker; ?>)</h1>
        <div class="price-box">
            <span id="live-price">--</span> €
        </div>
        <p><?php echo htmlspecialchars($marche['info']); ?></p>

        <?php if (isset($_SESSION['client'])) : ?>
            <form action="acheter.php" method="post">
                <input type="hidden" name="ticker" value="<?php echo $ticker; ?>">
                <label>Quantité :</label>
                <input type="number" name="quantite" min="1" required>
                <button type="submit">Ajouter au panier</button>
            </form>
        <?php endif; ?>
    </div>
</div>

<script>
    async function updatePrice() {
        const res = await fetch(`http://51.38.225.40:5000/api/prix?ticker=<?php echo $ticker; ?>`);
        const data = await res.json();
        if (data.prix_eur) document.getElementById('live-price').innerText = data.prix_eur.toFixed(2);
    }
    updatePrice();
    setInterval(updatePrice, 10000);
</script>
</body>
</html>