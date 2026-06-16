from django.test import TestCase
from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase
from gestionBatiment.models import Category 

# Create your tests here.

class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Catégorie Test')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Catégorie Test')
        self.assertTrue(self.category.is_active)

    def test_category_str_representation(self):
        self.assertEqual(str(self.category), 'Catégorie Test')  
        

class test_category_api(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Catégorie Test')
        self.url = reverse('category-list')

    def test_get_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Catégorie Test')
        
        