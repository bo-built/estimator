from django.urls import path
from catalogue import views

app_name = 'catalogue'

urlpatterns = [
    path(
        'material-catalogue/',
        views.MaterialCatalogue.as_view(),
        name='material_catalogue_dasboard',
    ),
    path(
        'work-catalogue/',
        views.WorkCatalogue.as_view(),
        name='work_catalogue_dasboard',
    ),
]
