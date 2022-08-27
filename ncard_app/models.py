from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
import pytz

#validators section

phone_validator = RegexValidator(r'^[ 0-9()+,*#-]*$', 'Phone numbers must contain only these characters: #()*+,-0123456789')
# ORCID ident. format based on https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier
orcid_validator = RegexValidator(r'^$|^https://orcid\.org/\d{4}-\d{4}-\d{4}-\d{3}(\d|X)$', 'ORCID identifier must be a full URL, in this format: https://orcid.org/XXXX-XXXX-XXXX-XXXX')
# https://help.twitter.com/en/managing-your-account/twitter-username-rules
twitter_validator = RegexValidator(r'^$|^@[A-Za-z0-9_]+$', 'Twitter handle must begin with an @ and only contain letters, digits and underscores.')
nonnegative_validator = MinValueValidator(0, 'Value must not be negative.')
country_code_validator = RegexValidator(r'^[A-Z]{2}$', 'Country code must be two upper-case letters, e.g. AU')

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
    name = models.CharField('name', max_length=255)
    primary_contact = models.ForeignKey(Person, on_delete=models.RESTRICT, related_name='organisations_primary_contact')
    phone = models.CharField('phone', max_length=25, blank=True, validators=[phone_validator])
    website = models.URLField('website', blank=True)
    twitter_handle = models.CharField('Twitter handle', max_length=255, blank=True, validators=[twitter_validator])
    type = models.CharField('type', max_length=255, blank=True)

    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['name']

class Project(models.Model):
    class ProjectStatus(models.IntegerChoices):
        NONE = 0, '-'
        PENDING = 1, 'Pending'
        ACTIVE = 2, 'Active'
        COMPLETE = 3, 'Complete'

    name = models.CharField(max_length=255)
    lead = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    status = models.IntegerField(choices=ProjectStatus.choices, default=ProjectStatus.NONE)
    funded = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

class Engagement(models.Model):
    contact_name = models.CharField('contact name', max_length=25) # Is this a foreign key to Person?
    type = models.CharField('type', max_length=255, blank=True) # integer choices change
    title = models.CharField('title', max_length=255, blank=True)
    lead_organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True, related_name='engagements')
    detail = models.TextField('detail', blank=True)
    year = models.PositiveSmallIntegerField('year')
    outcome = models.TextField('outcome', blank=True) # what type is this 
    media_link = models.URLField('media link', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Award(models.Model):
    type = models.CharField('type', max_length=255) # integer choices
    agency = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True, related_name='awards')
    name = models.CharField('name', max_length=255)
    recipients = models.ManyToManyField(Person)
    status = models.CharField('award status', max_length=255, blank=True) # integer chocies
    detail = models.TextField('detail', blank=True)
    year = models.PositiveSmallIntegerField('year')

    def __str__(self):
        return f'{self.name} {self.year}'

    class Meta:
        ordering = ['year']

class Biography(models.Model):
    person = models.OneToOneField(Person, on_delete=models.RESTRICT, related_name='biography')
    bio_type = models.CharField('bio type', max_length=255) # integer choice
    cv_attachment = models.FileField('cv attachment') # volume required

    def __str__(self):
        return str(self.person)


class Event(models.Model):
    type = models.CharField('type', max_length=255) #integer choices
    date = models.DateField('date')
    number_attendees = models.IntegerField('number of attendees')
    detail = models.TextField('detail')
    lead = models.ForeignKey(Organisation, on_delete=models.SET_NULL, blank=True, null=True, related_name='events')
    location = models.CharField('location', max_length=255, blank=True)
    title = models.CharField('title', max_length=255, blank=True)

    def __str__(self):
        if not self.title:
            return self.detail
        return self.title

    class Meta:
        ordering = ['title']

class Publication(models.Model):
    type = models.CharField('type', max_length=255) # integer choices
    year = models.PositiveSmallIntegerField('year') 
    title = models.CharField('title', max_length=255)
    contributors = models.ManyToManyField(Person)
    journal = models.CharField('journal', max_length=255)
    journal_ISSN = models.CharField('journal ISSN')
    volume = models.PositiveSmallIntegerField('volume', blank=True)
    page_start = models.PositiveIntegerField('start page', blank=True)
    page_end = models.PositiveIntegerField('end page', blank=True)
    open_access_status = models.CharField('open access status', max_length=255, blank=True) # integer choices
    doi = models.CharField('doi', max_length=255)
    electronic_ISBN = models.CharField('electronic ISBN', max_length=255, blank=True)
    print_ISBN = models.CharField('print ISBN', max_length=255, blank=True)
    abstract = models.TextField('abstract', blank=True)
    vancouver = models.CharField('Vancouver', max_length=255, blank=True)
    source_ID = models.CharField('source ID', max_length=50, blank=True) # check
    ncard_publication = models.BooleanField('NCARD publication', default=True)

    def __str__(self):
        if self.ncard_publication:
            return f'NCARD - {self.title}'
        return self.title

    class Meta:
        ordering = ['year']

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

class Country(models.Model):
    code = models.CharField('country code', max_length=2, primary_key=True, validators=[country_code_validator])
    name = models.CharField('name', max_length=255)

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
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, to_field='code', default='AU', related_name='+')

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

class Project(models.Model):
    class ProjectStatus(models.IntegerChoices):
        NONE = 0, '-'
        PENDING = 1, 'Pending'
        ACTIVE = 2, 'Active'
        COMPLETE = 3, 'Complete'

    name = models.CharField(max_length=255)
    lead = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    status = models.IntegerField(choices=ProjectStatus.choices, default=ProjectStatus.NONE)
    funded = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
