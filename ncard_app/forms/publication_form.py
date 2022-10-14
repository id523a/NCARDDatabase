from django.forms import ModelForm
from ncard_app import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field
from crispy_forms.bootstrap import Tab, TabHolder

class PublicationForm(ModelForm):
    class Meta:
        model = models.Publication
        exclude = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "publication"
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            TabHolder(
                Tab('Publication Information',
                    HTML("<br>"),
                    Row('title'),
                    Row(Field('contributors', css_class='selectpicker form-control row', data_live_search='true')),
                    Row(
                        Column('publication_type', css_class='col-md-4 mb-0'),
                        Column('year', css_class='col-md-2 mb-0'),
                    ),
                    Row('ncard_publication'),
                ),

                Tab('Journal Information',
                    HTML("<br>"),
                    Row('journal'),
                    Row(
                        Column('journal_ISSN', css_class='col-md-6 mb-0'),
                        Column('volume', css_class='col-md-2 mb-0'),
                        Column('page_start', css_class='col-md-2 mb-0'),
                        Column('page_end', css_class='col-md-2 mb-0'),
                    ),
                    Row(
                        Column('open_access_status', css_class='col-md-2 mb-0'),
                        Column('doi', css_class='col-md-4 mb-0'),
                        Column('electronic_ISBN', css_class='col-md-3 mb-0'),
                        Column('print_ISBN', css_class='col-md-3 mb-0'),
                    ),
                ),

                Tab('Library Resources',
                    HTML("<br>"),
                    Row('abstract'),
                    Row('citation'),
                    Row('source_ID'),
                ),
            )
        )