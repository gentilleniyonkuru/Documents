
from django.contrib import admin
from .models import Client, Niveau, TypeBureau, Batiment, Bureau, Paiement, Reservation, Contrat, Location

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # CORRECTION : On utilise les méthodes personnalisées (get_first_name...) au lieu de user__first_name
    list_display = ('id', 'user__id', 'get_first_name', 'get_last_name', 'telephone', 'addresse', 'date_naissance', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'telephone')
    list_filter = ('created_at',)
    
    # Amélioration de l'affichage des méthodes dans l'admin
    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'Prénom'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Nom'


@admin.register(Batiment)
class BatimentAdmin(admin.ModelAdmin):
    # AJOUT : 'taux_occupation' et 'revenues_totaux' visibles en direct
    list_display = ('id', 'nom', 'adresse', 'nombre_etages', 'taux_occupation_visuel', 'revenues_totaux_visuel', 'is_active')
    search_fields = ('nom', 'adresse')
    list_filter = ('is_active', 'created_at')
    
    def taux_occupation_visuel(self, obj):
        return f"{obj.taux_occupation}%"
    taux_occupation_visuel.short_description = "Taux d'occupation"

    def revenues_totaux_visuel(self, obj):
        return f"{obj.revenues_totaux} CFA"
    revenues_totaux_visuel.short_description = "Revenus encaissés"


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    # AJOUT : 'taux_occupation' et 'revenues_totaux' par étage
    list_display = ('id', 'nom', 'batiment', 'taux_occupation_visuel', 'revenues_totaux_visuel', 'is_active')
    search_fields = ('nom', 'batiment__nom')
    list_filter = ('batiment', 'is_active')

    def taux_occupation_visuel(self, obj):
        return f"{obj.taux_occupation}%"
    taux_occupation_visuel.short_description = "Taux d'occupation"

    def revenues_totaux_visuel(self, obj):
        return f"{obj.revenues_totaux} CFA"
    revenues_totaux_visuel.short_description = "Revenus de l'étage"


@admin.register(TypeBureau)
class TypeBureauAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'description', 'created_at', 'is_active')
    search_fields = ('nom',)
    list_filter = ('is_active', 'created_at')


@admin.register(Bureau)
class BureauAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'batiment', 'niveau', 'type', 'unite', 'espace', 'prix', 'is_active')
    search_fields = ('numero', 'batiment__nom')
    list_filter = ('batiment', 'niveau', 'type', 'is_active')
    # CORRECTION : Seul le champ 'prix' doit être en readonly. L'utilisateur doit pouvoir saisir l'espace et l'unite !
    readonly_fields = ('prix',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # AJOUT : Le 'statut_temporel' (À VENIR, EN COURS...) s'affiche dynamiquement
    list_display = ('id', 'client', 'bureau', 'date_debut', 'date_fin', 'statut_temporel', 'is_active')
    search_fields = ('client__user__first_name', 'client__user__last_name', 'bureau__numero')
    list_filter = ('is_active', 'date_debut', 'date_fin')


@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'reservation', 'date_debut', 'date_fin', 'loyer_mensuel', 'statut_temporel', 'is_active')
    search_fields = ('client__user__first_name', 'client__user__last_name', 'reservation__bureau__numero')
    list_filter = ('is_active', 'date_debut', 'date_fin')
    readonly_fields = ('loyer_mensuel',) # Géré automatiquement dans le modèle désormais


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    # AJOUT : Enregistrement de la table Location manquante
    list_display = ('id', 'client', 'bureau', 'date_debut', 'date_fin', 'statut_temporel', 'is_active')
    search_fields = ('client__user__first_name', 'client__user__last_name', 'bureau__numero')
    list_filter = ('is_active', 'date_debut', 'date_fin')


# @admin.register(Paiement)
# class PaiementAdmin(admin.ModelAdmin):
    
#     #list_display = ('id', 'client', 'loyer_mensuel', 'reste_a_payer_visuel', 'statut', 'mode', 'contrat', 'location', 'date')
#     # CODE ACTUEL (À MODIFIER)
#     list_display = ['id', 'contrat', 'loyer_mensuel', 'montant_verse', 'mois_paye', 'annee_paye']
#     search_fields = ('client__user__first_name', 'client__user__last_name', 'contrat__id')
#     list_filter = ('statut', 'mode', 'date')

#     def reste_a_payer_visuel(self, obj):
#         return f"{obj.reste_a_payer} CFA"
#     reste_a_payer_visuel.short_description = "Reste à payer"
#     @admin.display(ordering='contrat__loyer_mensuel', description='Loyer Mensuel Prévu')
#     def get_loyer_mensuel(self, obj):
#         # On va chercher le loyer mensuel dans le contrat lié au paiement
#         return obj.contrat.loyer_mensuel if obj.contrat else "-"

# @admin.register(Paiement)
# class PaiementAdmin(admin.ModelAdmin):
#     # 1. Correction : On utilise 'get_loyer_mensuel' à la place de 'loyer_mensuel'
#     list_display = ['id', 'contrat', 'get_loyer_mensuel', 'montant_verse', 'mois_paye', 'annee_paye', 'reste_a_payer_visuel']
    
#     # 2. Sécurité pour la recherche : on cherche via le contrat lié
#     search_fields = ('contrat__client__user__first_name', 'contrat__client__user__last_name', 'contrat__id')
    
#     # 3. Filtres basés sur les champs existants de ton modèle Paiement
#     list_filter = ('annee_paye', 'mois_paye', 'date_paiement')

#     # --- FONCTIONS D'AFFICHAGE PERSONNALISÉES ---

#     @admin.display(ordering='contrat__loyer_mensuel', description='Loyer Mensuel Prévu')
#     def get_loyer_mensuel(self, obj):
#         # On remonte au contrat pour afficher le loyer mensuel prévu
#         return f"{obj.contrat.loyer_mensuel} CFA" if obj.contrat and obj.contrat.loyer_mensuel else "-"

#     def reste_a_payer_visuel(self, obj):
#         # Si tu as une propriété ou un champ 'reste_a_payer' calculé dans ton modèle Paiement
#         if hasattr(obj, 'reste_a_payer') and obj.reste_a_payer is not None:
#             return f"{obj.reste_a_payer} CFA"
        
#         # Logique alternative automatique : Loyer prévu - Montant versé
#         if obj.contrat and obj.contrat.loyer_mensuel:
#             reste = obj.contrat.loyer_mensuel - obj.montant_verse
#             return f"{reste} CFA"
#         return "-"
        
#     reste_a_payer_visuel.short_description = "Reste à payer"

# @admin.register(Paiement)
# class PaiementAdmin(admin.ModelAdmin):
#     # CORRECTION : On utilise 'montant' à la place de 'montant_verse'
#     list_display = ['id', 'contrat', 'get_loyer_mensuel', 'montant', 'mois_paye', 'annee_paye', 'reste_a_payer_visuel']
    
#     search_fields = ('contrat__client__user__first_name', 'contrat__client__user__last_name', 'contrat__id')
    
#     # CORRECTION : On utilise 'date' à la place de 'date_paiement'
#     list_filter = ('annee_paye', 'mois_paye', 'date')

#     # --- FONCTIONS D'AFFICHAGE PERSONNALISÉES ---

#     @admin.display(ordering='contrat__loyer_mensuel', description='Loyer Mensuel Prévu')
#     def get_loyer_mensuel(self, obj):
#         return f"{obj.contrat.loyer_mensuel} CFA" if obj.contrat and obj.contrat.loyer_mensuel else "-"

#     def reste_a_payer_visuel(self, obj):
#         if hasattr(obj, 'reste_a_payer') and obj.reste_a_payer is not None:
#             return f"{obj.reste_a_payer} CFA"
        
#         # Logique de secours basée sur tes champs exacts ('montant' au lieu de 'montant_verse')
#         if obj.contrat and obj.contrat.loyer_mensuel:
#             reste = obj.contrat.loyer_mensuel - obj.montant
#             return f"{reste} CFA"
#         return "-"
        
#     reste_a_payer_visuel.short_description = "Reste à payer"
# @admin.register(Paiement)
# class PaiementAdmin(admin.ModelAdmin):
#     # On affiche 'get_loyer_mensuel_30' et 'reste_a_payer_visuel'
#     list_display = ['id', 'contrat', 'get_loyer_mensuel_30', 'montant', 'mois_paye', 'annee_paye', 'reste_a_payer_visuel']
    
#     search_fields = ('contrat__client__user__first_name', 'contrat__client__user__last_name', 'contrat__id')
#     list_filter = ('annee_paye', 'mois_paye', 'date')

#     @admin.display(ordering='contrat__loyer_mensuel', description='Loyer Mensuel Prévu (30j)')
#     def get_loyer_mensuel_30(self, obj):
#         return f"{obj.loyer_mensuel_prevu_30_jours} CFA"

#     @admin.display(description='Reste à payer')
#     def reste_a_payer_visuel(self, obj):
#         return f"{obj.reste_a_payer} CFA"
@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['id', 'contrat', 'get_loyer_mensuel_30', 'montant', 'mois_paye', 'annee_paye', 'reste_a_payer_visuel']
    search_fields = ('contrat__client__user__first_name', 'contrat__client__user__last_name', 'contrat__id')
    list_filter = ('annee_paye', 'mois_paye', 'date')

    @admin.display(description='Loyer Mensuel Prévu (30j)')
    def get_loyer_mensuel_30(self, obj):
        return f"{obj.loyer_mensuel_prevu_30_jours} CFA"

    @admin.display(description='Reste à payer')
    def reste_a_payer_visuel(self, obj):
        return f"{obj.reste_a_payer} CFA"