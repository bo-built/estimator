from django.urls import path
from catalogue import api as api_views


app_name = 'catalogue_api'

urlpatterns = [
    path(
        'catalogue/api/laboritems/',
        api_views.LaborItemsSerializer.as_view(),
        name='laboritems_api',
    ),
    path(
        'catalogue/api/materialitems/',
        api_views.MaterialItemsSerializer.as_view(),
        name='materialitems_api',
    ),
]
