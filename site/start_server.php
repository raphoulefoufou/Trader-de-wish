<?php
session_start();
header('Content-Type: application/json');

// Vérification que l'utilisateur est bien connecté
if (empty($_SESSION['id'])) {
    echo json_encode(["success" => false, "message" => "Non autorisé"]);
    exit;
}

// Chemin vers server.js (même dossier que ce fichier)
$serverPath = __DIR__ . '\\server.js';

if (!file_exists($serverPath)) {
    echo json_encode(["success" => false, "message" => "server.js introuvable : " . $serverPath]);
    exit;
}

// Vérifie si le port 3000 est déjà utilisé (Windows)
$check = shell_exec("netstat -ano | findstr :3000");
if ($check && strpos($check, '3000') !== false) {
    echo json_encode(["success" => true, "message" => "Serveur déjà en cours"]);
    exit;
}

// Lance node server.js en arrière-plan sur Windows avec popen/START
$cmd = 'start /B node "' . __DIR__ . '\\server.js"';
pclose(popen($cmd, 'r'));

sleep(2); // Laisse le temps au serveur de démarrer

echo json_encode(["success" => true, "message" => "Serveur démarré"]);
exit;
?>