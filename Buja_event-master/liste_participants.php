<?php
session_start();
if (!isset($_SESSION['admin'])) {
    header("Location: login_admin.php");
    exit;
}
?>
<?php
$host = "localhost";
$user = "root";
$pass = "";
$db   = "gestion_evenements";

$conn = mysqli_connect($host, $user, $pass, $db);

if (!$conn) {
    die("Erreur de connexion : " . mysqli_connect_error());
}

// --- Suppression ---
if (isset($_GET['delete'])) {
    $id = intval($_GET['delete']);
    mysqli_query($conn, "DELETE FROM participants WHERE id=$id");
    echo "<p style='color:red; font-weight:bold;'>❌ Participant supprimé avec succès.</p>";
}

// --- Récupération des données ---
$sql = "SELECT * FROM participants ORDER BY id DESC";
$result = mysqli_query($conn, $sql);
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Liste des participants</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #eef1f5;
            margin: 0;
            padding: 0;
        }
        header {
            background: #2c3e50;
            padding: 15px 20px;
        }
        nav a {
            color: white;
            margin-right: 15px;
            text-decoration: none;
            font-weight: bold;
            padding: 8px 12px;
            border-radius: 5px;
            transition: 0.3s;
        }
        nav a:hover {
            background: #34495e;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin: 20px 0;
        }
        table {
            width: 90%;
            margin: auto;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0px 3px 6px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 14px;
            border-bottom: 1px solid #ddd;
            text-align: center;
        }
        th {
            background: #2c3e50;
            color: white;
        }
        tr:hover {
            background: #f1f1f1;
        }
        a.btn {
            padding: 6px 12px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            color: white;
            transition: 0.3s;
        }
        a.edit { background: #27ae60; }
        a.edit:hover { background: #2ecc71; }
        a.delete { background: #c0392b; }
        a.delete:hover { background: #e74c3c; }
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="dashboard.php">🏠 Dashboard</a>
            <a href="liste_participants.php">Participants</a>
            <a href="liste_evenements.php">Événements</a>
            <a href="liste_organisateurs.php">Organisateurs</a>
        </nav>
    </header>

    <h1>📋 Liste des participants</h1>

<?php
if (mysqli_num_rows($result) > 0) {
    echo "<table>
            <tr>
                <th>ID</th>
                <th>Nom</th>
                <th>Prénom</th>
                <th>Téléphone</th>
                <th>Email</th>
                <th>Date de l'événement</th>
                <th>Message</th>
                <th>Actions</th>
            </tr>";
    while ($row = mysqli_fetch_assoc($result)) {
        echo "<tr>
                <td>".$row['id']."</td>
                <td>".$row['nom']."</td>
                <td>".$row['prenom']."</td>
                <td>".$row['telephone']."</td>
                <td>".$row['email']."</td>
                <td>".$row['date_evenement']."</td>
                <td>".$row['message']."</td>
                <td>
                    <a class='btn edit' href='modifier.php?id=".$row['id']."'>✏ Modifier</a> 
                    <a class='btn delete' href='liste_participants.php?delete=".$row['id']."' onclick=\"return confirm('Voulez-vous vraiment supprimer ce participant ?');\">🗑 Supprimer</a>
                </td>
              </tr>";
    }
    echo "</table>";
} else {
    echo "<p style='text-align:center;'>Aucun participant pour le moment.</p>";
}
mysqli_close($conn);
?>
</body>
</html>
