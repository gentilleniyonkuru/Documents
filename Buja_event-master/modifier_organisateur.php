<?php
$host = "localhost";
$user = "root";
$pass = "";
$db   = "gestion_evenements";

$conn = mysqli_connect($host, $user, $pass, $db);
if (!$conn) {
    die("Erreur de connexion : " . mysqli_connect_error());
}

// Vérifier si un ID est passé
if (!isset($_GET['id'])) {
    die("Erreur : Aucun ID spécifié.");
}

$id = intval($_GET['id']);

// --- Mise à jour ---
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nom       = mysqli_real_escape_string($conn, $_POST['nom']);
    $email     = mysqli_real_escape_string($conn, $_POST['email']);
    $telephone = mysqli_real_escape_string($conn, $_POST['telephone']);
    $role      = mysqli_real_escape_string($conn, $_POST['role']);

    $sql = "UPDATE organisateurs 
            SET nom=?, email=?, telephone=?, role=? 
            WHERE id=?";
    $stmt = mysqli_prepare($conn, $sql);
    mysqli_stmt_bind_param($stmt, "ssssi", $nom, $email, $telephone, $role, $id);

    if (mysqli_stmt_execute($stmt)) {
        echo "<p style='color:green;'>✅ Organisateur mis à jour avec succès.</p>";
        echo "<p><a href='liste_organisateurs.php'>↩ Retour à la liste</a></p>";
        exit;
    } else {
        echo "<p style='color:red;'>Erreur lors de la mise à jour : " . mysqli_error($conn) . "</p>";
    }
}

// --- Récupération des infos ---
$sql = "SELECT id, nom, email, telephone, role FROM organisateurs WHERE id=?";
$stmt = mysqli_prepare($conn, $sql);
mysqli_stmt_bind_param($stmt, "i", $id);
mysqli_stmt_execute($stmt);
$result = mysqli_stmt_get_result($stmt);

if (mysqli_num_rows($result) == 0) {
    die("❌ Organisateur introuvable.");
}

$row = mysqli_fetch_assoc($result);
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Modifier organisateur</title>
<style>
    body {font-family: Arial; background:#f4f4f9; padding:20px;}
    h1 {color:#2c3e50;}
    form {background:white; padding:20px; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.1); max-width:400px;}
    label {display:block; margin-top:10px; font-weight:bold;}
    input, select {width:100%; padding:8px; margin-top:5px; border:1px solid #ccc; border-radius:5px;}
    button {margin-top:15px; padding:10px 15px; border:none; background:#27ae60; color:white; font-weight:bold; border-radius:6px; cursor:pointer;}
    button:hover {background:#2ecc71;}
</style>
</head>
<body>

<h1>✏ Modifier organisateur</h1>

<form method="post" action="">
    <label for="nom">Nom :</label>
    <input type="text" name="nom" id="nom" value="<?= htmlspecialchars($row['nom']) ?>" required>

    <label for="email">Email :</label>
    <input type="email" name="email" id="email" value="<?= htmlspecialchars($row['email']) ?>" required>

    <label for="telephone">Téléphone :</label>
    <input type="tel" name="telephone" id="telephone" value="<?= htmlspecialchars($row['telephone']) ?>" required>

    <label for="role">Rôle :</label>
    <select name="role" id="role" required>
        <option value="Coordinateur" <?= ($row['role']=="Coordinateur"?"selected":"") ?>>Coordinateur</option>
        <option value="Animateur" <?= ($row['role']=="Animateur"?"selected":"") ?>>Animateur</option>
        <option value="Technicien" <?= ($row['role']=="Technicien"?"selected":"") ?>>Technicien</option>
        <option value="Logistique" <?= ($row['role']=="Logistique"?"selected":"") ?>>Logistique</option>
    </select>

    <button type="submit">💾 Enregistrer</button>
</form>

<p><a href="liste_organisateurs.php">↩ Retour à la liste</a></p>

</body>
</html>
