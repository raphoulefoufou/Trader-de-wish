<?php
if(isset($_POST['start'])){
    header('Location: dashboard.php');
    exit;
}

if(isset($_POST['explore'])){
    header('Location: marches.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home - Trade For Sure</title>
    <link href="home.css" rel="stylesheet" />
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    
</head>
<?php
include 'securite.php';
?>
<body class="hero">

<header>

    <img id="menu-ferme" src="images/menu_ferme.png" alt="Ouvrir Menu">

    <div id="menu-ouvert">
        <div id="menu-header">
            <img id="img_menu_ouvert" src="images/menu_ferme.png" alt="Fermer Menu">
            <h1 id="title-Menu">Menu</h1>
        </div>
        <hr>
        <ul>
            <li><a class="textelien" href="Home.php">Accueil</a></li>
            <li><a class="textelien" href="connexion.php"> Se connecter </a></li>
            <li><a class="textelien" href="enregistrement.php">S'inscrire </a></li>
            <li><a class="textelien" href="dashboard.php">Dashboard </a></li>
                        <li><a class="textelien" href="marches.php">Marchés </a></li>
            <?php 
            if (isset($_SESSION['client']['pseudo'])){?>
             <li><a class="textelien" href="deconnexion.php">Se deconnecter </a></li>
            <?php } ?>

        </ul>
    </div>


</header>

<div class="hero-content" style="text-align: center; margin-top: 100px;">
    <h1>Trade For Sure</h1>
    <p>Tradez, investissez et gérez vos actions en bourse en toute confiance.</p>

    <form method="post">
        <button type="submit" name="start" class="btn primary">
            Commencer à trader →
        </button>
        <button type="submit" name="explore" class="btn secondary">
            Explorer les marchés
        </button>
    </form>
</div>

<script>
    $(document).ready(function(){
        $("#menu-ferme").click(function (){
            $("#menu-ouvert").show("slide", { direction: "left" }, 300) || $("#menu-ouvert").fadeIn();
        });

        $("#img_menu_ouvert").click(function (){
            $("#menu-ouvert").fadeOut();
        });

        $(document).mouseup(function(e) {
            var container = $("#menu-ouvert");
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                container.fadeOut();
            }
        });
    });
</script>

</body>
</html>