# Système de Permissions API REST Framework

## Vue d'ensemble

Ce projet utilise un système de permissions granulaires basé sur les rôles pour contrôler l'accès aux endpoints API REST Framework.

## Architecture des Permissions

### Fichiers impliqués:

- **`permissions.py`**: Contient les classes de permissions pour chaque ViewSet
- **`views.py`**: ViewSets utilisant les permissions granulaires
- **`management/commands/init_groups.py`**: Commande pour initialiser les groupes Django

## Rôles et Permissions

### 1. **ADMIN** (Administrateur)

- **Accès**: Complet à tous les endpoints
- **Actions autorisées**: CREATE, READ, UPDATE, DELETE sur toutes les ressources
- **Assignation**: Utilisateurs avec `is_superuser=True` OU dans le groupe 'ADMIN'

### 2. **TRAVAILLEUR** / **MANAGER** / **AGENT** (Travailleurs)

- **Clients**:
  - ✓ Lecture (voir tous les clients)
  - ✗ Création/Modification/Suppression
- **Batiments, Niveaux, TypeBureau**:
  - ✓ Lecture seule
  - ✗ Création/Modification/Suppression (admin seulement)
- **Bureaux**:
  - ✓ Lecture seule
  - ✗ Création/Modification/Suppression
- **Réservations**:
  - ✓ Lecture de toutes les réservations
  - ✓ Création (peuvent créer pour d'autres clients)
  - ✗ Modification/Suppression
- **Contrats**:
  - ✓ Lecture de tous les contrats
  - ✓ Création (peuvent créer pour d'autres clients)
  - ✗ Modification/Suppression
- **Locations**:
  - ✓ Lecture et création
  - ✗ Modification/Suppression
- **Paiements**:
  - ✓ Lecture et création
  - ✗ Modification/Suppression (admin seulement)

### 3. **CLIENT** (Personnel/Clients)

- **Clients (profil)**:
  - ✓ Créer son propre profil
  - ✓ Modifier son propre profil
  - ✗ Voir/modifier les autres profils
- **Batiments, Niveaux, TypeBureau**:
  - ✗ Pas d'accès
- **Bureaux**:
  - ✓ Voir tous les bureaux (incluant les disponibles)
  - ✗ Création/Modification/Suppression
- **Réservations**:
  - ✓ Créer ses propres réservations
  - ✓ Voir ses propres réservations
  - ✗ Voir/modifier celles d'autres clients
- **Contrats**:
  - ✓ Créer ses propres contrats
  - ✓ Voir/modifier ses propres contrats
  - ✗ Voir/modifier ceux d'autres clients
- **Locations**:
  - ✗ Pas d'accès (gérées par les travailleurs/admin)
- **Paiements**:
  - ✓ Voir ses propres paiements
  - ✗ Création/Modification/Suppression

## Initialisation des Groupes

### Première exécution:

```bash
python manage.py init_groups
```

Cela crée les groupes Django suivants avec les permissions appropriées:

- ADMIN
- TRAVAILLEUR
- MANAGER
- AGENT
- CLIENT

### Assignation d'utilisateurs aux groupes:

```python
from django.contrib.auth.models import User, Group

user = User.objects.get(username='nomutilisateur')
group = Group.objects.get(name='TRAVAILLEUR')
user.groups.add(group)
```

## Détection du Rôle

Le système détecte le rôle de l'utilisateur dans cet ordre:

1. **is_superuser**: Si `True`, role = ADMIN
2. **client_profile.role**: Utilise le champ `role` du modèle `Client`
3. **Groupes Django**: Cherche dans les groupes assignés à l'utilisateur
4. **Défaut**: Pas de rôle assigné

## Comment ça fonctionne

### Flux de vérification des permissions:

1. **has_permission()**: Vérifie si l'utilisateur peut accéder au ViewSet en général
   - Récupère le rôle de l'utilisateur
   - Vérifie si la méthode HTTP est autorisée pour ce rôle
   - Retourne True/False

2. **has_object_permission()**: Vérifie si l'utilisateur peut accéder à un objet spécifique
   - Pour les clients: Vérifie que c'est son propre objet (client_id, reservation_id, etc.)
   - Pour les travailleurs: Accès lecture seule
   - Pour les admins: Accès complet

### Exemple: ReservationViewSet

```python
class ReservationPermission(BaseRolePermission):
    def has_permission(self, request, view):
        role = self.get_user_role(request)

        if role == ADMIN_ROLE:
            return True

        if role in WORKER_ROLES:
            # Peuvent lire et créer, pas modifier/supprimer
            return request.method in ('GET', 'HEAD', 'OPTIONS', 'POST')

        if role in CLIENT_ROLES:
            # Peuvent créer et lire
            return request.method in ('GET', 'HEAD', 'OPTIONS', 'POST')

        return False

    def has_object_permission(self, request, view, obj):
        role = self.get_user_role(request)

        if role == ADMIN_ROLE:
            return True

        if role in WORKER_ROLES:
            # Peuvent seulement lire
            return request.method in SAFE_METHODS

        if role in CLIENT_ROLES:
            # Peuvent lire seulement leurs propres réservations
            user_client = getattr(request.user, 'client_profile', None)
            if user_client and obj.client.id == user_client.id:
                return request.method in SAFE_METHODS

        return False
```

## Personnalisation des Permissions

Pour modifier les permissions d'un ViewSet:

1. Ouvrir le fichier `permissions.py`
2. Localiser la classe de permission correspondante (ex: `ClientPermission`)
3. Modifier les méthodes `has_permission()` et/ou `has_object_permission()`
4. Les changements sont appliqués immédiatement (pas besoin de migration)

### Exemple: Permettre aux clients de voir les batiments

```python
class BatimentPermission(BaseRolePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        role = self.get_user_role(request)

        if role == ADMIN_ROLE:
            return True

        if role in WORKER_ROLES:
            return request.method in SAFE_METHODS

        if role in CLIENT_ROLES:  # NOUVEAU: Ajouter cette ligne
            return request.method in SAFE_METHODS  # Lecture seule

        return False
```

## Tests de Permissions

### Vérifier les permissions d'un utilisateur:

```python
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from gestionBatiment.permissions import ClientPermission

user = User.objects.get(username='test_client')
factory = APIRequestFactory()
request = factory.get('/api/clients/')
request.user = user

permission = ClientPermission()
print(permission.has_permission(request, None))  # True/False
```

## Points importants

⚠️ **Important**:

- Les permissions sont contrôlées par les classes personnalisées, **pas seulement** par les permissions Django standard
- Même si un utilisateur a une permission Django, la classe de permission peut la refuser
- Les groupes Django sont là pour l'organisation, les vraies permissions sont dans le code

## Dépannage

### Les clients ne peuvent pas créer leur profil?

→ Vérifier que `ClientPermission` autorise POST pour CLIENT_ROLES

### Les travailleurs voient trop/pas assez de données?

→ Vérifier la méthode `get_queryset()` du ViewSet correspondant

### Les permissions ne s'appliquent pas?

→ Vérifier que le ViewSet utilise la bonne classe de permission dans `permission_classes`

## Endpoints utiles

- `GET /api/clients/` - Voir les clients (selon les permissions)
- `POST /api/clients/` - Créer un client (clients peuvent créer leur profil)
- `GET /api/bureaux/disponibles` - Voir les bureaux disponibles
- `POST /api/reservations/` - Créer une réservation
- `GET /api/mes-reservations` - Voir ses réservations (endpoint personnalisé)
- `GET /api/mes-contrats` - Voir ses contrats (endpoint personnalisé)
- `GET /api/mes-paiements` - Voir ses paiements (endpoint personnalisé)

---

**Dernière mise à jour**: 2024
**Auteur**: Système de gestion de bâtiments
