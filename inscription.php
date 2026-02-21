
<?php
    header('Content-Type: text/plain');

include 'bd.php';
$pdo = getBD();

$pseudo = $_POST['pseudo'];
$mdp = $_POST['password'];
$email = $_POST['mail'];

$ok = true; 
$sql = $pdo->prepare("SELECT pseudo, email FROM client");
$sql->execute();
$clients = $sql->fetchAll(PDO::FETCH_ASSOC); 

foreach($clients as $cli) {
    if($pseudo == $cli['pseudo'] || $email == $cli['email']) {
        $ok = false;
        break;
    }
}

if ($ok) {
    $stmt = $pdo->prepare("INSERT INTO client(pseudo, email, mdp) VALUES(:pseudo, :email, :mdp)");
    $stmt->execute([
        "pseudo" => $pseudo,
        "email"  => $email,
        "mdp"    => password_hash($mdp, PASSWORD_DEFAULT)
    ]);
     session_start();
    $_SESSION['client'] = [
        'id'     => $client['id'], // Utile pour tes requêtes SQL plus tard
        'pseudo' => $client['pseudo'], // Ce que tu cherches dans panier.php
        'email'  => $client['email'],
        'monnaie'=> $client['monnaie'],
    ];
    echo '1';


} else {
    echo '0';
}
exit();
?>
