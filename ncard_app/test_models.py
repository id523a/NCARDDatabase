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

class ContactRecordTests(TestCase):
    def setUp(self):
        self.person = models.Person(title='Mr.', given_name='Edward', surname='Giles')
        self.person.save()

    def test_default(self):
        self.person.full_clean()

    def test_email_validation(self):
        self.person.email = 'valid.email!+0123@example.com'
        self.person.email2 = 'valid.email!+0123@example.com'
        self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.email = 'invalid.email@example'
            self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.email2 = 'invalid.email@example'
            self.person.full_clean()

    def test_phone_validation(self):
        self.person.phone_office = '#()*+,- 0123456789'
        self.person.phone_mobile = '+61 (0) 456-789-012'
        self.person.phone_home = '11'
        self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.phone_office = 'invalid'
            self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.phone_mobile = 'invalid'
            self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.phone_home = 'invalid'
            self.person.full_clean()

    def test_orcid_validation(self):
        self.person.orcid_id = 'https://orcid.org/0000-0002-1694-233X'
        self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.orcid_id = 'invalid'
            self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.orcid_id = '0000-0002-1694-233X'
            self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.orcid_id = 'https://orcid.org/000000021694233X'
            self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.orcid_id = 'http://orcid.org/0000-0002-1694-233X'
            self.person.full_clean()

    def test_twitter_validation(self):
        self.person.twitter = '@xxxxxx_Yyyyyy'
        self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.twitter = 'missing_at'
            self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.twitter = '@overlongoverlong'
            self.person.full_clean()

        with self.assertRaises(ValidationError):
            self.person.twitter = '@INVALID_CHAR$'
            self.person.full_clean()
