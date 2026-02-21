<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="dashboard.css" rel="stylesheet" />

    <title>Document</title>
</head>
<body>
<?php
include 'header.php';
include 'bd.php';

$pdo=getBD();
$stmt=$pdo->Prepare("SELECT * FROM marche ORDER BY prix DESC LIMIT 3");
$stmt->execute();
$prix=$stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<h1>Dashboard</h1>
<h2>Top Assets </h2>
<table class="prix">
<?php
foreach($prix as $pr){
     echo "<tr>
    <td>{$pr['nom_marche']}</td>
    <td>{$pr['prix']}</td></tr>";

}


?>
</table>
</body>
</html>