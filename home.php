<?php
// TOUJOURS placer le PHP de redirection au sommet absolu du fichier
if(isset($_POST['start'])){
    header('Location: trader.php');
    exit;
}

if(isset($_POST['explore'])){
    header('Location: explorer.php');
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
            <li><a href="Home.php">Accueil</a></li>
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

        // Optionnel : Fermer le menu si on clique en dehors
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