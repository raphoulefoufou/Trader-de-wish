<?php
require_once "bd.php";
session_start();
header('Content-Type: application/json');

$bdd = getBD();

$email = $_POST['mail'] ?? "";
$mdp   = $_POST['mdp'] ?? "";

// Vérification des champs vides
if ($email === "" || $mdp === "") {
    echo json_encode(["exist" => false, "valid" => false]);
    exit;
}

// Récupération de l'utilisateur par email
$req = $bdd->prepare("SELECT mail, mdp FROM utilisateur WHERE mail = ?");
$req->execute([$email]);
$client = $req->fetch(PDO::FETCH_ASSOC);

if ($client) {
    if (password_verify($mdp, $client['mdp'])) {
        // Email + mot de passe corrects → on crée la session
        $_SESSION['id'] = $email;
        echo json_encode(["exist" => true, "valid" => true]);
    } else {
        // Email trouvé mais mot de passe incorrect
        echo json_encode(["exist" => true, "valid" => false]);
    }
} else {
    // Email non trouvé
    echo json_encode(["exist" => false, "valid" => false]);
}
exit;
?>