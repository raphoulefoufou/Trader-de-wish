<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
       <link rel="stylesheet" href=
"connexion.css" type="text/css"
media="screen" />

</head>
<body>

<div class="connexion">
<form id="connexionform">
    <input type="text" id="mail" name="email" placeholder="Votre adresse email" required>
    <input type="password" id="password" name="password" placeholder="Mot de passe" required>
    <input type="submit" value="Se connecter">
    <div id="message" ></div>
</form>
</div>

<script>
$(document).ready(function(){
    $('#connexionform').on('submit', function(e){
        e.preventDefault();

        $.ajax({
            url: 'connecter.php',
            type: 'POST',
            data: {
                mail: $('#mail').val(),
                password: $('#password').val()
            },
            success: function(response) {
                if (response.trim() === '1') {
                    window.location.href = 'home.php';
                } else {
                    $('#message').text('Email ou mot de passe incorrect');
                }
            },
            error: function() {
                $('#message').text('Erreur serveur');
            }
        });
    });
});
</script>


    
</body>
</html>