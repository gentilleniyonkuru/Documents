<?php
// Connexion à MySQL
$host = "localhost";
$user = "root";     // change si nécessaire
$pass = "";         // mot de passe MySQL (vide par défaut sous XAMPP)
$db   = "gestion_evenements";

$conn = mysqli_connect($host, $user, $pass, $db);

// Vérification de connexion
if (!$conn) {
    die("Erreur de connexion : " . mysqli_connect_error());
}

// Vérification si formulaire soumis
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nom       = mysqli_real_escape_string($conn, $_POST['name']);
    $prenom    = mysqli_real_escape_string($conn, $_POST['prenom']);
    $telephone = mysqli_real_escape_string($conn, $_POST['number']);
    $email     = mysqli_real_escape_string($conn, $_POST['email']);
    $date      = mysqli_real_escape_string($conn, $_POST['date']);
    $message   = mysqli_real_escape_string($conn, $_POST['message']);

    // Insertion en BDD
    $sql = "INSERT INTO participants (nom, prenom, telephone, email, date_evenement, message)
            VALUES ('$nom', '$prenom', '$telephone', '$email', '$date', '$message')";

    if (mysqli_query($conn, $sql)) {
        echo "<p style='color:green;'>✅ Merci $prenom $nom, votre message a été enregistré avec succès.</p>";
    } else {
        echo "<p style='color:red;'>❌ Erreur : " . mysqli_error($conn) . "</p>";
    }
}

/* --- Nouvelle fonction pour afficher les formulaires envoyés --- */
function afficher_participants($conn) {
    $sql = "SELECT * FROM participants ORDER BY id DESC";
    $result = mysqli_query($conn, $sql);

    if (mysqli_num_rows($result) > 0) {
        echo "<h2>📋 Liste des participants</h2>";
        echo "<table border='1' cellpadding='8' cellspacing='0'>
                <tr>
                    <th>ID</th>
                    <th>Nom</th>
                    <th>Prénom</th>
                    <th>Téléphone</th>
                    <th>Email</th>
                    <th>Date de l'événement</th>
                    <th>Message</th>
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
                  </tr>";
        }
        echo "</table>";
    } else {
        echo "<p>Aucun participant enregistré pour le moment.</p>";
    }
}

// Appel de la fonction pour afficher la liste
afficher_participants($conn);

mysqli_close($conn);
?>
