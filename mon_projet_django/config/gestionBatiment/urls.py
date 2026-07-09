from gestionBatiment.views import (
    BatimentViewSet,
    BureauViewSet,
    ClientViewSet,
    ContratViewSet,
    LocationViewSet,
    NiveauViewSet,
    PaiementViewSet,
    ReservationViewSet,
    TypeBureauViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"clients", ClientViewSet)
router.register(r"batiments", BatimentViewSet)
router.register(r"types-bureau", TypeBureauViewSet)
router.register(r"niveaux", NiveauViewSet)
router.register(r"bureaux", BureauViewSet)
router.register(r"reservations", ReservationViewSet)
router.register(r"contrats", ContratViewSet)
router.register(r"locations", LocationViewSet)
router.register(r"paiements", PaiementViewSet)
