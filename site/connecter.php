<?php
session_start();
header('Content-Type: text/plain');

include 'bd.php';
$pdo = getBD();

$email = $_POST['mail'] ?? '';
$mdp   = $_POST['password'] ?? '';

$stmt = $pdo->prepare("SELECT * FROM client WHERE email = ?");
$stmt->execute([$email]);
$client = $stmt->fetch(PDO::FETCH_ASSOC);

if ($client && password_verify($mdp, $client['mdp'])) {
    $token=random_int(1, 99);

$update = $pdo->prepare("UPDATE client SET token = ? WHERE email = ?");
    $update->execute([$token, $email]);    
    
    $_SESSION['client'] = [
        'id'     => $client['id'], 
        'pseudo' => $client['pseudo'], 
        'email'  => $client['email'],
        'monnaie'=> $client['monnaie'],
    ];
    echo '1';
} else {
    echo '0';
}
?>