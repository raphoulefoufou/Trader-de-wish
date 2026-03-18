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


$query = $pdo->prepare("SELECT monnaie FROM client WHERE id = ?");
$query->execute([$id_client]);
$row = $query->fetch(PDO::FETCH_ASSOC);


if($row){
    $monnaie=$row['monnaie'];
}

if ($solde >= $prix_total) {
    $sql = $pdo->prepare("
        INSERT INTO mes_actions (id_marche, id_client, nom, prix_total)
        VALUES (:id_marche, :id_client, :nom, :prix_total)
    ");
    
    $sql->execute([
        ':id_marche' => $id_marche,
        ':id_client' => $id_client,
        ':nom'       => $nom,
        ':prix_total' => $prix_total
    ]);
$nouveau_solde = $monnaie - $prix_total;

$sql2 = $pdo->prepare("UPDATE client SET monnaie = ? WHERE id = ?");
$sql2->execute([$nouveau_solde, $id_client]);

echo '1';
}else{
    echo '0';
}
?>
