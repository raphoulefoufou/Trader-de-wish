<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
        <link href="wallet.css" rel="stylesheet" />

</head>
<body>
<?php
include 'bd.php';
include 'header.php';
session_start();
$pdo=getBD();
if(isset($_SESSION['client'])){
$id_client=$_SESSION['client']['id'];




$stmt=$pdo->prepare("SELECT * FROM mes_actions WHERE id_client =?");
$stmt->execute([$id_client]);
  $row = $stmt->fetchAll(PDO::FETCH_ASSOC);
$sql=$pdo->prepare("SELECT SUM(prix_total) as total FROM mes_actions WHERE id_client= ?");
$sql->execute([$id_client]);
$result=$sql->fetch(PDO::FETCH_ASSOC);
$total_portefeuille = $result['total'] ?? 0;
?>
  
<div class="wallet-container">
    <h1>Porte Feuille</h1>
    <h2>Votre porte feuille actuel est de : <?php echo($total_portefeuille) ?> €</h2>
</div>
<table class="marches"> 
    <h2>Vos actions </h2>
    <tr>

<th>Nom du Marche</th>
<th>Valeur</th>
<th>Pourcentages</th>
</tr>
<?php
foreach($row as $march){

$prix = $march['prix_total'];

$pourcentage = 0;

if($total_portefeuille > 0){
$pourcentage = ($prix / $total_portefeuille) * 100;
}

echo "<tr>
<td>{$march['nom']}</td>
<td>{$march['prix_total']} €</td>
<td>".round($pourcentage,2)." %</td>
</tr>";
$labels[] = $march['nom'];
    $valeurs[] = round($pourcentage, 2);
}

?>

</table>
<?php
}?>

<?php
if(!isset($_SESSION['client'])) {?>

        <p class="login-message">
            Vous devez être connecté pour voir votre portfolio.
        </p>
<?php
}
?>



</body>
</html>