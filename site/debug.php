<?php
require_once "bd.php";
$bdd = getBD();

$email = "test@gmail.com"; // ← remplace par ton vrai email dans la BD

$req = $bdd->prepare("SELECT mail, mdp FROM utilisateur WHERE mail = ?");
$req->execute([$email]);
$client = $req->fetch(PDO::FETCH_ASSOC);

if (!$client) {
    echo "❌ Email introuvable dans la base.";
    exit;
}

echo "✅ Email trouvé.<br>";
echo "Hash en base : <code>" . htmlspecialchars($client['mdp']) . "</code><br><br>";

$mdpTest = "testeur";
if (password_verify($mdpTest, $client['mdp'])) {
    echo "✅ password_verify() : MOT DE PASSE CORRECT";
} else {
    echo "❌ password_verify() : MOT DE PASSE INCORRECT<br>";
    echo "Le hash ne correspond pas au mot de passe '<b>" . htmlspecialchars($mdpTest) . "</b>'<br><br>";
    echo "Voici le bon hash à mettre dans ta BD : <br><code>" . password_hash($mdpTest, PASSWORD_DEFAULT) . "</code>";
}
?>