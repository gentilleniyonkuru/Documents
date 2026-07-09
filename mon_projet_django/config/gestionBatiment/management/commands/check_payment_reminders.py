from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from gestionBatiment.models import Contrat


class Command(BaseCommand):
    help = "Vérifie les dates de paiement et envoie un rappel par email si paiement dans les 24h ou en retard"

    def handle(self, *args, **kwargs):
        aujourdhui = timezone.now().date()
        seuil = aujourdhui + timedelta(days=1)

        contrats = Contrat.objects.filter(
            date_paiement__isnull=False,
            is_active=True,
        ).select_related("client", "client__user")

        total = 0
        for contrat in contrats:
            date_paiement = contrat.date_paiement
            if not date_paiement:
                continue

            # RAPPEL si paiement demain (seuil) ou déjà passé
            if date_paiement == seuil or date_paiement < aujourdhui:
                client = contrat.client
                if not client or not client.user or not client.user.email:
                    continue

                # Vérifier si un paiement validé existe déjà pour ce mois/année sur ce contrat
                # Si date_paiement < aujourd'hui, c'est en retard
                # Sinon c'est dans 24h
                if date_paiement < aujourdhui:
                    sujet = "Rappel : Votre loyer est en retard"
                    message = (
                        f"Bonjour {client.user.first_name},\n\n"
                        f"Votre paiement prévu le {date_paiement.strftime('%d/%m/%Y')} pour le contrat n°{contrat.id} n'a pas été enregistré.\n"
                        "Veuillez régulariser votre situation dans les plus brefs délais.\n\n"
                        "Cordialement."
                    )
                else:
                    sujet = "Rappel : Votre loyer arrive à échéance demain"
                    message = (
                        f"Bonjour {client.user.first_name},\n\n"
                        f"Votre prochain paiement de loyer est prévu le {date_paiement.strftime('%d/%m/%Y')} pour le contrat n°{contrat.id}.\n"
                        "Nous vous invitons à effectuer le paiement dans les plus brefs délais.\n\n"
                        "Cordialement."
                    )

                try:
                    send_mail(
                        subject=sujet,
                        message=message,
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                        recipient_list=[client.user.email],
                        fail_silently=False,
                    )
                    total += 1
                    self.stdout.write(
                        f"Rappel envoyé à {client.user.email} pour contrat {contrat.id}"
                    )
                except Exception as e:
                    self.stderr.write(f"Erreur envoi email contrat {contrat.id} : {e}")

        self.stdout.write(f"Total rappels envoyés : {total}")
