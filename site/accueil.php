<?php
session_start();
$a = $_SESSION['id'] ?? "";

if ($a == "") {
    echo '<script>
            alert("Veuillez vous connecter avant de consulter cette page");
            window.location.href = "login.php";
          </script>';
    exit;
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Accueil</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background-color: #0f0f0f;
            color: #e0e0e0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h1 { color: #00d4ff; margin-bottom: 30px; }
        #btnActions {
            padding: 14px 30px;
            font-size: 16px;
            font-weight: bold;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
        }
        #btnActions:hover { background: #0056b3; transform: translateY(-2px); }
        #status {
            margin-top: 20px;
            font-size: 14px;
            color: #aaa;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>Bienvenue, <?= htmlspecialchars($a) ?> 👋</h1>
    <button id="btnActions">📈 Voir les actions</button>
    <p id="status"></p>

    <script>
        document.getElementById("btnActions").addEventListener("click", function() {
            document.getElementById("status").innerText = "Démarrage du serveur...";

            fetch("start_server.php")
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById("status").innerText = "Serveur démarré ! Redirection...";
                        setTimeout(function(){
                            window.open("http://localhost:3000", "_blank");
                        }, 1500);
                    } else {
                        document.getElementById("status").innerText = "Erreur : " + data.message;
                    }
                })
                .catch(() => {
                    document.getElementById("status").innerText = "Impossible de contacter le serveur PHP.";
                });
        });
    </script>
</body>
</html>