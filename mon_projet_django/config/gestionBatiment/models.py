from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal
   
class Client(models.Model):
    id = models.AutoField
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    telephone = PhoneNumberField(region='CM', blank=True, null=True)
    addresse = models.CharField(max_length=255, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
    
class Batiment(models.Model):
    id = models.AutoField
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=50)
    nombre_etages = models.IntegerField(default=0)
    date_construction = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nom
    
class Niveau(models.Model):
    id = models.AutoField
    nom = models.CharField(max_length=50)
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name='niveaux')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nom
    
    
class TypeBureau(models.Model):
    id = models.AutoField
    nom = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nom
    
 
class Bureau(models.Model):
    id = models.AutoField
    numero = models.CharField(max_length=20)
    type = models.ForeignKey(TypeBureau, on_delete=models.CASCADE, related_name='bureaux', null=True, blank=True)
    unite = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    espace = models.FloatField(default=0.0)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name='bureaux')
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='bureaux', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.numero
    
    def save(self, *args, **kwargs):
        # Calculer l'espace en fonction du type de bureau
        self.prix = Decimal(str(self.espace)) * self.unite
        super().save(*args, **kwargs)
    

class Reservation(models.Model):
    id = models.AutoField
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    bureau = models.ForeignKey(Bureau, on_delete=models.CASCADE, related_name='reservations')
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reservations')
    
    
    def __str__(self):
        return f"Réservation du {self.date_debut} au {self.date_fin} - {self.client.user.first_name} {self.client.user.last_name}"
    
class Contrat(models.Model):
    
    id = models.AutoField
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='contrat')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contrats')
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Contrat du {self.date_debut} au {self.date_fin} - {self.client.user.first_name} {self.client.user.last_name}"

class Location(models.Model):
    id = models.AutoField
    bureau = models.ForeignKey(Bureau, on_delete=models.CASCADE, related_name='locations')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='locations')
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Location du {self.date_debut} au {self.date_fin} - {self.client.user.first_name} {self.client.user.last_name}"



class Paiement(models.Model):
    class paiementStatus(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        COMPLETED = 'PAID', _('Payé')
        FAILED = 'FAILED', _('Échoué') 
        
        
    id = models.AutoField
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True, blank=True)
    mode= models.CharField(max_length=20, choices=[('CASH', 'Espèces'), ('CARD', 'Carte bancaire'), ('TRANSFER', 'Virement bancaire')], default='CASH')
    location = models.ForeignKey(Bureau, on_delete=models.CASCADE, related_name='paiements')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='paiements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Paiement de {self.montant}€ le {self.date} - {self.client.user.first_name} {self.client.user.last_name}"
 