from django.contrib import admin
from estimator import models

admin.site.register(models.Project)
admin.site.register(models.LaborCalculation)
admin.site.register(models.MaterialCalculation)

admin.site.register(models.LaborEstimate)

admin.site.register(models.MaterialEstimate)


"""
@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'name',
        'description',

        'formatted_total_estimated_cost',
        'formatted_total_charge',
        'formatted_total_estimated_profit',

        'formatted_labor_cost_estimate',
        'formatted_labor_charge_total',
        'formatted_estimated_profit_on_labor',
        'formatted_realized_labor_cost',
        'formatted_realized_labor_profit',

        'formatted_material_cost_estimate',
        'formatted_material_charge_total',
        'formatted_profit_on_materials',

    ]
    readonly_fields = [
        'formatted_realized_labor_cost',
        'formatted_realized_labor_profit',
        'formatted_total_estimated_cost',
        'formatted_total_charge',
        'formatted_total_estimated_profit',
        'formatted_material_cost_estimate',
        'formatted_material_charge_total',
        'formatted_profit_on_materials',
        'formatted_labor_cost_estimate',
        'formatted_labor_charge_total',
        'formatted_estimated_profit_on_labor',
    ]

    @admin.display(description="Realized Cost of Labor")
    def formatted_realized_labor_cost(self, obj):
        if obj.realized_labor_cost:
            return f"${obj.realized_labor_cost:,.2f}"
        return "-"

    @admin.display(description="Realized Profit on Labor")
    def formatted_realized_labor_profit(self, obj):
        if obj.realized_labor_profit:
            return f"${obj.realized_labor_profit:,.2f}"
        return "-"

    @admin.display(description="Total Estimated Cost")
    def formatted_total_estimated_cost(self, obj):
        if obj.total_estimated_cost:
            return f"${obj.total_estimated_cost:,.2f}"
        return "-"

    @admin.display(description="Total Project Charge")
    def formatted_total_charge(self, obj):
        if obj.total_charge:
            return f"${obj.total_charge:,.2f}"
        return "-"

    @admin.display(description="Total Estimated Profit")
    def formatted_total_estimated_profit(self, obj):
        if obj.total_estimated_profit:
            return f"${obj.total_estimated_profit:,.2f}"
        return "-"

    @admin.display(description="Materials Charge")
    def formatted_material_charge_total(self, obj):
        if obj.material_charge_total:
            return f"${obj.material_charge_total:,.2f}"
        return "-"

    @admin.display(description="Estimated Materials Cost")
    def formatted_material_cost_estimate(self, obj):
        if obj.material_cost_estimate:
            return f"${obj.material_cost_estimate:,.2f}"
        return "-"

    @admin.display(description="Estimated Profit on Materials")
    def formatted_profit_on_materials(self, obj):
        if obj.estimated_profit_on_materials:
            return f"${obj.estimated_profit_on_materials:,.2f}"
        return "-"

    @admin.display(description="Estimated Cost of Labor")
    def formatted_labor_cost_estimate(self, obj):
        if obj.labor_cost_estimate:
            return f"${obj.labor_cost_estimate:,.2f}"
        return "-"

    @admin.display(description="Labor Charge")
    def formatted_labor_charge_total(self, obj):
        if obj.labor_charge_total:
            return f"${obj.labor_charge_total:,.2f}"
        return "-"

    @admin.display(description="Estimated Profit on Labor")
    def formatted_estimated_profit_on_labor(self, obj):
        if obj.estimated_profit_on_labor:
            return f"${obj.estimated_profit_on_labor:,.2f}"
        return "-"


@admin.register(models.Labor)
class LaborAdmin(admin.ModelAdmin):
    readonly_fields = [
        'total_cost',
        'total_charge',
        'actual_cost',
        'realized_profit',
        'profit',
    ]


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    readonly_fields = [
        'estimated_cost',
        'total_charge',
        'actual_cost',
        'realized_profit',
        'profit',
    ]


@admin.display(description="Total Materials Charge:")
def formatted_material_charge_total(self, obj):
    if obj.material_charge_total:
        return f"${obj.material_charge_total:,.2f}"
    return "-"

"""
