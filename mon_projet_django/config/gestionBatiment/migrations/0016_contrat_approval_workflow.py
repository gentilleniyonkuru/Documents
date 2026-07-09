# Generated migration for contract approval workflow

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestionBatiment", "0015_remove_batiment_periodicite"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="contrat",
            name="periodicite",
            field=models.CharField(
                choices=[
                    ("MENSUEL", "Mensuel"),
                    ("TRIMESTRIEL", "Trimestriel"),
                    ("SEMESTRIEL", "Semestriel"),
                ],
                default="MENSUEL",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="contrat",
            name="statut_approbation",
            field=models.CharField(
                choices=[
                    ("DRAFT", "Brouillon"),
                    ("PENDING", "En attente"),
                    ("ACCEPTED", "Accepté"),
                    ("REJECTED", "Refusé"),
                ],
                default="DRAFT",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="contrat",
            name="approved_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contrats_approved",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contrat",
            name="approved_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contrat",
            name="rejection_reason",
            field=models.TextField(blank=True, null=True),
        ),
    ]
