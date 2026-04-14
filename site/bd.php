<?php 
function getBD(){
    $bdd = new PDO('mysql:host=localhost;port=3306;dbname=trader;charset=utf8',
        'root',
        'root');
    return $bdd;
}
?>