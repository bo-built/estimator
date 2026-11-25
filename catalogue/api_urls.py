from django.urls import path
from catalogue import api as api_views


app_name = 'catalogue_api'

urlpatterns = [
    path(
        'catalogue/api/workitems/',
        api_views.WorkItemsSerializer.as_view(),
        name='workitems_api',
    ),
    path(
        'catalogue/api/materialitems/',
        api_views.MaterialItemsSerializer.as_view(),
        name='materialitems_api',
    ),
]
