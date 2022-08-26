from operator import truediv
import profile
from sunau import AUDIO_FILE_ENCODING_DOUBLE
from unittest.loader import VALID_MODULE_NAME
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
    organisation_ID = models.CharField('Organisation ID', max_length=50, blank=True)
    organisation_name = models.CharField('Organisation name', max_length=255, blank=True)
    primary_contact = models.CharField('Primary Contact', max_length=255, blank=True)
    organisation_phone = models.CharField('Organisation Phone', max_length=25, blank=True)
    website = models.CharField('Website', max_length=255, blank=True)
    twitter_handle = models.CharField('Twitter Handle', max_length=255, blank=True)
    organisation_type = models.CharField('Organisation Type', max_length=255, blank=True)

    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['name']

class HumanResource(models.Model):
    human_resource_ID = models.CharField('Human Resource ID', max_length=50, blank=True)
    contact_ID = models.CharField('Contact ID', max_length=50, blank=True)
    group_lead = models.CharField('Group Lead', max_length=255, blank=True)
    line_manager = models.CharField('Line Manager', max_length=255, blank=True)
    student_ID = models.CharField('Student ID', max_length=50, blank=True)
    staff_ID = models.CharField('Staff ID', max_length=50, blank=True)
    uwa_ID = models.CharField('UWA ID', max_length=50, blank=True)
    school_centre = models.CharField('School Centre', max_length=255, blank=True)
    hr_role = models.CharField('HR Role', max_length=255, blank=True)
    hr_start_date = models.DateField('HR Start Date', blank=True)
    hr_end_date = models.DateField('HR End Date', blank=True)
    year_phd_awarded = models.IntegerField('Year PHD Awarded', max_length=4,blank=True)
    employer1 = models.CharField('Employer 1', max_length=255, blank=True)
    employer2 = models.CharField('Employer 2', max_length=255, blank=True)
    hr_classification = models.CharField('HR Classification', max_length=255, blank=True)
    hr_level = models.IntegerField('HR Level', blank=True)
    fte = models.CharField('FTE', max_length=255, blank=True)
    cake_date = models.DateField('Cake Date', blank=True)

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

class grants(models.Model):
    grant_ID = models.CharField('Grant ID', max_length=50, blank=True)
    grant_reference = models.CharField('Grant Reference', max_length=255, blank=True)
    grant_title = models.CharField('Grant Title', max_length=255, blank=True)
    project_name = models.CharField('Project Name', max_length=255, blank=True)
    grant_lead_FN = models.CharField('Grant Lead FN', max_length=255, blank=True)
    grant_all_investigators = models.CharField('Grant All Investigators', max_length=255, blank=True)
    funding_agency = models.CharField('Funding Agency', max_length=255, blank=True)
    year_submitted = models.IntegerField('Year Submitted', max_length=4,blank=True)
    total_award = models.IntegerField('Total Award', blank=True)
    grant_status = models.CharField('Grant Status', max_length=255, blank=True)
    year_start = models.IntegerField('Year Start', max_length=4,blank=True)
    year_end = models.IntegerField('Year End', max_length=4,blank=True)
    business_unit = models.CharField('Business Unit', max_length=255, blank=True)
    uwa_pgnumber = models.IntegerField('UWA PG Number', blank=True)

class engagement(models.Model):
    engagement_ID = models.CharField('Engagement ID', max_length=50, blank=True)
    contact_name = models.CharField('Contact Name', max_length=255, blank=True)
    engagement_type = models.CharField('Engagement Type', max_length=255, blank=True)
    engagement_title = models.CharField('Engagement Title', max_length=255, blank=True)
    lead_organisation = models.CharField('Lead Organisation', max_length=255, blank=True)
    engagement_detail = models.CharField('Engagement Detail', max_length=255, blank=True)
    engagement_year = models.IntegerField('Engagement Year', max_length=4,blank=True)
    engagement_outcome = models.CharField('Engagement Outcome', max_length=255, blank=True)
    media_link = models.CharField('Media Link', max_length=255, blank=True)

class awards(models.Model):
    award_ID = models.CharField('Award ID', max_length=50, blank=True)
    award_type = models.CharField('Award Type', max_length=255, blank=True)
    award_agency = models.CharField('Award Agency', max_length=255, blank=True)
    award_name = models.CharField('Award Name', max_length=255, blank=True)
    award_recipient = models.CharField('Award Recipient', max_length=255, blank=True)
    award_status = models.CharField('Award Status', max_length=255, blank=True)
    award_detail =  models.TextField('Award Detail', blank=True)
    award_year = models.IntegerField('Award Year', max_length=4,blank=True)

class biography:
    bio_ID = models.CharField('Biography ID', max_length=50, blank=True)
    contact_ID = models.CharField('Contact ID', max_length=50, blank=True)
    bio_type = models.CharField('Bio Type', max_length=255, blank=True)
    profile_contact_name = models.CharField('Profile Contact Name', max_length=255, blank=True)

class events:
    event_ID = models.CharField('Event ID', max_length=50, blank=True)
    event_type = models.CharField('Event Type', max_length=255, blank=True)
    event_date = models.DateField('Event Date', blank=True)
    number_attendees = models.BigIntegerField('Number Of Attendees', blank=True)
    event_detail = models.TextField(blank=True)
    event_lead = models.CharField('Event Lead', max_length=255, blank=True)
    event_location = models.CharField('Event Location', blank=True)

class governance:
    field1 = models.CharField('Field1', blank=True)
    governance_ID = models.CharField('Governance ID', max_length=50, blank=True)
    governance_group = models.CharField('Governance Group', max_length=255,blank=True)
    member_name = models.CharField('Member Name', max_length=255,blank=True)

class enewssubscribers:
    e_news_ID = models.CharField('eNews ID', max_length=50, blank=True)
    first_name = models.CharField('First Name', max_length=64)
    last_name = models.CharField('Last Name', max_length=64)
    email_address = models.EmailField('email Address', blank=True)
    category = models.CharField('category', blank=True)
    audience_type = models.CharField('Audience Type', blank=True)

class students:
    student_ID = models.CharField('Student ID', max_length=50, blank=True)
    student_name = models.CharField('Student Name', max_length=64)
    student_type = models.CharField('Student Type', blank=True)
    primary_supervisor = models.CharField('Primary supervisor', max_length=255,blank=True)
    supervisor2 = models.CharField('Second supervisor', max_length=255,blank=True)
    supervisor3 = models.CharField('Third supervisor', max_length=255,blank=True)
    title_topic = models.TextField('title topic', blank=True)
    year_start = models.IntegerField('Award Year', max_length=4,blank=True)
    year_end = models.IntegerField('Award Year', max_length=4,blank=True)
    scholarship = models.CharField('Scholarship', max_length=255,blank=True)

class publications:
    publication_ID = models.CharField('Publication ID', max_length=50, blank=True)
    publication_type = models.CharField('Publication Type', blank=True)
    publication_year = models.DateField('Publication Date', blank=True)
    publication_title = models.CharField('Publication Title', max_length=255, blank=True)
    contributors = models.CharField('contributors', blank=True)
    journal = models.CharField('journal', max_length=255, blank=True)
    journal_ISSN = models.CharField('Journal ISSN', blank=True)
    volume = models.CharField('Volume', blank=True)
    pages = models.IntegerField('Pages', blank=True)
    open_access_status = models.CharField('open access status', blank=True)
    doi = models.CharField('DOI', blank=True)
    electronic_ISBN = models.CharField('Electronic ISBN', blank=True)
    print_ISBN = models.CharField('Print ISBN', blank=True)
    abstract =models.CharField('Abstract', blank=True)
    vancouver =models.CharField('Vancouver', blank=True)
    source_ID = models.CharField('source ID', max_length=50, blank=True)
    ncard_publication = models.CharField('NCARD publication', blank=True)

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