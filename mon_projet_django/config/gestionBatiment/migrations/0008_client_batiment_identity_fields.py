# Generated manually for Client and Batiment identity fields addition

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBatiment', '0007_paiement_annee_paye_mois_paye'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='lieu_naissance',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='nationalite',
            field=models.CharField(max_length=50, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='profession',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='type_piece_identite',
            field=models.CharField(blank=True, choices=[('CNI', "Carte Nationale d'Identité"), ('PASSPORT', 'Passeport'), ('PERMIS', 'Permis de conduire'), ('ACTE_NAISSANCE', 'Acte de naissance'), ('AUTRE', 'Autre')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='numero_piece_identite',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='photo_profil',
            field=models.ImageField(blank=True, null=True, upload_to='clients/photos/'),
        ),
        migrations.AddField(
            model_name='batiment',
            name='proprietaire_adresse',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='batiment',
            name='proprietaire_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='batiment',
            name='proprietaire_nom',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='batiment',
            name='proprietaire_numero_piece',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='batiment',
            name='proprietaire_prenom',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='batiment',
            name='proprietaire_telephone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='CM'),
        ),
        migrations.AddField(
            model_name='batiment',
            name='proprietaire_type_piece',
            field=models.CharField(blank=True, choices=[('CNI', "Carte Nationale d'Identité"), ('PASSPORT', 'Passeport'), ('PERMIS', 'Permis de conduire'), ('ACTE_NAISSANCE', 'Acte de naissance'), ('AUTRE', 'Autre')], max_length=20, null=True),
        ),
    ]
