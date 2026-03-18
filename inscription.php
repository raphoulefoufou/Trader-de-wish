<?php
header('Content-Type: text/plain');

include 'bd.php';
$pdo = getBD();

$pseudo = $_POST['pseudo'];
$mdp = $_POST['password'];
$email = $_POST['mail'];

$ok = true;

$sql = $pdo->prepare("SELECT pseudo, email FROM client");
$sql->execute();
$clients = $sql->fetchAll(PDO::FETCH_ASSOC);

foreach($clients as $cli){
    if($pseudo == $cli['pseudo'] || $email == $cli['email']){
        $ok = false;
        break;
    }
}

if($ok){

    $stmt = $pdo->prepare("INSERT INTO client(pseudo, email, mdp,monnaie) VALUES(:pseudo, :email, :mdp, :monnaie)");
    $stmt->execute([
        "pseudo"=>$pseudo,
        "email"=>$email,
        "mdp"=>password_hash($mdp, PASSWORD_DEFAULT),
        "monnaie"=>10000
    ]);
        $id = $pdo->lastInsertId();


    session_start();

    $_SESSION['client'] = [
        'id'=>$id,
        'pseudo'=>$pseudo,
        'email'=>$email,
        'monnaie'=>10000
        
    ];

    echo "1";
}else{
    echo "0";
}
exit(); ?>