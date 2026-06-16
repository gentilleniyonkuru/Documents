<?php
// --- Connexion ---
$host = "localhost";
$user = "root";
$pass = "";
$db   = "gestion_evenements";
$conn = mysqli_connect($host, $user, $pass, $db);
if (!$conn) { die("Erreur de connexion : " . mysqli_connect_error()); }

// Petite fonction pour échapper l'affichage HTML
function e($str) { return htmlspecialchars($str ?? "", ENT_QUOTES, 'UTF-8'); }

// --- Soumission du formulaire (UPDATE) ---
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $id    = isset($_POST['id']) ? (int)$_POST['id'] : 0;
    $titre = $_POST['titre'] ?? '';
    $date  = $_POST['date_event'] ?? '';
    $lieu  = $_POST['lieu'] ?? '';
    $desc  = $_POST['description'] ?? '';

    // Requête préparée pour éviter l'injection SQL
    $stmt = mysqli_prepare($conn, "UPDATE evenements SET titre=?, date_event=?, lieu=?, description=? WHERE id=?");
    mysqli_stmt_bind_param($stmt, "ssssi", $titre, $date, $lieu, $desc, $id);
    if (mysqli_stmt_execute($stmt)) {
        // Retour à la liste avec un flag de succès (évite le re-post en rafraîchissant)
        header("Location: liste_evenements.php?updated=1");
        exit;
    } else {
        $err = "Erreur lors de la mise à jour : " . mysqli_error($conn);
    }
    mysqli_stmt_close($stmt);
}

// --- Récupération des données à modifier ---
$id = isset($_GET['id']) ? (int)$_GET['id'] : (isset($id) ? (int)$id : 0);
if ($id <= 0) { die("ID invalide."); }

$stmt = mysqli_prepare($conn, "SELECT id, titre, date_event, lieu, description FROM evenements WHERE id=? LIMIT 1");
mysqli_stmt_bind_param($stmt, "i", $id);
mysqli_stmt_execute($stmt);
$res = mysqli_stmt_get_result($stmt);
$event = mysqli_fetch_assoc($res);
mysqli_stmt_close($stmt);

if (!$event) { die("Événement introuvable."); }
?>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Modifier un événement</title>
<style>
    body {font-family: Arial, sans-serif; background:#f4f4f9; padding:20px;}
    nav {margin-bottom:20px; background:#2c3e50; padding:10px; border-radius:6px;}
    nav a {color:#fff; text-decoration:none; margin:0 10px; font-weight:bold;}
    nav a:hover {text-decoration:underline;}
    h1 {color:#2c3e50; text-align:center; margin-bottom:16px;}
    .card {
        max-width: 600px; margin: 0 auto; background:#fff; padding:20px;
        border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.1);
    }
    label {display:block; font-weight:bold; margin-top:12px;}
    input, textarea {
        width:100%; padding:10px; margin-top:6px; border:1px solid #ccc; border-radius:6px;
    }
    textarea {min-height:120px; resize:vertical;}
    .actions {display:flex; gap:10px; margin-top:16px;}
    .btn {display:inline-block; padding:10px 14px; border-radius:6px; text-decoration:none; font-weight:bold; border:none; cursor:pointer;}
    .btn.save {background:#27ae60; color:#fff;}
    .btn.save:hover {background:#2ecc71;}
    .btn.cancel {background:#c0392b; color:#fff;}
    .btn.cancel:hover {background:#e74c3c;}
    .alert {max-width:600px; margin:0 auto 16px; padding:12px; border-radius:6px;}
    .alert.error {background:#fdecea; color:#b71c1c; border:1px solid #f5c6cb;}
</style>
</head>
<body>
    <!-- Menu global -->
    <nav>
        <a href="liste_participants.php">👤 Participants</a>
        <a href="liste_evenements.php">📅 Événements</a>
        <a href="liste_organisateurs.php">👔 Organisateurs</a>
    </nav>

    <h1>✏ Modifier l'événement</h1>

    <?php if (!empty($err)): ?>
        <div class="alert error"><?= e($err) ?></div>
    <?php endif; ?>

    <div class="card">
        <form method="post">
            <input type="hidden" name="id" value="<?php echo e($event['id']); ?>">

            <label for="titre">Titre</label>
            <input type="text" id="titre" name="titre" value="<?php echo e($event['titre']); ?>" required>

            <label for="date_event">Date</label>
            <input type="date" id="date_event" name="date_event" value="<?php echo e($event['date_event']); ?>" required>

            <label for="lieu">Lieu</label>
            <input type="text" id="lieu" name="lieu" value="<?php echo e($event['lieu']); ?>" required>

            <label for="description">Description</label>
            <textarea id="description" name="description"><?php echo e($event['description']); ?></textarea>

            <div class="actions">
                <button type="submit" class="btn save">💾 Enregistrer</button>
                <a class="btn cancel" href="liste_evenements.php">↩ Annuler</a>
            </div>
        </form>
    </div>
</body>
</html>
<?php mysqli_close($conn); ?>
