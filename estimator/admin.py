from django.contrib import admin
from estimator import models


admin.site.register(models.MaterialType)

admin.site.register(models.LaborType)


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = [
        'material_charge_total',
        'material_cost_total',
        'profit_on_materials',
        'labor_cost_total',
        'labor_charge_total',
        'profit_on_labor',
    ]

    @admin.display(description="Total Materials Charge")
    def material_charge_total(self, obj):
        if obj.material_charge_total:
            return f"${obj.material_charge_total:,.2f}"
        return "$0.00"

    @admin.display(description="Total Materials Cost")
    def material_cost_total(self, obj):
        if obj.material_cost_total:
            return f"${obj.material_cost_total:,.2f}"
        return "$0.00"

    @admin.display(description="Profit on Materials")
    def profit_on_materials(self, obj):
        if obj.profit_on_materials:
            return f"${obj.profit_on_materials:,.2f}"
        return "$0.00"


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

@admin.display(description="Total Materials Charge:")
def formatted_material_charge_total(self, obj):
    if obj.material_charge_total:
        return f"${obj.material_charge_total:,.2f}"
    return "$0.00"
