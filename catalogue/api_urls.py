from django.urls import path
from catalogue import api as api_views


app_name = 'catalogue_api'

urlpatterns = [
    path(
        'catalogue/api/workitems/',
        api_views.WorkItemsApi.as_view(),
        name='work_catalogue',
    ),
    path(
        'catalogue/api/workitems/<int:item_pk>/',
        api_views.WorkItemsApi.as_view(),
        name='work_catalogue_item',
    ),
    path(
        'catalogue/api/materials/',
        api_views.MaterialItemsApi.as_view(),
        name='material_catalogue',
    ),
    path(
        'catalogue/api/materialitems/<int:item_pk>/',
        api_views.MaterialItemsApi.as_view(),
        name='material_catalogue_item',
    ),
]
