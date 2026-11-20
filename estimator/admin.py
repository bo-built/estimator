from django.contrib import admin
from django import forms

from estimator import models


class ProjectForm(forms.ModelForm):
    model = models.Project
    fields = '__all__'


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm


@admin.register(models.Labor)
class LaborAdmin(admin.ModelAdmin):
    readonly_fields = [
        'total_cost',
        'total_charge',
        'profit',
    ]


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    readonly_fields = [
        'total_cost',
        'total_charge',
        'profit',
    ]
