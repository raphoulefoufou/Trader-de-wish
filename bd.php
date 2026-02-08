<?php
function getBD(){
$bdd = new PDO('mysql:host=localhost;dbname=trader;charset=utf8',
            'root',
            '');
return $bdd;
}
?>