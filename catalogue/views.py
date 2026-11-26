from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from appuser.views import ProtectedView


class MaterialCatalogue(ProtectedView):
    def get(self, request):
        template = loader.get_template('catalogue/catalogue2.html')
        context = {
            'fetch_url': reverse('catalogue_api:material_catalogue'),
            'header': 'Materials',
            'unit_name': 'Unit',
        }
        return HttpResponse(template.render(context, request))


class WorkCatalogue(ProtectedView):
    def get(self, request):
        template = loader.get_template('catalogue/catalogue2.html')
        context = {
            'fetch_url': reverse('catalogue_api:work_catalogue'),
            'header': 'Work Type',
            'unit_name': 'Hour',
        }
        return HttpResponse(template.render(context, request))
