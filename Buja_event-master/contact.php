<!DOCTYPE html>
<html>
<head>
    <title>BUJA EVENT - CONTACT</title> 
    <meta charset="utf-8">  
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: black;
            color: white;
            line-height: 1.6;
        }
        /* --- HEADER --- */
        header {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #000, #1a1a1a);
        }
        header img.logos {
            width: 150px;
            border-radius: 12px;
        }
        nav {
            margin-top: 20px;
        }
        nav li {
            display: inline-block;
            margin: 0 12px;
            list-style: none;
        }
        nav a {
            text-decoration: none;
            color: white;
            font-weight: bold;
            padding: 8px 14px;
            border-radius: 6px;
            transition: 0.3s;
        }
        nav a:hover {
            background: #27ae60;
        }
        header h1 {
            margin-top: 40px;
            font-size: 32px;
            color: #27ae60;
        }
        header p {
            font-size: 18px;
        }

        /* --- SECTION --- */
        .section {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 60px 20px;
            flex-wrap: wrap;
            gap: 40px;
        }
        .section img {
            max-width: 400px;
            border-radius: 50%;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        }
        .section h2 {
            font-size: 42px;
            color: #27ae60;
            margin-bottom: 20px;
        }
        .section p {
            max-width: 500px;
        }

        /* --- CONTACT --- */
        .contact {
            background: #111;
            padding: 40px 20px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 30px;
        }
        .contact-info {
            max-width: 400px;
        }
        .contact-info h2 {
            color: #27ae60;
        }
        .contact-form {
            background: #1a1a1a;
            padding: 20px;
            border-radius: 10px;
            max-width: 400px;
            width: 100%;
        }
        .contact-form h2 {
            margin-bottom: 15px;
            color: #27ae60;
        }
        .contact-form label {
            display: block;
            margin: 10px 0 5px;
        }
        .contact-form input,
        .contact-form textarea,
        .contact-form button {
            width: 100%;
            padding: 10px;
            margin-bottom: 12px;
            border: none;
            border-radius: 6px;
        }
        .contact-form input,
        .contact-form textarea {
            background: #222;
            color: white;
        }
        .contact-form button {
            background: #27ae60;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }
        .contact-form button:hover {
            background: #2ecc71;
        }

        /* --- FOOTER --- */
        footer {
            background: #000;
            text-align: center;
            padding: 20px;
            border-top: 1px solid #333;
        }
        footer p {
            margin-bottom: 10px;
        }
        footer .icons {
            margin-top: 10px;
        }
        footer .logo {
            width: 30px;
            margin: 0 8px;
            vertical-align: middle;
            transition: 0.3s;
        }
        footer .logo:hover {
            transform: scale(1.2);
        }

        /* --- RESPONSIVE --- */
        @media (max-width: 768px) {
            .section {
                flex-direction: column;
                text-align: center;
            }
            nav li {
                display: block;
                margin: 8px 0;
            }
        }
    </style>
</head>
<body>
    <header>
        <img src="./Image/BujaEventLogo.jpg" class="logos">
        <nav>
            <li><a href="acceuil.html">Accueil</a></li>
            <li><a href="a propos.html">À propos</a></li>
            <li><a href="services.html">Services</a></li>
            <li><a href="galerie.html">Galerie</a></li>
            <li><a href="contact.html">Contact</a></li>
             <li><a href="login_admin.php">connexion</a></li>
        </nav>
        <h1>Transformer vos idées en événements mémorables avec Buja Event!</h1>
        <p>Nous serions ravis de discuter de vos besoins pour votre prochain événement</p>
    </header>

    <section class="section">
        <div>
            <img src="./Image/contact.png" alt="">
        </div>
        <div>
            <h2>Contactez-nous</h2>
            <p>Nous avons hâte d'avoir de vos nouvelles et d'en apprendre davantage sur vos besoins en matière d'événement.<br>
            Notre équipe de professionnels expérimentés est dédiée à fournir des services de planification et de gestion exceptionnels qui surpasseront vos attentes.</p>
        </div>
    </section>

    <section class="contact">
        <div class="contact-info">
            <h2>Informations de contact</h2>
            <ul>
                <li><strong>Adresse:</strong> Rue Ngendandumwe 123, Bujumbura, Burundi</li>
                <li><strong>Téléphone:</strong> +257 71 98 79 35</li>
                <li><strong>Email:</strong> bujaevent@gmail.com</li>
            </ul>
        </div>
        <div class="contact-form">
            <h2>Envoyez-nous un message</h2>
            <form action="form.php" method="post">
                <label for="name">Votre nom</label>
                <input type="text" id="name" name="name" required placeholder="Ex: INTSINZI">

                <label for="prenom">Votre prénom</label>
                <input type="text" id="prenom" name="prenom" required placeholder="Ex: Kim-Chretien">

                <label for="number">Téléphone</label>
                <input type="tel" id="number" name="number" required placeholder="Écrire les nombres seulement">

                <label for="email">Votre email</label>
                <input type="email" id="email" name="email" required placeholder="Ex: exemple@mail.com">

                <label for="date">Date de l'évènement</label>
                <input type="date" id="date" name="date" required>

                <label for="message">Votre message</label>
                <textarea name="message" id="message" rows="5" required></textarea>

                <button type="submit">Envoyer le message</button>
            </form>

            
        </div>
    </section>

    <footer>
        <p>&copy; 2025 Buja Event, Tous droits réservés</p>
        <div class="icons">
            <img src="./Image/download.png" alt="" class="logo">
            <p>+257 71 987 935</p>
            <img src="./Image/face.png" alt="" class="logo">
            <img src="./Image/ig.png" alt="" class="logo">
            <img src="./Image/twit.png" alt="" class="logo">
            <p>: BujaEvent</p>
        </div>
    </footer>
</body>
</html>
