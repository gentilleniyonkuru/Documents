"""
Commande Django pour envoyer des rappels de paiement en retard
Usage: python manage.py send_payment_reminders
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from gestionBatiment.email_notifications import (
    send_contract_payment_reminder_email,
    send_payment_reminder_email,
)
from gestionBatiment.models import Contrat, Paiement


class Command(BaseCommand):
    help = "Envoie des emails de rappel pour les paiements en retard"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=7,
            help="Nombre de jours après lesquels envoyer un rappel (défaut: 7)",
        )

    def handle(self, *args, **options):
        days = options["days"]

        # Récupérer les paiements en attente depuis plus de X jours
        cutoff_date = timezone.now() - timedelta(days=days)

        paiements_en_retard = Paiement.objects.filter(
            statut="PENDING", created_at__lte=cutoff_date, is_active=True
        )

        count = 0
        for paiement in paiements_en_retard:
            if send_payment_reminder_email(paiement):
                count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Rappel envoyé à {paiement.client.user.get_full_name()}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠ Impossible d'envoyer le rappel à {paiement.client.user.get_full_name()}"
                    )
                )

        contract_count = 0
        thresholds = {
            "MENSUEL": 1,
            "TRIMESTRIEL": 2,
            "SEMESTRIEL": 3,
        }
        today = timezone.now().date()
        contrats = Contrat.objects.filter(
            statut_approbation="ACCEPTED",
            date_paiement__isnull=False,
            is_active=True,
        )

        for contrat in contrats:
            days_before = thresholds.get(contrat.periodicite, 1)
            reminder_date = contrat.date_paiement - timedelta(days=days_before)
            if reminder_date == today:
                if send_contract_payment_reminder_email(contrat):
                    contract_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Rappel de contrat envoyé à {contrat.client.user.get_full_name()}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"⚠ Impossible d'envoyer le rappel de contrat à {contrat.client.user.get_full_name()}"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n{count} rappel(s) de paiement envoyé(s) avec succès!\n{contract_count} rappel(s) de contrat envoyé(s) avec succès!"
            )
        )
