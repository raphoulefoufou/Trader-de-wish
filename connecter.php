<?php
header('Content-Type: text/plain');

include 'bd.php';
$pdo = getBD();

$email = $_POST['mail'] ?? '';
$mdp   = $_POST['password'] ?? '';

$stmt = $pdo->prepare("SELECT * FROM client WHERE email = ?");
$stmt->execute([$email]);
$client = $stmt->fetch(PDO::FETCH_ASSOC);

if ($client && password_verify($mdp, $client['mdp'])) {
    $token=bin2hex(random_bytes(32));

$update = $pdo->prepare("UPDATE client SET token = ? WHERE email = ?");
    $update->execute([$token, $email]);    
    session_start();
    $_SESSION['client'] = [
        'id'     => $client['id'], // Utile pour tes requêtes SQL plus tard
        'pseudo' => $client['pseudo'], // Ce que tu cherches dans panier.php
        'email'  => $client['email'],
        'monnaie'=> $client['monnaie'],
    ];
    echo '1';
} else {
    echo '0';
}
?>