<?php
session_start();
$ticker = $_POST['ticker'] ?? null;
$quantite = intval($_POST['quantite'] ?? 0);

if ($ticker && $quantite > 0) {
    if (!isset($_SESSION['panier'])) $_SESSION['panier'] = [];
    
    // Si l'action est déjà là, on cumule
    if (isset($_SESSION['panier'][$ticker])) {
        $_SESSION['panier'][$ticker] += $quantite;
    } else {
        $_SESSION['panier'][$ticker] = $quantite;
    }
}
header('Location: panier.php');
exit;