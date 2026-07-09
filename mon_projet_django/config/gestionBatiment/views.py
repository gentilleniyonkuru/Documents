from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail  
from datetime import timedelta
import logging                          

from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError 
from rest_framework.exceptions import ValidationError as DRFValidationError

from .serializers import (
    ClientSerializer, BatimentSerializer, NiveauSerializer, 
    TypeBureauSerializer, BureauSerializer, LocationSerializer,
    ContratSerializer, PaiementSerializer, ReservationSerializer
)
from .models import Client, Batiment, TypeBureau, Bureau, Niveau, Contrat, Location, Paiement, Reservation
from .permissions import (
    ClientPermission, BatimentPermission, NiveauPermission,
    TypeBureauPermission, BureauPermission, ReservationPermission,
    ContratPermission, LocationPermission, PaiementPermission,
    ADMIN_ROLE, WORKER_ROLES, CLIENT_ROLES
)

logger = logging.getLogger(__name__)


class BaseModelViewSet(viewsets.ModelViewSet):
    """Base viewset that converts Django ValidationError into DRF HTTP 400 responses."""

    def _format_django_validation_error(self, exc):
        if hasattr(exc, 'message_dict'):
            return exc.message_dict
        if hasattr(exc, 'error_dict'):
            return {k: v.messages if hasattr(v, 'messages') else v for k, v in exc.error_dict.items()}
        if hasattr(exc, 'messages'):
            return {'detail': exc.messages}
        return {'detail': str(exc)}

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except DjangoValidationError as e:
            raise ValidationError(self._format_django_validation_error(e))

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except DjangoValidationError as e:
            raise ValidationError(self._format_django_validation_error(e))

    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except DjangoValidationError as e:
            raise ValidationError(self._format_django_validation_error(e))
        
    def get_permissions(self):
        if getattr(self, 'permission_classes', None):
            return [permission() for permission in self.permission_classes]
        return [IsAuthenticated()]

    def get_client_profile(self):
        return getattr(self.request.user, 'client_profile', None)

    def get_user_role(self):
        user = self.request.user
        if not user or user.is_anonymous:
            return None
        if user.is_superuser:
            return ADMIN_ROLE

        profile = self.get_client_profile()
        if profile is not None:
            return profile.role

        groups = set(user.groups.values_list('name', flat=True))
        if ADMIN_ROLE in groups:
            return ADMIN_ROLE
        for role in WORKER_ROLES:
            if role in groups:
                return role
        if CLIENT_ROLES and CLIENT_ROLES[0] in groups:
            return CLIENT_ROLES[0]
        return None


# ==================== Vues simples ====================

def hello(request):
    return HttpResponse('<h1>Bienvenue dans la gestion de bâtiments!</h1>')

def index(request):
    batiments = Batiment.objects.all()
    bureaux = Bureau.objects.all()
    context = {
        'batiments': batiments,
        'bureaux': bureaux,
        'nombre_batiments': batiments.count(),
        'nombre_bureaux': bureaux.count(),
    }
    return render(request, 'gestionBatiment/index.html', context)


# ==================== ViewSets API REST ====================

class ClientViewSet(BaseModelViewSet):
   """ViewSet pour gérer les Clients avec email de bienvenue"""
   serializer_class = ClientSerializer
   permission_classes = [ClientPermission]
   ordering = ['user_id']
   

   def get_queryset(self):
        role = self.get_user_role()
        profile = self.get_client_profile()
        base_query = Client.objects.select_related('user')

        if role == ADMIN_ROLE or role in WORKER_ROLES:
            return base_query.all().order_by('user_id')
        if role in CLIENT_ROLES and profile is not None:
            return base_query.filter(id=profile.id)
        
        return Client.objects.none()

   @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='inscription')
   def inscription(self, request):
        if request.user.is_authenticated and self.get_client_profile() is not None:
            return Response(
                {"detail": "Vous avez déjà un profil client créé."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                client = serializer.save(user=request.user)
            else:
                client = serializer.save()
            
            # --- Email de Bienvenue après inscription réussie ---
            try:
                if client.user and client.user.email:
                    send_mail(
                        subject="Bienvenue sur notre plateforme de gestion !",
                        message=f"Bonjour,\n\nVotre profil client a été créé avec succès.\nVous pouvez dès à présent réserver vos bureaux et gérer vos contrats en ligne.\n\nMerci de votre confiance,\nL'équipe.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[client.user.email],
                        fail_silently=False,
                    )
            except Exception as e:
                logger.error(f"Erreur d'envoi de l'email de bienvenue pour le client {client.id}: {str(e)}")
            # ----------------------------------------------------

            return Response(self.get_serializer(client).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   @action(detail=False, methods=['get'], url_path='mon-profil')
   def mon_profil(self, request):
        profile = self.get_client_profile()
        if profile is None:
            return Response(
                {"has_profile": False, "detail": "Aucun profil client trouvé pour cet utilisateur."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(profile)
        data = serializer.data
        data["has_profile"] = True
        return Response(data, status=status.HTTP_200_OK)
    
    
class BatimentViewSet(BaseModelViewSet):
    """ViewSet pour gérer les Bâtiments"""
    serializer_class = BatimentSerializer
    permission_classes = [BatimentPermission]

    def get_queryset(self):
        role = self.get_user_role()
        if role == ADMIN_ROLE or role in WORKER_ROLES:
            return Batiment.objects.all()
        return Batiment.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='actifs')
    def actifs(self, request):
        batiments = Batiment.objects.filter(is_active=True)
        serializer = self.get_serializer(batiments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='statistiques')
    def statistiques(self, request, pk=None):
        batiment = self.get_object()
        return Response({
            'id': batiment.id,
            'nom': batiment.nom,
            'taux_occupation': batiment.taux_occupation,
            'revenues_totaux': batiment.revenues_totaux,
            'nombre_bureaux': batiment.bureaux.count(),
        })


class NiveauViewSet(BaseModelViewSet):
    """ViewSet pour gérer les Niveaux"""
    serializer_class = NiveauSerializer
    permission_classes = [NiveauPermission]

    def get_queryset(self):
        role = self.get_user_role()
        if role == ADMIN_ROLE or role in WORKER_ROLES:
            return Niveau.objects.all()
        return Niveau.objects.none()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], url_path='par-batiment/(?P<batiment_id>[0-9]+)')
    def par_batiment(self, request, batiment_id=None):
        niveaux = Niveau.objects.filter(batiment_id=batiment_id, is_active=True)
        serializer = self.get_serializer(niveaux, many=True)
        return Response(serializer.data)


class TypeBureauViewSet(BaseModelViewSet):
    """ViewSet pour gérer les Types de Bureau"""
    serializer_class = TypeBureauSerializer
    permission_classes = [TypeBureauPermission]

    def get_queryset(self):
        role = self.get_user_role()
        if role == ADMIN_ROLE or role in WORKER_ROLES:
            return TypeBureau.objects.all()
        return TypeBureau.objects.none()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], url_path='actifs')
    def actifs(self, request):
        types_bureau = TypeBureau.objects.filter(is_active=True)
        serializer = self.get_serializer(types_bureau, many=True)
        return Response(serializer.data)


class BureauViewSet(BaseModelViewSet):
    """ViewSet pour gérer les Bureaux"""
    serializer_class = BureauSerializer
    permission_classes = [BureauPermission]

    def get_queryset(self):
        user = self.request.user
        profile = self.get_client_profile()
        role = self.get_user_role()

        if role == ADMIN_ROLE or role in WORKER_ROLES:
            return Bureau.objects.all()

        if role in CLIENT_ROLES and profile is not None:
            bureaux_reserves = Bureau.objects.filter(reservations__client=profile, reservations__is_active=True)
            bureaux_libres = Bureau.objects.filter(is_active=True).exclude(
                reservations__is_active=True,
                reservations__date_fin__gte=timezone.now().date()
            )
            return (bureaux_reserves | bureaux_libres).distinct()

        return Bureau.objects.none()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], url_path='par-type/(?P<type_id>[0-9]+)')
    def par_type(self, request, type_id=None):
        bureaux = Bureau.objects.filter(type_id=type_id, is_active=True)
        serializer = self.get_serializer(bureaux, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='disponibles')
    def disponibles(self, request):
        livres = Bureau.objects.filter(is_active=True).exclude(
            reservations__is_active=True,
            reservations__date_fin__gte=timezone.now().date()
        )
        serializer = self.get_serializer(livres.distinct(), many=True)
        return Response(serializer.data)


class ReservationViewSet(BaseModelViewSet):
    """ViewSet pour gérer les Réservations avec email de confirmation"""
    serializer_class = ReservationSerializer
    permission_classes = [ReservationPermission]

    def get_queryset(self):
        profile = self.get_client_profile()
        role = self.get_user_role()

        if role == ADMIN_ROLE or role in WORKER_ROLES:
            return Reservation.objects.all()

        if role in CLIENT_ROLES and profile is not None:
            return Reservation.objects.filter(client=profile)

        return Reservation.objects.none()

    def perform_create(self, serializer):
        profile = self.get_client_profile()
        if profile and self.get_user_role() in CLIENT_ROLES:
            reservation = serializer.save(client=profile)
        else:
            reservation = serializer.save()
        reservation.bureau.statut = Bureau.BureauStatus.OCCUPE
        reservation.bureau.save()

        # --- Email de Confirmation de la Réservation ---
        try:
            if reservation.client and reservation.client.user and reservation.client.user.email:
                bureau_nom = reservation.bureau.code if hasattr(reservation.bureau, 'code') else f"#{reservation.bureau.id}"
                batiment_nom = reservation.bureau.niveau.batiment.nom if hasattr(reservation.bureau, 'niveau') else "votre bâtiment"
                
                send_mail(
                    subject=f"Confirmation de votre réservation - Bureau {bureau_nom}",
                    message=f"Bonjour,\n\nNous vous confirmons la prise en compte de votre réservation pour le bureau {bureau_nom} ({batiment_nom}).\n\nPériode : du {reservation.date_debut} au {reservation.date_fin}.\n\nCordialement.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[reservation.client.user.email],
                    fail_silently=False,
                )
        except Exception as e:
            logger.error(f"Erreur d'envoi de l'email pour la réservation {reservation.id}: {str(e)}")
        # ------------------------------------------------

    @action(detail=False, methods=['get'], url_path='mes-reservations')
    def mes_reservations(self, request):
        profile = self.get_client_profile()
        if profile is None:
            return Response([], status=status.HTTP_200_OK)
        reservations = Reservation.objects.filter(client=profile)
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)


class ContratViewSet(BaseModelViewSet):
    """ViewSet pour gérer les Contrats avec emails intégrés"""
    serializer_class = ContratSerializer
    permission_classes = [ContratPermission]

    def get_queryset(self):
        profile = self.get_client_profile()
        role = self.get_user_role()

        if role == ADMIN_ROLE or role in WORKER_ROLES:
            return Contrat.objects.all()

        if role in CLIENT_ROLES and profile is not None:
            return Contrat.objects.filter(client=profile)

        return Contrat.objects.none()

    def perform_create(self, serializer):
        profile = self.get_client_profile()
        if profile and self.get_user_role() in CLIENT_ROLES:
            contrat = serializer.save(client=profile, user=self.request.user)
        else:
            contrat = serializer.save(user=self.request.user)

        if contrat.reservation and contrat.reservation.bureau:
            contrat.reservation.bureau.statut = Bureau.BureauStatus.OCCUPE
            contrat.reservation.bureau.save()

    @action(detail=True, methods=['post'], url_path='soumettre')
    def soumettre(self, request, pk=None):
        contrat = self.get_object()
        profile = self.get_client_profile()
        role = self.get_user_role()

        if role not in CLIENT_ROLES or profile is None or contrat.client != profile:
            return Response({'detail': 'Seuls les clients propriétaires peuvent soumettre un contrat.'}, status=status.HTTP_403_FORBIDDEN)

        if contrat.statut_approbation not in ('DRAFT', 'REJECTED'):
            return Response(
                {'detail': 'Le contrat doit être en brouillon ou rejeté pour être soumis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        contrat.statut_approbation = 'PENDING'
        contrat.rejection_reason = None
        contrat.save(user=request.user)
        
        # --- Notification email admin ---
        try:
            send_mail(
                subject=f"[ADMIN] Nouveau contrat en attente - Réf : #{contrat.id}",
                message=f"Le client {contrat.client} a soumis un contrat pour approbation (Montant: {contrat.montant}). Connectez-vous pour le traiter.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Erreur notification soumission contrat {contrat.id}: {str(e)}")

        serializer = self.get_serializer(contrat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='accepter')
    def accepter(self, request, pk=None):
        role = self.get_user_role()
        if role != ADMIN_ROLE:
            return Response({'detail': 'Seuls les administrateurs peuvent accepter un contrat.'}, status=status.HTTP_403_FORBIDDEN)

        contrat = self.get_object()
        if contrat.statut_approbation != 'PENDING':
            return Response(
                {'detail': 'Seul un contrat en attente peut être accepté.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        contrat.statut_approbation = 'ACCEPTED'
        contrat.approved_by = request.user
        contrat.approved_at = timezone.now()
        contrat.rejection_reason = None
        contrat.save(user=request.user)
        
        # --- Notification email Client (Accepté) ---
        try:
            if contrat.client and contrat.client.user and contrat.client.user.email:
                send_mail(
                    subject=f"Votre contrat a été accepté ! - Réf : #{contrat.id}",
                    message=f"Bonjour,\n\nBonne nouvelle ! Votre contrat (Réf : #{contrat.id}) a été validé et approuvé par notre équipe.\n\nCordialement.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contrat.client.user.email],
                    fail_silently=False,
                )
        except Exception as e:
            logger.error(f"Erreur email contrat accepté {contrat.id}: {str(e)}")

        serializer = self.get_serializer(contrat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='rejeter')
    def rejeter(self, request, pk=None):
        role = self.get_user_role()
        if role != ADMIN_ROLE:
            return Response({'detail': 'Seuls les administrateurs peuvent rejeter un contrat.'}, status=status.HTTP_403_FORBIDDEN)

        contrat = self.get_object()
        if contrat.statut_approbation != 'PENDING':
            return Response(
                {'detail': 'Seul un contrat en attente peut être rejeté.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rejection_reason = request.data.get('rejection_reason', '')
        contrat.statut_approbation = 'REJECTED'
        contrat.approved_by = request.user
        contrat.approved_at = timezone.now()
        contrat.rejection_reason = rejection_reason.strip() if rejection_reason else None
        contrat.save(user=request.user)
        
        # --- Notification email Client (Rejeté) ---
        try:
            if contrat.client and contrat.client.user and contrat.client.user.email:
                reason_text = contrat.rejection_reason if contrat.rejection_reason else "Aucun motif spécifié."
                send_mail(
                    subject=f"Mise à jour concernant votre contrat - Réf : #{contrat.id}",
                    message=f"Bonjour,\n\nVotre contrat a été refusé pour le motif suivant :\n> {reason_text}\n\nVous pouvez le corriger et le soumettre à nouveau.\n\nCordialement.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contrat.client.user.email],
                    fail_silently=False,
                )
        except Exception as e:
            logger.error(f"Erreur email contrat rejeté {contrat.id}: {str(e)}")

        serializer = self.get_serializer(contrat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='mes-contrats')
    def mes_contrats(self, request):
        profile = self.get_client_profile()
        if profile is None:
            return Response([], status=status.HTTP_200_OK)
        contrats = Contrat.objects.filter(client=profile)
        serializer = self.get_serializer(contrats, many=True)
        return Response(serializer.data)


class LocationViewSet(BaseModelViewSet):
    """ViewSet pour gérer les Locations"""
    serializer_class = LocationSerializer
    permission_classes = [LocationPermission]

    def get_queryset(self):
        profile = self.get_client_profile()
        role = self.get_user_role()

        if role == ADMIN_ROLE or role in WORKER_ROLES:
            return Location.objects.all()

        if role in CLIENT_ROLES and profile is not None:
            return Location.objects.filter(client=profile)

        return Location.objects.none()

    def perform_create(self, serializer):
        profile = self.get_client_profile()
        kwargs = {}
        if profile and self.get_user_role() in CLIENT_ROLES:
            kwargs['client'] = profile

        contrat = getattr(serializer, 'validated_data', {}).get('contrat')
        if not contrat and 'contrat' in self.request.data:
            kwargs['contrat_id'] = self.request.data.get('contrat')
        elif contrat:
            kwargs['contrat'] = contrat

        location = serializer.save(**kwargs)
        location.bureau.statut = Bureau.BureauStatus.OCCUPE
        location.bureau.save()

    @action(detail=False, methods=['get'], url_path='mes-locations')
    def mes_locations(self, request):
        profile = self.get_client_profile()
        if profile is None:
            return Response([], status=status.HTTP_200_OK)
        locations = Location.objects.filter(client=profile)
        serializer = self.get_serializer(locations, many=True)
        return Response(serializer.data)


class PaiementViewSet(BaseModelViewSet):
    """ViewSet pour gérer les Paiements avec validation et confirmation email"""
    queryset = Paiement.objects.filter(is_active=True)
    serializer_class = PaiementSerializer
    permission_classes = [PaiementPermission]

    def get_queryset(self):
        role = self.get_user_role()
        profile = self.get_client_profile()
        query = self.queryset.select_related('client__user', 'contrat', 'location')

        if role == ADMIN_ROLE or role in WORKER_ROLES:
            return query
        if role in CLIENT_ROLES and profile is not None:
            return query.filter(client=profile)
        return Paiement.objects.none()

    def perform_create(self, serializer):
        role = self.get_user_role()
        profile = self.get_client_profile()
        
        data = self.request.data
        contrat_id = data.get('contrat')
        location_id = data.get('location')
        
        maintenant = timezone.now()
        mois_auto = data.get('mois_paye', maintenant.month)
        annee_auto = data.get('annee_paye', maintenant.year)
    
        montant_auto = None
        client_final = None

        if contrat_id:
            try:
                contrat = Contrat.objects.get(pk=contrat_id, is_active=True)
                if role in CLIENT_ROLES and contrat.client != profile:
                    raise DRFValidationError({"contrat": "Ce contrat ne vous appartient pas."})
                
                montant_auto = contrat.montant or getattr(contrat.reservation, 'montant_calcule', None)
                client_final = contrat.client
            except Contrat.DoesNotExist:
                raise DRFValidationError({"contrat": "Contrat introuvable ou inactif."})

        elif location_id:
            try:
                location = Location.objects.get(pk=location_id, is_active=True)
                if role in CLIENT_ROLES and location.client != profile:
                    raise DRFValidationError({"location": "Cette location ne vous appartient pas."})
                
                if hasattr(location, 'montant') and location.montant:
                    montant_auto = location.montant
                elif location.bureau:
                    montant_auto = location.bureau.prix
                
                client_final = location.client
            except Location.DoesNotExist:
                raise DRFValidationError({"location": "Location introuvable ou inactive."})
        else:
            raise DRFValidationError({"detail": "Un identifiant de contrat ou de location valide est requis."})

        if montant_auto is None or float(montant_auto) <= 0:
            raise DRFValidationError({"montant": "Impossible de générer un montant automatique valide pour cette entité."})

        if role in CLIENT_ROLES:
            serializer.save(
                client=profile, 
                montant=montant_auto, 
                statut='PENDING', 
                mois_paye=mois_auto, 
                annee_paye=annee_auto
            )
        else:
            serializer.save(
                client=client_final, 
                montant=montant_auto, 
                statut='PAID', 
                mois_paye=mois_auto, 
                annee_paye=annee_auto
            )
            
    @action(detail=True, methods=['post'], url_path='valider-paiement')
    def valider_paiement(self, request, pk=None):
        """Action personnalisée pour passer un paiement en statut 'PAID'."""
        paiement = get_object_or_404(Paiement, pk=pk)
        
        user = request.user
        if not hasattr(user, 'client_profile') or user.client_profile.role not in ['ADMIN', 'TRAVAILLEUR', 'MANAGER']:
            return Response(
                {"detail": "Vous n'avez pas la permission de valider ce paiement."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        if paiement.statut == 'PAID':
            return Response(
                {"detail": "Ce paiement a déjà été validé et encaissé."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        paiement.statut = 'PAID'
        paiement.save(user=user) 
        
        # --- Notification par e-mail ---
        try:
            if paiement.client and paiement.client.user and paiement.client.user.email:
                destinataire_email = paiement.client.user.email
                
                send_mail(
                    subject=f"Confirmation de validation de paiement - Réf : #{paiement.id}",
                    message=f"Bonjour,\n\nNous vous informons que votre paiement d'un montant de {paiement.montant} pour la période {paiement.mois_paye}/{paiement.annee_paye} a été validé et encaissé avec succès.\n\nMerci pour votre confiance,\nL'équipe de gestion.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[destinataire_email],
                    fail_silently=False,
                )
        except Exception as e:
            logger.error(f"Échec de l'envoi de l'email pour le paiement {paiement.id}. Erreur : {str(e)}")

        return Response(
            {"detail": "Le paiement a été validé avec succès !", "statut": paiement.statut}, 
            status=status.HTTP_200_OK
        )