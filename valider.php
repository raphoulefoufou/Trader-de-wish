<?php
header('Content-Type: text/plain');

session_start();
include 'bd.php';
$pdo=getBD();


$prix_total=$_POST['prix_total'];
$id_marche=$_POST['id_marche'];
$nom=$_POST['nom'];

$solde=$_SESSION['client']['monnaie'];
$id_client=$_SESSION['client']['id'];


if($solde>=$prix_total){
 $sql = $pdo->prepare("
    INSERT INTO mes_actions (id_marche, id_client, nom, prix_total)
    VALUES (:id_marche, :id_client, :nom, :prix_total)
");

$sql->execute([
    ':id_marche' => $id_marche,
    ':id_client' => $id_client,
    ':nom' => $nom,
    ':prix_total' => $prix_total
]);

echo '1';
}else{
    echo '0';
}
?>
