from django.contrib import admin
from estimator import models


class BaseAggregateAdmin(admin.ModelAdmin):
    fields = [
        'estimated_charge',
        'estimated_cost',
        'estimated_profit',
        'realized_cost',
        'realized_profit',
    ]

    readonly_fields = fields


@admin.register(models.MaterialAggregate)
class MaterialAggregateAdmin(BaseAggregateAdmin):
    pass


@admin.register(models.WorkAggregate)
class WorkAggregateAdmin(BaseAggregateAdmin):
    pass


class BaseEstimateAdmin(admin.ModelAdmin):
    fields = [
        'project',
        'source',
        'name',
        'description',
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

    readonly_fields = [
        'estimated_cost',
        'estimated_charge',
        'estimated_profit',
        'realized_cost',
        'realized_profit',
    ]


@admin.register(models.MaterialItemEstimate)
class MaterialItemEstimateAdmin(BaseEstimateAdmin):
    pass


@admin.register(models.WorkItemEstimate)
class WorkItemEstimateAdmin(BaseEstimateAdmin):
    pass


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
