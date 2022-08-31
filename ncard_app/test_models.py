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
        self.contact_record = models.ContactRecord(person=self.person)
        self.contact_record.save()

    def test_default(self):
        self.person.full_clean()
        self.contact_record.full_clean()

    def test_email_validation(self):
        self.contact_record.email = 'valid.email!+0123@example.com'
        self.contact_record.email2 = 'valid.email!+0123@example.com'
        self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.email = 'invalid.email@example'
            self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.email2 = 'invalid.email@example'
            self.contact_record.full_clean()

    def test_phone_validation(self):
        self.contact_record.phone_office = '#()*+,- 0123456789'
        self.contact_record.phone_mobile = '+61 (0) 456-789-012'
        self.contact_record.phone_home = '11'
        self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.phone_office = 'invalid'
            self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.phone_mobile = 'invalid'
            self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.phone_home = 'invalid'
            self.contact_record.full_clean()

    def test_orcid_validation(self):
        self.contact_record.orcid_id = 'https://orcid.org/0000-0002-1694-233X'
        self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.orcid_id = 'invalid'
            self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.orcid_id = '0000-0002-1694-233X'
            self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.orcid_id = 'https://orcid.org/000000021694233X'
            self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.orcid_id = 'http://orcid.org/0000-0002-1694-233X'
            self.contact_record.full_clean()

    def test_twitter_validation(self):
        self.contact_record.twitter = '@xxxxxx_Yyyyyy'
        self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.twitter = 'missing_at'
            self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.twitter = '@overlongoverlong'
            self.contact_record.full_clean()

        with self.assertRaises(ValidationError):
            self.contact_record.twitter = '@INVALID_CHAR$'
            self.contact_record.full_clean()