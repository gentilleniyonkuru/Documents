<?php
session_start();
if (!isset($_SESSION['admin'])) {
    header("Location: login_admin.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Tableau de Bord - Gestion des Événements</title>
<style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        height: 100vh;
        background: #f4f4f9;
    }
    /* Sidebar */
    .sidebar {
        width: 250px;
        background: #2c3e50;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 20px;
    }
    .sidebar h2 {
        margin: 0;
        font-size: 20px;
        text-align: center;
    }
    .sidebar p {
        text-align: center;
        margin: 10px 0;
        font-size: 14px;
        color: #ccc;
    }
    .sidebar a {
        display: block;
        padding: 12px;
        margin: 8px 0;
        text-decoration: none;
        color: white;
        background: #34495e;
        border-radius: 6px;
        text-align: center;
        transition: 0.3s;
    }
    .sidebar a:hover {
        background: #1abc9c;
    }
    .logout {
        background: #e74c3c !important;
    }
    .logout:hover {
        background: #c0392b !important;
    }

    /* Contenu principal */
    .main {
        flex: 1;
        padding: 40px;
        overflow-y: auto;
    }
    .main h1 {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 30px;
    }
    .container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        max-width: 1200px;
        margin: auto;
    }
    .card {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    .card:hover {
        transform: scale(1.05);
    }
    .card h2 {
        color: #2c3e50;
        margin-bottom: 15px;
    }
    .card p {
        color: #555;
        margin-bottom: 20px;
    }
    .btn {
        display: inline-block;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        color: white;
    }
    .participants { background: #3498db; }
    .participants:hover { background: #2980b9; }
    .evenements { background: #27ae60; }
    .evenements:hover { background: #219150; }
    .organisateurs { background: #e67e22; }
    .organisateurs:hover { background: #d35400; }
</style>
</head>
<body>

<!-- Sidebar -->
<div class="sidebar">
    <div>
        <h2>👑 Admin</h2>
        <p>Bienvenue, <strong><?= $_SESSION['admin'] ?></strong> 👋</p>
        <a href="dashboard.php">🏠 Tableau de bord</a>
        <a href="liste_participants.php">👤 Participants</a>
        <a href="liste_evenements.php">📅 Événements</a>
        <a href="liste_organisateurs.php">👔 Organisateurs</a>
    </div>
    <a href="logout.php" class="logout">🚪 Se déconnecter</a>
</div>

<!-- Contenu principal -->
<div class="main">
    <h1>📊 Tableau de Bord - Gestion des Événements</h1>
    <div class="container">
        <!-- Participants -->
        <div class="card">
            <h2>👤 Participants</h2>
            <p>Voir, ajouter, modifier ou supprimer les participants.</p>
            <a href="liste_participants.php" class="btn participants">Accéder</a>
        </div>

        <!-- Événements -->
        <div class="card">
            <h2>📅 Événements</h2>
            <p>Gérer la liste des événements organisés.</p>
            <a href="liste_evenements.php" class="btn evenements">Accéder</a>
        </div>

        <!-- Organisateurs -->
        <div class="card">
            <h2>👔 Organisateurs</h2>
            <p>Administrer les organisateurs responsables.</p>
            <a href="liste_organisateurs.php" class="btn organisateurs">Accéder</a>
        </div>
    </div>
</div>

</body>
</html>
