from django.http import HttpResponse
from django.template import loader
from appuser.views import ProtectedView


class MaterialCatalogue(ProtectedView):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('catalogue/dashboard.html')
        context = {}
        return HttpResponse(template.render(context, request))
