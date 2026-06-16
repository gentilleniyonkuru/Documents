<?php
$serveur = "localhost";
$utilisateur = "root";
$motdepasse = "";
$basededonnees = "gestion_evenements";
$connexion = mysqli_connect($serveur,$utilisateur,$motdepasse,$basededonnees);
if (!$connexion) {
    die("Connexion échouée: " . mysqli_connect_error());
}else {
    echo "Connexion réussie à la base de données.";
}  
?>