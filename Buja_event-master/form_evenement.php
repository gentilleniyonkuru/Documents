<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $conn = mysqli_connect("localhost", "root", "", "gestion_evenements");
    $titre = $_POST['titre'];
    $date  = $_POST['date_event'];
    $lieu  = $_POST['lieu'];
    $desc  = $_POST['description'];

    $sql = "INSERT INTO evenements (titre, date_event, lieu, description) VALUES ('$titre','$date','$lieu','$desc')";
    if (mysqli_query($conn, $sql)) {
        header("Location: liste_evenements.php");
        exit;
    } else {
        echo "Erreur : " . mysqli_error($conn);
    }
}
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Ajouter un événement</title>
<style>
    body{font-family:Arial;background:#f4f4f9;padding:20px;}
    form{max-width:500px;margin:auto;background:white;padding:20px;border-radius:10px;box-shadow:0 2px 6px rgba(0,0,0,0.1);}
    label{font-weight:bold;}
    input,textarea{width:100%;padding:10px;margin:8px 0;border:1px solid #ccc;border-radius:5px;}
    button{background:#27ae60;color:white;border:none;padding:10px 15px;border-radius:5px;cursor:pointer;}
    button:hover{background:#2ecc71;}
</style>
</head>
<body>
<h1>➕ Ajouter un événement</h1>
<form method="post">
    <label>Titre :</label>
    <input type="text" name="titre" required>
    <label>Date :</label>
    <input type="date" name="date_event" required>
    <label>Lieu :</label>
    <input type="text" name="lieu" required>
    <label>Description :</label>
    <textarea name="description"></textarea>
    <button type="submit">💾 Enregistrer</button>
</form>
</body>
</html>
