<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
        <link href="header.css" rel="stylesheet" />


</head>
<body>
<?php
if(isset($_POST['home'])){
    header('Location: home.php');
    exit();
}

if(isset($_POST['pf'])){
    header('Location: wallet.php');
    exit();
}
?>
<header class="navbar">


    <nav>
        <form method="POST" action="" class="nav-form">
            <button type="submit" name="home">Accueil</button>
                        <button type="submit" name="dash">Dashboard</button>

            <button type="submit" name="marche">Marchés</button>
            <button type="submit" name="trade">Trader</button>
            <button type="submit" name="wallet" >Portes Feuiles</button>
            <button type="submit" name="portfolio">Portfolio</button>
        </form>
    </nav>
</header>
</body>
</html>