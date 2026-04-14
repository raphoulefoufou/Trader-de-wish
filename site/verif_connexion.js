$(document).ready(function(){
    $("#send").on("click", function(e){
        e.preventDefault();
        var email = $("input[name='mail']").val().trim();
        var mdp   = $("input[name='mdp']").val().trim();

        if (email === "" || mdp === "") {
            alert("Veuillez remplir tous les champs.");
            return;
        }

        $.ajax({
            url: "check_email.php",
            type: "POST",
            data: { mail: email, mdp: mdp },
            dataType: "json",
            success: function(result){
                if (result.exist && result.valid) {
                    // Connexion réussie
                    $("body").append("<p style='color:green;'>Connexion réussie, redirection en cours...</p>");
                    setTimeout(function(){
                        window.location.href = "accueil.php";
                    }, 2000);
                } else if (result.exist && !result.valid) {
                    // Email correct mais mauvais mot de passe
                    alert("Mot de passe incorrect, veuillez réessayer.");
                } else {
                    // Email introuvable
                    alert("Aucun compte trouvé avec cet email.");
                }
            },
            error: function(){
                alert("Erreur serveur, veuillez réessayer.");
            }
        });
    });
});