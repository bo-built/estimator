from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from appuser.views import ProtectedView


class MaterialCatalogue(ProtectedView):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('catalogue/catalogue.html')
        context = {
            'fetch_url': reverse('catalogue_api:materialitems_api'),
            'header': 'Materials',
        }
        return HttpResponse(template.render(context, request))


class WorkCatalogue(ProtectedView):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('catalogue/catalogue.html')
        context = {
            'fetch_url': reverse('catalogue_api:workitems_api'),
            'header': 'Work Type',
        }
        return HttpResponse(template.render(context, request))
