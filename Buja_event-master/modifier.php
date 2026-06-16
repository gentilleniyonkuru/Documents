<?php
$host = "localhost";
$user = "root";
$pass = "";
$db   = "gestion_evenements";

$conn = mysqli_connect($host, $user, $pass, $db);

if (!$conn) {
    die("Erreur de connexion : " . mysqli_connect_error());
}

if (isset($_GET['id'])) {
    $id = intval($_GET['id']);

    // --- Mise à jour si formulaire soumis ---
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $nom       = mysqli_real_escape_string($conn, $_POST['nom']);
        $prenom    = mysqli_real_escape_string($conn, $_POST['prenom']);
        $telephone = mysqli_real_escape_string($conn, $_POST['telephone']);
        $email     = mysqli_real_escape_string($conn, $_POST['email']);
        $date      = mysqli_real_escape_string($conn, $_POST['date_evenement']);
        $message   = mysqli_real_escape_string($conn, $_POST['message']);

        $sql = "UPDATE participants 
                SET nom='$nom', prenom='$prenom', telephone='$telephone', 
                    email='$email', date_evenement='$date', message='$message' 
                WHERE id=$id";

        if (mysqli_query($conn, $sql)) {
            echo "<p style='color:green; font-weight:bold;'>✅ Participant modifié avec succès.</p>";
            echo "<p><a href='liste_participants.php'>⬅ Retour à la liste</a></p>";
        } else {
            echo "Erreur : " . mysqli_error($conn);
        }
    } else {
        // --- Charger les infos pour pré-remplir le formulaire ---
        $res = mysqli_query($conn, "SELECT * FROM participants WHERE id=$id");
        $row = mysqli_fetch_assoc($res);
        ?>
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Modifier participant</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f4f4f9;
                    padding: 20px;
                }
                form {
                    max-width: 500px;
                    margin: auto;
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
                }
                h1 {
                    text-align: center;
                    color: #2c3e50;
                }
                label {
                    font-weight: bold;
                }
                input, textarea {
                    width: 100%;
                    padding: 10px;
                    margin: 8px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                button {
                    background: #27ae60;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }
                button:hover {
                    background: #2ecc71;
                }
            </style>
        </head>
        <body>
            <h1>✏ Modifier le participant</h1>
            <form method="post">
                <label>Nom :</label>
                <input type="text" name="nom" value="<?= $row['nom'] ?>" required>

                <label>Prénom :</label>
                <input type="text" name="prenom" value="<?= $row['prenom'] ?>" required>

                <label>Téléphone :</label>
                <input type="text" name="telephone" value="<?= $row['telephone'] ?>" required>

                <label>Email :</label>
                <input type="email" name="email" value="<?= $row['email'] ?>" required>

                <label>Date :</label>
                <input type="date" name="date_evenement" value="<?= $row['date_evenement'] ?>" required>

                <label>Message :</label>
                <textarea name="message" required><?= $row['message'] ?></textarea>

                <button type="submit">💾 Enregistrer</button>
            </form>
        </body>
        </html>
        <?php
    }
} else {
    echo "<p>Aucun ID fourni.</p>";
}

mysqli_close($conn);
?>

