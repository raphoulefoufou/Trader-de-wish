<?php
session_start();

// 1. Générer un token sécurisé s'il n'existe pas encore
if (empty($_SESSION['token'])) {
    $_SESSION['token'] = bin2hex(random_bytes(32));
}

// 2. Vérification (uniquement si des données sont envoyées, ex: POST)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_POST['token']) || $_POST['token'] !== $_SESSION['token']) {
        http_response_code(403);
        exit("Erreur : Jeton CSRF invalide ou absent.");
    }
}
?>