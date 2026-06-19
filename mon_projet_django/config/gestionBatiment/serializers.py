from rest_framework import serializers
from django.contrib.auth.models import User 
from django.db import transaction
from .models import Client, Batiment, Niveau,  TypeBureau, Bureau, Reservation,  Contrat, Location, Paiement


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ClientDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    telephone = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'user', 'telephone', 'addresse', 'date_naissance']

    def get_telephone(self, obj):
        return str(obj.telephone) if obj.telephone else None


class ClientSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    username = serializers.CharField(write_only=True, required=False, max_length=150)
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False, max_length=150)
    last_name = serializers.CharField(write_only=True, required=False, max_length=150)

    class Meta:
        model = Client
        fields = [
            'user_id', 'user_detail', 'username', 'password', 'email',
            'first_name', 'last_name', 'telephone', 'addresse',
            'date_naissance', 'created_at', 'updated_at'
        ]

    def get_user_detail(self, obj):
        return UserDetailSerializer(obj.user).data

    def validate_username(self, value):
        query = User.objects.filter(username=value)
        if self.instance and self.instance.user:
            query = query.exclude(pk=self.instance.user.id)
        if query.exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            username = validated_data.pop('username')
            password = validated_data.pop('password')
            email = validated_data.pop('email', '')
            first_name = validated_data.pop('first_name', '')
            last_name = validated_data.pop('last_name', '')

            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'first_name': first_name, 'last_name': last_name},
            )
            if not created:
                user.email = email or user.email
                user.first_name = first_name or user.first_name
                user.last_name = last_name or user.last_name
                user.save()
            user.set_password(password)
            user.save()

            client = Client.objects.create(user=user, role=Client.UserRole.CLIENT, **validated_data)
            return client

    def update(self, instance, validated_data):
        user_data = {}
        for field in ['username', 'email', 'first_name', 'last_name']:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)
        
        password = validated_data.pop('password', None)

        with transaction.atomic():
            if user_data or password:
                user = instance.user
                for attr, value in user_data.items():
                    setattr(user, attr, value)
                if password:
                    user.set_password(password)
                user.save()

            return super().update(instance, validated_data)


class BatimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batiment
        fields = ['id', 'nom', 'adresse', 'nombre_etages', 'date_construction', 'created_at', 'updated_at', 'is_active']


class NiveauSerializer(serializers.ModelSerializer):
    batiment_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Niveau
        fields = ['id', 'nom', 'batiment', 'batiment_detail', 'created_at', 'updated_at', 'is_active']
    
    def get_batiment_detail(self, obj):
        if obj.batiment:
            return {
                'id': obj.batiment.id,
                'nom': obj.batiment.nom,
                'adresse': obj.batiment.adresse,
                'nombre_etages': obj.batiment.nombre_etages,
                'date_construction': obj.batiment.date_construction,
            }
        return None


class TypeBureauSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeBureau
        fields = ['id', 'nom', 'description', 'created_at', 'is_active']


class BureauSerializer(serializers.ModelSerializer):
    type_detail = serializers.SerializerMethodField(read_only=True)
    batiment_detail = serializers.SerializerMethodField(read_only=True)
    niveau_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bureau
        fields = ['id', 'numero', 'type', 'type_detail', 'unite', 'espace', 'prix', 'batiment', 'batiment_detail', 'niveau', 'niveau_detail', 'statut', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['prix', 'statut']

    def get_type_detail(self, obj):
        if obj.type:
            return {
                'id': obj.type.id,
                'nom': obj.type.nom,
                'description': obj.type.description,
            }
        return None

    def get_batiment_detail(self, obj):
        if obj.batiment:
            return {
                'id': obj.batiment.id,
                'nom': obj.batiment.nom,
                'adresse': obj.batiment.adresse,
                'nombre_etages': obj.batiment.nombre_etages,
                'date_construction': obj.batiment.date_construction,
            }
        return None

    def get_niveau_detail(self, obj):
        if obj.niveau:
            return {
                'id': obj.niveau.id,
                'nom': obj.niveau.nom,
                'batiment': obj.niveau.batiment.id if obj.niveau.batiment else None,
            }
        return None

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        bureau = Bureau(**validated_data)
        bureau.save(user=user)
        return bureau

    def update(self, instance, validated_data):
        user = validated_data.pop('user', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(user=user)
        return instance


class ContratSerializer(serializers.ModelSerializer):
    montant = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    created_by = UserDetailSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)
    locations = serializers.SerializerMethodField(read_only=True)
    paiements = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Contrat
        fields = [
            'id', 'reservation', 'client', 'date_debut', 'date_fin',
            'type_facturation', 'montant', 'description',
             'created_by', 'created_at', 'updated_at', 'is_active',
            'locations', 'paiements'
        ]
        read_only_fields = [ 'created_by', 'created_at', 'updated_at', 'is_active', 'locations', 'paiements']

    def get_locations(self, obj):
        qs = obj.locations.all()
        return [
            {
                'id': loc.id,
                'date_debut': loc.date_debut,
                'date_fin': loc.date_fin,
                'bureau_id': loc.bureau_id,
            }
            for loc in qs
        ]

    def get_paiements(self, obj):
        qs = obj.paiements.all()
        return [
            {
                'id': p.id,
                'date': p.date,
                'montant': str(p.montant),
                'mode': p.mode,
                'statut': p.statut,
                'location_id': p.location_id,
                'client_id': p.client_id,
            }
            for p in qs
        ]

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        contrat = Contrat(**validated_data)
        contrat.save(user=user)
        return contrat

    def update(self, instance, validated_data):
        user = validated_data.pop('user', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(user=user)
        return instance


class ReservationSerializer(serializers.ModelSerializer):
    client_detail = serializers.SerializerMethodField(read_only=True)
    bureau_detail = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Reservation
        fields = ['id', 'date_debut', 'date_fin', 'bureau', 'client', 'client_detail', 'bureau_detail', 'created_at', 'updated_at', 'is_active']

    def get_client_detail(self, obj):
        if obj.client:
            return {
                'id': obj.client.id,
                'user': {
                    'id': obj.client.user.id,
                    'username': obj.client.user.username,
                    'first_name': obj.client.user.first_name,
                    'last_name': obj.client.user.last_name,
                    'email': obj.client.user.email,
                },
                'telephone': str(obj.client.telephone) if obj.client.telephone else None,
                'addresse': obj.client.addresse,
                'date_naissance': obj.client.date_naissance,
            }
        return None
    #Fonction pour masque le champ client aux Clients connecte mais permettre les admins de voir les champs
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            if hasattr(request.user, 'client_profile') and request.user.client_profile:
                profile = request.user.client_profile
                
                if profile.role == 'CLIENT':
                    self.fields['client'].read_only = True

    def get_bureau_detail(self, obj):
        if obj.bureau:
            return {
                'id': obj.bureau.id,
                'numero': obj.bureau.numero,
                'batiment': obj.bureau.batiment.nom if obj.bureau.batiment else None,
                'niveau': obj.bureau.niveau.nom if obj.bureau.niveau else None,
                'prix': str(obj.bureau.prix) if obj.bureau.prix else None,
                'statut': obj.bureau.statut,
            }
        return None


class LocationSerializer(serializers.ModelSerializer):
    client_detail = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Location
        fields = ['id', 'date_debut', 'date_fin', 'bureau','contrat', 'client', 'client_detail', 'created_at', 'updated_at', 'is_active']
        
    def get_client_detail(self, obj):
        if obj.client:
            return {
                'id': obj.client.id,
                'user': {
                    'id': obj.client.user.id,
                    'username': obj.client.user.username,
                    'first_name': obj.client.user.first_name,
                    'last_name': obj.client.user.last_name,
                    'email': obj.client.user.email,
                },
                'telephone': str(obj.client.telephone) if obj.client.telephone else None,
                'addresse': obj.client.addresse,
                'date_naissance': obj.client.date_naissance,
            }
        return None


class PaiementSerializer(serializers.ModelSerializer):
    client_detail = serializers.SerializerMethodField(read_only=True)
    created_by = UserDetailSerializer(read_only=True)
    mode = serializers.ChoiceField(choices=[('CASH', 'Espèces'), ('CARD', 'Carte bancaire'), ('TRANSFER', 'Virement bancaire')], default='CASH')
    montant = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(default=True)
    
    class Meta:
        model = Paiement
        fields = [
            'id', 'date', 'montant', 'mode', 'location', 'client',
            'client_detail', 'contrat', 'statut','mois_paye','annee_paye',
            'created_by', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['created_by', 'statut', 'created_at', 'updated_at', 'is_active']

    def get_client_detail(self, obj):
        if obj.client:
            return {
                'id': obj.client.id,
                'user': {
                    'id': obj.client.user.id,
                    'username': obj.client.user.username,
                    'first_name': obj.client.user.first_name,
                    'last_name': obj.client.user.last_name,
                    'email': obj.client.user.email,
                },
                'telephone': str(obj.client.telephone) if obj.client.telephone else None,
                'addresse': obj.client.addresse,
                'date_naissance': obj.client.date_naissance,
            }
        return None 
    
    
    def validate(self, attrs):
        client = attrs.get('client')
        contrat = attrs.get('contrat')
        location = attrs.get('location')

        if not client and not contrat and not location:
            raise serializers.ValidationError(
                "Un paiement doit etre lie a un client, un contrat ou une location."
            )

        if client and contrat and contrat.client_id != client.id:
            raise serializers.ValidationError({
                'client': "Le client ne correspond pas au client du contrat."
            })

        if client and location and location.client_id != client.id:
            raise serializers.ValidationError({
                'client': "Le client ne correspond pas au client de la location."
            })

        return attrs

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        contrat = validated_data.get('contrat')
        location = validated_data.get('location')
        client = validated_data.get('client')

        if not client:
            if contrat:
                if hasattr(contrat, 'client'):
                    validated_data['client'] = contrat.client
                elif isinstance(contrat, int):
                    try:
                        validated_data['client'] = Contrat.objects.get(pk=contrat).client
                    except Contrat.DoesNotExist:
                        pass
            elif location:
                if hasattr(location, 'client'):
                    validated_data['client'] = location.client
                elif isinstance(location, int):
                    try:
                        validated_data['client'] = Location.objects.get(pk=location).client
                    except Location.DoesNotExist:
                        pass

        paiement = Paiement(**validated_data)
        paiement.save(user=user)
        return paiement

    def update(self, instance, validated_data):
        user = validated_data.pop('user', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(user=user)
        return instance
        