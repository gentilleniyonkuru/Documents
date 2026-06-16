<?php
session_start();
include 'connexion.php';


if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit();
}

// Ajouter un client
if (isset($_POST['ajouter'])) {
    $nom = $_POST['nom'];
    $prenom = $_POST['prenom'];
    $tel = $_POST['telephone'];
    $email = $_POST['email'];
    mysqli_query($conn, "INSERT INTO clients (nom, prenom, telephone, email) 
                         VALUES ('$nom','$prenom','$tel','$email')");
}

// Supprimer un client
if (isset($_GET['delete'])) {
    $id = $_GET['delete'];
    mysqli_query($conn, "DELETE FROM clients WHERE id=$id");
}

// Récupérer tous les clients
$result = mysqli_query($conn, "SELECT * FROM clients");
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Gestion Clients</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<header><h1>Gestion des Clients</h1></header>
<nav>
    <a href="dashboard.php">🏠 Dashboard</a>
    <a href="evenements.php">🎉 Événements</a>
    <a href="logout.php">🚪 Déconnexion</a>
</nav>
<div class="container">
    <h2>Ajouter un client</h2>
    <form method="post">
        <input type="text" name="nom" placeholder="Nom" required>
        <input type="text" name="prenom" placeholder="Prénom" required>
        <input type="text" name="telephone" placeholder="Téléphone" required>
        <input type="email" name="email" placeholder="Email" required>
        <button type="submit" name="ajouter">Ajouter</button>
    </form>

    <h2>Liste des clients</h2>
    <table>
        <tr><th>ID</th><th>Nom</th><th>Prénom</th><th>Téléphone</th><th>Email</th><th>Action</th></tr>
        <?php while ($row = mysqli_fetch_assoc($result)) { ?>
        <tr>
            <td><?= $row['id'] ?></td>
            <td><?= $row['nom'] ?></td>
            <td><?= $row['prenom'] ?></td>
            <td><?= $row['telephone'] ?></td>
            <td><?= $row['email'] ?></td>
            <td><a href="?delete=<?= $row['id'] ?>">Supprimer</a></td>
        </tr>
        <?php } ?>
    </table>
</div>
</body>
</html>
