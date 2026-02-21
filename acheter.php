<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
<?php
session_start();


$id_marche = intval($_POST['id_marche']);
$quantite = intval($_POST['quantite']);

if ($quantite <= 0) {
    header('Location: index.php');
    exit;
}


    
    include 'bd.php';
    $connexion = getBD();
    $stmt = $connexion->prepare("SELECT quantites FROM marche WHERE id_marche = ?");
    $stmt->execute([$id_marche]);
    $article = $stmt->fetch();
    

    if ($quantite <= 0) {
        die('<meta http-equiv="refresh" content="100;url=../index.php">');
    }

    $_SESSION['panier'][$id_marche] = $quantite;
    
    header('Location: panier.php');
    exit;


if ($id_marche !== null) {
    if (!isset($_SESSION['panier'])) {
        $_SESSION['panier'] = [];
    }
    if (isset($_SESSION['panier'][$id_marche])) {
        $_SESSION['panier'][$id_marche] += $quantite;
    } else {
        $_SESSION['panier'][$id_marche] = $quantite;
    }
}

print_r($_SESSION['panier']);
?>

</body>
</html>