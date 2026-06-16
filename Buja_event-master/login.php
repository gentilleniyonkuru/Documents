<?php
session_start();
include 'connexion.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST['email'];
    $password = md5($_POST['password']);

    $sql = "SELECT * FROM utilisateurs WHERE email='$email' AND mot_de_passe='$password'";
    $result = mysqli_query($conn, $sql);

    if (mysqli_num_rows($result) == 1) {
        $_SESSION['user'] = mysqli_fetch_assoc($result);
        header("Location: dashboard.php");
        exit();
    } else {
        $error = "❌ Email ou mot de passe incorrect.";
    }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Connexion Admin</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header><h1>Buja Event - Admin</h1></header>
    <div class="container">
        <h2>Connexion</h2>
        <form method="post">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Mot de passe" required>
            <button type="submit">Se connecter</button>
            <?php if(isset($error)) echo "<p style='color:red'>$error</p>"; ?>
        </form>
    </div>
</body>
</html>
