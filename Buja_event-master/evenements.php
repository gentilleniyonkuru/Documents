<?php
session_start();
include '../connexion.php';

if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit();
}

// Ajouter un événement
if (isset($_POST['ajouter'])) {
    $id_client = $_POST['id_client'];
    $titre = $_POST['titre'];
    $description = $_POST['description'];
    $date = $_POST['date_evenement'];
    $lieu = $_POST['lieu'];
    mysqli_query($conn, "INSERT INTO evenements (id_client, titre, description, date_evenement, lieu) 
                         VALUES ($id_client,'$titre','$description','$date','$lieu')");
}

// Supprimer un événement
if (isset($_GET['delete'])) {
    $id = $_GET['delete'];
    mysqli_query($conn, "DELETE FROM evenements WHERE id=$id");
}

// Clients pour la liste déroulante
$clients = mysqli_query($conn, "SELECT * FROM clients");
// Récupérer les événements
$result = mysqli_query($conn, "SELECT e.*, c.nom, c.prenom FROM evenements e 
                                JOIN clients c ON e.id_client=c.id");
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Gestion Événements</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<header><h1>Gestion des Événements</h1></header>
<nav>
    <a href="dashboard.php">🏠 Dashboard</a>
    <a href="clients.php">👥 Clients</a>
    <a href="logout.php">🚪 Déconnexion</a>
</nav>
<div class="container">
    <h2>Ajouter un événement</h2>
    <form method="post">
        <select name="id_client" required>
            <option value="">-- Choisir un client --</option>
            <?php while ($c = mysqli_fetch_assoc($clients)) { ?>
                <option value="<?= $c['id'] ?>"><?= $c['nom']." ".$c['prenom'] ?></option>
            <?php } ?>
        </select>
        <input type="text" name="titre" placeholder="Titre" required>
        <textarea name="description" placeholder="Description"></textarea>
        <input type="date" name="date_evenement" required>
        <input type="text" name="lieu" placeholder="Lieu" required>
        <button type="submit" name="ajouter">Ajouter</button>
    </form>

    <h2>Liste des événements</h2>
    <table>
        <tr><th>ID</th><th>Client</th><th>Titre</th><th>Description</th><th>Date</th><th>Lieu</th><th>Action</th></tr>
        <?php while ($row = mysqli_fetch_assoc($result)) { ?>
        <tr>
            <td><?= $row['id'] ?></td>
            <td><?= $row['nom']." ".$row['prenom'] ?></td>
            <td><?= $row['titre'] ?></td>
            <td><?= $row['description'] ?></td>
            <td><?= $row['date_evenement'] ?></td>
            <td><?= $row['lieu'] ?></td>
            <td><a href="?delete=<?= $row['id'] ?>">Supprimer</a></td>
        </tr>
        <?php } ?>
    </table>
</div>
</body>
</html>
