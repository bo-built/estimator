from django.urls import path
from catalogue import views

app_name = 'catalogue'

urlpatterns = [
    path(
        'catalogue/',
        views.MaterialCatalogue.as_view(),
        name='catalogue_dasboard',
    ),
]
