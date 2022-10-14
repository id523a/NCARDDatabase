from email.policy import default
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.urls import reverse

#validators section

phone_validator = RegexValidator(r'^[ 0-9()+,*#-]*$', 'Phone numbers must contain only these characters: #()*+,-0123456789')
# ORCID ident. format based on https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier
orcid_validator = RegexValidator(r'^$|^https://orcid\.org/\d{4}-\d{4}-\d{4}-\d{3}(\d|X)$', 'ORCID identifier must be a full URL, in this format: https://orcid.org/XXXX-XXXX-XXXX-XXXX')
# https://help.twitter.com/en/managing-your-account/twitter-username-rules
twitter_validator = RegexValidator(r'^$|^@[A-Za-z0-9_]+$', 'Twitter handle must begin with an @ and only contain letters, digits and underscores.')
nonnegative_validator = MinValueValidator(0, 'Value must not be negative.')
country_code_validator = RegexValidator(r'^[A-Z]{2}$', 'Country code must be two upper-case letters, e.g. AU')

class Organisation(models.Model):
    class OrganisationType(models.IntegerChoices):
        NONE = 0, '-'
        HEALTH_EDUCATION_RESEARCH = 1, 'Health/Education/Research'
        FUNDING_AGENCY = 2, 'Funding Agency'
        COMMUNITY = 3, 'Community'
        SERVICE_PROVIDER = 4, 'Service Provider'

    name = models.CharField('name', max_length=255)
    organisation_type = models.IntegerField('type', choices=OrganisationType.choices, default=OrganisationType.NONE)
    primary_contact = models.ForeignKey('ncard_app.Person', on_delete=models.RESTRICT, null=True, blank=True, related_name='organisations_primary_contact')
    phone = models.CharField('phone', max_length=25, blank=True, validators=[phone_validator])
    website = models.URLField('website', blank=True)
    twitter_handle = models.CharField('Twitter handle', max_length=16, blank=True, validators=[twitter_validator])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = "Organisation"

class Country(models.Model):
    code = models.CharField('country code', max_length=2, primary_key=True, validators=[country_code_validator])
    name = models.CharField('name', max_length=255)

    def __str__(self):
        return f'{self.code} - {self.name}'

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'countries'
        db_table = "Country"

class Person(models.Model):
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

    class Clinician(models.IntegerChoices):
        NO = 0, 'No'
        YES = 1, 'Yes'

    title = models.CharField(max_length=16, blank=True)
    given_name = models.CharField('First Name',max_length=64)
    middle_name = models.CharField('Middle Name',max_length=64, blank=True)
    surname = models.CharField('Last Name', max_length=64, blank=True)
    surname_first = models.BooleanField(default=False)
    auth_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='person')
    email = models.EmailField('Primary Email', blank=True)
    email2 = models.EmailField('Secondary Email', blank=True)
    phone_office = models.CharField('phone (Office)', max_length=25, blank=True, validators=[phone_validator])
    phone_mobile = models.CharField('phone (Mobile)', max_length=25, blank=True, validators=[phone_validator])
    phone_home = models.CharField('phone (Home)', max_length=25, blank=True, validators=[phone_validator])
    cre_role = models.CharField('CRE Role', max_length=15, blank=True)
    ncard_relation = models.IntegerField('relationship with NCARD', choices=NCARDRelation.choices, default=NCARDRelation.OTHER)
    project = models.CharField(max_length=50, blank=True)
    display_on_website = models.IntegerField(choices=DisplayOnWebsite.choices, default=DisplayOnWebsite.NO)
    profile_url = models.URLField('Profile URL', blank=True)
    orcid_id = models.CharField('ORCID iD', max_length=37, blank=True, validators=[orcid_validator])
    scopus_id = models.BigIntegerField('Scopus ID', null=True, blank=True, validators=[nonnegative_validator])
    wos_researcher_id = models.CharField('WoS ResearcherID', max_length=32, blank=True)
    google_scholar = models.URLField('Google Scholar', blank=True)
    researchgate = models.URLField('ResearchGate', blank=True)
    loop_profile = models.URLField('Loop Profile', blank=True)
    linkedin = models.URLField('LinkedIn (URL)', blank=True)
    twitter = models.CharField('Twitter Handle (please include "@")', max_length=16, blank=True, validators=[twitter_validator])
    employers = models.ManyToManyField(Organisation, blank=True, related_name='employees')
    location = models.CharField(max_length=50, blank=True)
    organisation_primary = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts_primary_org', verbose_name='Organisation (Primary)')
    organisation_other = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts_other_org', verbose_name='Organisation (Other)')
    clinician = models.IntegerField(choices=Clinician.choices, default=Clinician.NO)
    research_focus = models.CharField('Research Focus',max_length=255, blank=True)
    work_line1 = models.CharField('Line 1', max_length=64, blank=True)
    work_line2 = models.CharField('Line 2', max_length=64, blank=True)
    work_line3 = models.CharField('Line 3', max_length=64, blank=True)
    work_suburb = models.CharField('Suburb',max_length=32, blank=True)
    work_state = models.CharField('State (abbrev.)', max_length=3, blank=True)
    work_postcode = models.CharField('Postcode', max_length=20, blank=True)
    work_country = models.ForeignKey(Country, on_delete=models.RESTRICT, to_field='code', default='AU', related_name='+', verbose_name='Country')
    home_line1 = models.CharField('Line 1', max_length=64, blank=True)
    home_line2 = models.CharField('Line 2', max_length=64, blank=True)
    home_line3 = models.CharField('Line 3', max_length=64, blank=True)
    home_suburb = models.CharField('Suburb', max_length=32, blank=True)
    home_state = models.CharField('State (abbrev.)', max_length=3, blank=True)
    home_postcode = models.CharField('Postcode', max_length=20, blank=True)
    home_country = models.ForeignKey(Country, on_delete=models.RESTRICT, to_field='code', default='AU', related_name='+', verbose_name='Country')
    notes = models.TextField(blank=True)


    @property
    def full_name(self):
        if self.surname_first:
            names = (self.surname, self.given_name, self.middle_name)
        else:
            names = (self.given_name, self.middle_name, self.surname)
        return ' '.join(filter(None, names))

    def __str__(self):
        return f'{self.full_name} [{self.id}]'
        
    def get_absolute_url(self):
        return reverse('edit-person', args=[self.id])

    class Meta:
        verbose_name_plural = 'people'
        ordering = ['surname', 'given_name', 'id']
        indexes = [
            models.Index(fields=['surname']),
            models.Index(fields=['given_name'])
        ]
        db_table = "Person"

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
        db_table = "Project"

class Award(models.Model):
    class AwardType(models.IntegerChoices):
        PRIZE = 1, 'Prize'
        SCHOLARSHIP = 2, 'Scholarship'

    class AwardStatus(models.IntegerChoices):
        AWARDEE = 1, 'Awardee'
        NOMINEE = 2, 'Nominee'
        FINALIST = 3, 'Finalist'

    name = models.CharField('Name', max_length=255)
    award_type = models.IntegerField('type', choices=AwardType.choices)
    agency = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True, related_name='awards')
    recipients = models.ManyToManyField(Person, related_name='awards')
    status = models.IntegerField('Award Status', choices=AwardStatus.choices, default=AwardStatus.AWARDEE)
    detail = models.TextField('details', blank=True)
    year = models.PositiveSmallIntegerField('Year Established')
    no_year = models.DecimalField(verbose_name="Concurrent Years",default=1.0, max_digits=10, decimal_places=1, null=True, blank=True)
    notes = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f'{self.name} {self.year}'

    class Meta:
        ordering = ['-year']
        db_table = "Award"

# The Biography table is not a high priority at the moment, and it is complicated to support thanks to the attachment column.
# class Biography(models.Model):
#     person = models.OneToOneField(Person, on_delete=models.RESTRICT, related_name='biography')
#     bio_type = # choice of 'CV Full', 'CV Short' and 'Profile'
#     cv_attachment = # Microsoft Access supports multiple files in the Attachment column.

#     def __str__(self):
#         return str(self.person)

class Event(models.Model):
    title = models.CharField('Title', max_length=255, blank=True)
    event_type = models.CharField('type', max_length=255)
    date = models.DateField('date')
    location = models.CharField('location', max_length=255, blank=True)
    lead_organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, blank=True, null=True, related_name='events')
    lead_contacts = models.ManyToManyField(Person, blank=True, related_name='events')
    number_attendees = models.IntegerField('number of Attendees', blank=True)
    # The participants field is deliberately not ManyToManyField(Person). This allows for the free-form participation info seen in the existing spreadsheet.
    participants = models.TextField('participants', blank=True)
    detail = models.TextField('details', blank=True)


    def __str__(self):
        if not self.title:
            return f'{self.date} - {self.detail}'
        return f'{self.date} - {self.title}'

    class Meta:
        ordering = ['-date']
        db_table = "Event"

class Publication(models.Model):
    class OpenAccessStatus(models.IntegerChoices):
        NONE = 0, 'None'
        OPEN = 1, 'Open'
        CLOSED = 2, 'Closed'
        INDETERMINATE = 3, 'Indeterminate'
        EMBARGOED = 4, 'Embargoed'

    title = models.TextField('title')
    publication_type = models.CharField('type', max_length=255) # integer choices
    ncard_publication = models.BooleanField('NCARD publication', default=True)
    year = models.PositiveSmallIntegerField('year')
    contributors = models.ManyToManyField(Person, related_name='publications')
    journal = models.CharField('journal', max_length=255)
    journal_ISSN = models.CharField('journal ISSN', max_length=255) # add validator
    volume = models.PositiveSmallIntegerField('volume', blank=True, null=True)
    page_start = models.PositiveIntegerField('start page', blank=True, null=True)
    page_end = models.PositiveIntegerField('end page', blank=True, null=True)
    open_access_status = models.IntegerField(choices=OpenAccessStatus.choices, default=OpenAccessStatus.NONE)
    doi = models.CharField('doi', max_length=255)
    electronic_ISBN = models.CharField('electronic ISBN', max_length=255, blank=True)
    print_ISBN = models.CharField('print ISBN', max_length=255, blank=True)
    abstract = models.TextField('abstract', blank=True)
    citation = models.TextField('citation (Vancouver)', blank=True)
    source_ID = models.CharField('source ID', max_length=50, blank=True) # check type

    def __str__(self):
        if self.ncard_publication:
            return f'NCARD - {self.title}'
        return self.title

    class Meta:
        ordering = ['-year']
        db_table = "Publication"

class Grant(models.Model):
    title = models.CharField(max_length=255, blank=True)
    reference = models.CharField(max_length=64, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='grants')
    investigators = models.ManyToManyField(Person, through='GrantInvestigator', related_name='grants')

    def __str__(self):
        name = self.title or 'Grant'
        return f'{name} [{self.id}]'
    
    class Meta:
        db_table = "Grant"

class GrantInvestigator(models.Model):
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE, related_name='+')
    investigator = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='+')
    chief = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['grant', 'investigator'], name='grantinvestigator_unique')
        ]
        db_table = "GrantInvestigator"

class Students(models.Model): 
    class StudentTypes(models.IntegerChoices):
        HONS = 1, 'Honours'
        PHD = 2, 'PhD'

    student_name = models.OneToOneField(Person, on_delete=models.CASCADE, related_name = 'person')
    student_type = models.IntegerField('Student Type', choices= StudentTypes.choices)
    supervisor = models.ManyToManyField(Person, blank=True)
    title_topic = models.TextField('Title Topic', blank=True)
    year_start = models.PositiveSmallIntegerField('Year Start',blank=True,null=True)
    year_end = models.PositiveSmallIntegerField('Year End',blank=True,null=True)
    scholarship = models.OneToOneField(Award, on_delete=models.SET_NULL, null=True, blank=True, related_name='award')

    def __str__(self):
        return self.student_name
    
    class Meta:
        ordering = ['student_name']
        db_table = "Student"