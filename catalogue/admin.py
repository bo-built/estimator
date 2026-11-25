from django.contrib import admin
from catalogue import models


class ProjectChargableAdmin(admin.ModelAdmin):
    readonly_fields = ['charge_per_unit', ]
    list_display = ['pk', 'name', 'cost_rate', 'charge_multiplier', 'charge_rate']
    list_display = ['sku', 'name', 'cost_rate', 'charge_multiplier', 'charge_rate']

    @admin.display(description='Charge Rate')
    def charge_per_unit(self, obj):
        if obj.charge_per_unit:
            return f'${obj.charge_per_unit:,.2f}'
        return '-'


@admin.register(models.MaterialType)
class MaterialTypeAdmin(ProjectChargableAdmin):
    pass


@admin.register(models.WorkType)
class WorkTypeAdmin(ProjectChargableAdmin):
    pass
