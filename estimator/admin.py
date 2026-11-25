from django.contrib import admin
from estimator import models

admin.site.register(models.LaborCalculation)
admin.site.register(models.MaterialCalculation)


class BaseEstimateAdmin(admin.ModelAdmin):
    item_type_field = None

    readonly_fields = [
        'estimated_cost',
        'estimated_charge',
        'estimated_profit',
        'realized_cost',
        'realized_profit',
    ]

    def get_fields(self, request, obj=None):
        return [
            'project',
            self.item_type_field,
            'estimated_quantity',
            'cost_rate',
            'charge_multiplier',
            'actual_quantity',
            'estimated_cost',
            'estimated_charge',
            'estimated_profit',
            'realized_cost',
            'realized_profit',
        ]


@admin.register(models.MaterialEstimate)
class MaterialEstimateAdmin(BaseEstimateAdmin):
    item_type_field = 'material_type'


@admin.register(models.LaborEstimate)
class LaborEstimateAdmin(BaseEstimateAdmin):
    item_type_field = 'labor_type'


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'project_name',
        'description',
        'estimated_charge',
        'invoiced_charge',
        'estimated_cost',
        'realized_cost',
        'estimated_profit',
        'realized_profit',
    ]

    readonly_fields = [
        'estimated_charge',
        'estimated_cost',
        'realized_cost',
        'estimated_profit',
        'realized_profit',
    ]
