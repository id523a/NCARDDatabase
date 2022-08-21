from django.test import TestCase
from ncard_app import models
from django.core.exceptions import ValidationError

class PersonTests(TestCase):
    def setUp(self):
        self.roosevelt = models.Person(given_name='Franklin', middle_name='Delano', surname='Roosevelt')
        self.curie = models.Person(title='Dr.', given_name='Marie', surname='Curie')
        self.chairman = models.Person(surname='Mao', given_name='Zedong', surname_first=True)
        self.mononym = models.Person(given_name='Diogenes')
    
    def test_valid(self):
        self.roosevelt.full_clean()
        self.curie.full_clean()
        self.chairman.full_clean()
        self.mononym.full_clean()
    
    def test_invalid(self):
        with self.assertRaises(ValidationError):
            noname = models.Person(title='Mr.', surname='Anonymous')
            noname.full_clean()
        
    def test_full_name(self):
        self.assertEqual(self.roosevelt.full_name, 'Franklin Delano Roosevelt')
        self.assertEqual(self.curie.full_name, 'Marie Curie')
        self.assertEqual(self.chairman.full_name, 'Mao Zedong')
        self.assertEqual(self.mononym.full_name, 'Diogenes')