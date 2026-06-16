<?php
session_start();
$host = "localhost";
$user = "root";
$pass = "";
$db   = "gestion_evenements";

$conn = mysqli_connect($host, $user, $pass, $db);

if (!$conn) {
    die("Erreur de connexion : " . mysqli_connect_error());
}

$message = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    $sql = "SELECT * FROM admins WHERE username=?";
    $stmt = mysqli_prepare($conn, $sql);
    mysqli_stmt_bind_param($stmt, "s", $username);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);

    if ($row = mysqli_fetch_assoc($result)) {
        // Comparaison directe (mot de passe en clair)
        if ($password === $row['password']) {
            $_SESSION['admin'] = $row['username'];
            header("Location: dashboard.php");
            exit;
        } else {
            $message = "❌ Mot de passe incorrect.";
        }
    } else {
        $message = "❌ Utilisateur introuvable.";
    }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Login Admin</title>
<style>
body{font-family:Arial;background:#f4f4f9;display:flex;justify-content:center;align-items:center;height:100vh;}
form{background:#fff;padding:20px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.2);width:300px;}
h2{text-align:center;color:#2c3e50;}
input{width:100%;padding:10px;margin:10px 0;border:1px solid #ddd;border-radius:5px;}
button{width:100%;padding:10px;background:#2c3e50;color:white;border:none;border-radius:5px;font-weight:bold;cursor:pointer;}
button:hover{background:#34495e;}
p{color:red;text-align:center;}
</style>
</head>
<body>
<form method="POST">
    <h2>🔐 Admin Login</h2>
    <input type="text" name="username" placeholder="Nom d'utilisateur" required>
    <input type="password" name="password" placeholder="Mot de passe" required>
    <button type="submit">Se connecter</button>
    <p><?= $message ?></p>
</form>
</body>
</html>
