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
<?php
$stmt=$pdo->prepare("SELECT * FROM marche");
$stmt->execute();
$marche=$stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<table class="marches"> 
    <tr>
<th>Ticker</th>
<th>Entreprise</th>
<th>Info</th>
</tr>


</tr>
<?php
foreach($marche as $march){
     echo "<tr>
    <td>{$march['ticker']}</td>
    <td><a href=http://51.38.225.40:3000?ticker={$march['ticker']}>{$march['nom']}</td>
    <td>{$march['info']}</td>
    </tr>";
    

}
?>


<table>
</body>
</html>