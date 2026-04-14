<?php session_start();?>
<!DOCTYPE html>
<html lang='fr'>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <script src="https://code.jquery.com/jquery-3.7.1.min.js" ></script>
        <script src="verif_connexion.js"></script>
    </head>
    <body>
        <form method="post" autocomplete="off">
            <p>
                MAIL : <INPUT type="text" name="mail" value=""> <br>
                Mot de passe : <INPUT type="password" name="mdp" value=""> <br>
                <INPUT id="send" type="submit" value="Soumettre">
            </p>
            

    </body>
</html>