import django_tables2 as tables
from django_tables2.export.views import ExportMixin

from ncard_app import models
from ncard_app.views import tables_class

class TableView(ExportMixin, tables.SingleTableView):
    table_class = MyTable
    model = Person
    template_name = "django_tables2/bootstrap.html"