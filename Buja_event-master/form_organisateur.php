<?php
$host = "localhost";
$user = "root";
$pass = "";
$db   = "gestion_evenements";

$conn = mysqli_connect($host, $user, $pass, $db);
if (!$conn) {
    die("Erreur de connexion : " . mysqli_connect_error());
}

// Traitement du formulaire
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nom       = mysqli_real_escape_string($conn, $_POST['nom']);
    $email     = mysqli_real_escape_string($conn, $_POST['email']);
    $telephone = mysqli_real_escape_string($conn, $_POST['telephone']);
    $role      = mysqli_real_escape_string($conn, $_POST['role']);

    $sql = "INSERT INTO organisateurs (nom, email, telephone, role) 
            VALUES ('$nom', '$email', '$telephone', '$role')";
    
    if (mysqli_query($conn, $sql)) {
        echo "<p style='color:green;'>✅ Organisateur ajouté avec succès.</p>";
        echo "<p><a href='liste_organisateurs.php'>↩ Retour à la liste</a></p>";
    } else {
        echo "<p style='color:red;'>Erreur : " . mysqli_error($conn) . "</p>";
    }
}
mysqli_close($conn);
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Ajouter un organisateur</title>
<style>
    body {font-family: Arial; background:#f4f4f9; padding:20px;}
    h1 {color:#2c3e50;}
    form {background:white; padding:20px; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.1); max-width:400px;}
    label {display:block; margin-top:10px; font-weight:bold;}
    input, select {width:100%; padding:8px; margin-top:5px; border:1px solid #ccc; border-radius:5px;}
    button {margin-top:15px; padding:10px 15px; border:none; background:#2980b9; color:white; font-weight:bold; border-radius:6px; cursor:pointer;}
    button:hover {background:#3498db;}
    a {text-decoration:none; color:#2980b9;}
</style>
</head>
<body>

<h1>➕ Ajouter un organisateur</h1>

<form method="post" action="">
    <label for="nom">Nom :</label>
    <input type="text" name="nom" id="nom" required>

    <label for="email">Email :</label>
    <input type="email" name="email" id="email" required>

    <label for="telephone">Téléphone :</label>
    <input type="tel" name="telephone" id="telephone" required>

    <label for="role">Rôle :</label>
    <select name="role" id="role" required>
        <option value="">-- Choisir un rôle --</option>
        <option value="Coordinateur">Coordinateur</option>
        <option value="Animateur">Animateur</option>
        <option value="Technicien">Technicien</option>
        <option value="Logistique">Logistique</option>
    </select>

    <button type="submit">Enregistrer</button>
</form>

<p><a href="liste_organisateurs.php">↩ Retour à la liste</a></p>

</body>
</html>
