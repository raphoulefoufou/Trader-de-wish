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
    echo '1';
} else {
    echo '0';
}
?>