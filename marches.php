<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=
    , initial-scale=1.0">
    <title>Document</title>
    <link href="marches.css" rel="stylesheet" />
</head>
<body>
<?php
include 'header.php';
include 'bd.php';
$pdo=getBD();
?>
<h1>Marches </h1>
<input type="search" id="site-search" name="q" placeholder="Rechercher un marche"/>
<?php
$stmt=$pdo->prepare("SELECT * FROM marche");
$stmt->execute();
$marche=$stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<table class="marches"> 
    <tr>
<th>#</th>
<th>Nom du Marche</th>
<th>Prix</th>
<th>Quantites</th>
</tr>
<?php
foreach($marche as $march){
     echo "<tr>
    <td>{$march['id_marche']}</td>
    <td><a href=trader.php?id_marche={$march['id_marche']}>{$march['nom_marche']}</td>
    <td>{$march['prix']}</td>
    <td>{$march['quantites']}</td>";
    

}
?>


<table>
</body>
</html>