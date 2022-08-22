from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
import pytz

class Person(models.Model):
    title = models.CharField(max_length=16, blank=True)
    given_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True)
    surname = models.CharField(max_length=64, blank=True)
    surname_first = models.BooleanField(default=False)
    auth_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='person')

    @property
    def full_name(self):
        if self.surname_first:
            names = (self.surname, self.given_name, self.middle_name)
        else:
            names = (self.given_name, self.middle_name, self.surname)
        return ' '.join(filter(None, names))

    def __str__(self):
        return f'{self.full_name} [{self.id}]'

    class Meta:
        verbose_name_plural = 'people'
        ordering = ['surname', 'given_name', 'id']
        indexes = [
            models.Index(fields=['surname']),
            models.Index(fields=['given_name'])
        ]

class Organisation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['name']

class ContactRecord(models.Model):
    class NCARDRelation(models.IntegerChoices):
        CORE_TEAM = 1, 'Core team'
        AFFILIATE = 2, 'Affiliate'
        COLLABORATOR = 3, 'Collaborator'
        COMMUNITY_OR_CONSUMER = 4, 'Community / Consumer'
        ADVOCATE = 5, 'Advocate'
        GOVT_OR_INDUSTRY = 6, 'Govt / Industry'
        OTHER = 0, 'Other'

    class DisplayOnWebsite(models.IntegerChoices):
        NO = 0, 'No'
        YES = 1, 'Yes'
        STUDENT = 2, 'Yes - student'

    phone_validator = RegexValidator(r'^[ 0-9()+,*#-]*$', 'Phone numbers must contain only these characters: #()*+,-0123456789')
    # ORCID ident. format based on https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier
    orcid_validator = RegexValidator(r'^$|^https://orcid\.org/\d{4}-\d{4}-\d{4}-\d{3}(\d|X)$', 'ORCID identifier must be a full URL, in this format: https://orcid.org/XXXX-XXXX-XXXX-XXXX')
    # https://help.twitter.com/en/managing-your-account/twitter-username-rules
    twitter_validator = RegexValidator(r'^$|^@[A-Za-z0-9_]+$', 'Twitter handle must begin with an @ and only contain letters, digits and underscores.')
    nonnegative_validator = MinValueValidator(0, 'Value must not be negative.')

    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='contact')
    email = models.EmailField('email', blank=True)
    email2 = models.EmailField('email 2', blank=True)
    phone_office = models.CharField('phone (office)', max_length=25, blank=True, validators=[phone_validator])
    phone_mobile = models.CharField('phone (mobile)', max_length=25, blank=True, validators=[phone_validator])
    phone_home = models.CharField('phone (home)', max_length=25, blank=True, validators=[phone_validator])
    cre_role = models.CharField('CRE role', max_length=15, blank=True)
    ncard_relation = models.IntegerField('relationship with NCARD', choices=NCARDRelation.choices, default=NCARDRelation.OTHER)
    project = models.CharField(max_length=50, blank=True)
    display_on_website = models.IntegerField(choices=DisplayOnWebsite.choices, default=DisplayOnWebsite.NO)
    profile_url = models.URLField('profile URL', blank=True)
    orcid_id = models.CharField('ORCID iD', max_length=37, blank=True, validators=[orcid_validator])
    scopus_id = models.BigIntegerField('Scopus ID', null=True, blank=True, validators=[nonnegative_validator])
    wos_researcher_id = models.CharField('WoS ResearcherID', max_length=32, blank=True)
    google_scholar = models.URLField('Google Scholar', blank=True)
    researchgate = models.URLField('ResearchGate', blank=True)
    loop_profile = models.URLField('Loop profile', blank=True)
    linkedin = models.URLField('LinkedIn', blank=True)
    twitter = models.CharField('Twitter handle', max_length=16, blank=True, validators=[twitter_validator])
    employers = models.ManyToManyField(Organisation, blank=True)
    location = models.CharField(max_length=50, blank=True)
    organisation_primary = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_records_primary', verbose_name='organisation (primary)')
    organisation_other = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_records_other', verbose_name='organisation (other)')
    clinician = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    research_focus = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.person)

    class Meta:
        ordering = ['person']
        indexes = [
            models.Index(fields=['person'])
        ]

class PersonAddress(models.Model):
    class AddressType(models.IntegerChoices):
        HOME = 1, 'Home'
        WORK = 2, 'Work'
        
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='addresses')
    type = models.IntegerField(choices=AddressType.choices)
    line1 = models.CharField('line 1', max_length=64)
    line2 = models.CharField('line 2', max_length=64, blank=True)
    line3 = models.CharField('line 3', max_length=64, blank=True)
    suburb = models.CharField(max_length=32, blank=True)
    state = models.CharField('state (abbrev.)', max_length=3, blank=True)
    postcode = models.CharField(max_length=20)
    country = models.CharField(max_length=2, choices=sorted(pytz.country_names.items(), key=lambda kv: kv[1]), default='AU')

    def __str__(self):
        return f'{self.person}, {self.get_type_display()}'

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        constraints = [
            models.UniqueConstraint(fields=['person', 'type'], name='address_unique_person_type')
        ]
        indexes = [
            models.Index(fields=['person', 'type'])
        ]