<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
        <link href="inscription.css" rel="stylesheet" />
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>


</head>
<body>
<div class="connexion">
<h1> Creez votre compte </h2>
<form  id="loginForm">
<input type="text" id="pseudo" name="pseudo" placeholder="Quel est votre pseudo" required>
<input type="text" id="mail" name="mail" placeholder="Adresse email" required>
<input type="password" id="password" name="password" placeholder="Mot de Passe" required>
<input type='submit' value="S'inscrire">
<div id="message"></div>
</form>
<a href="connexion.php">Vous avez deja un compte ? Se connecter</a>
</div>

    <script>
    $(document).ready(function(){
        $('#loginForm').on('submit', function(e){
            e.preventDefault();
            $.ajax({
                url: 'inscription.php',
                type: 'POST',
                data: {

                    pseudo: $('#pseudo').val(),
                    password: $('#password').val(),
                    mail:$("#mail").val()
                },
            success: function(response) {
    if (response.trim() === '1') { 
        window.location.href = 'home.php';
    } else {
        $('#message').text('Pseudo ou email déjà utilisé');
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