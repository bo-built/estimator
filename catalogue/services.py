import csv

from catalogue.models import MaterialType, LaborType


def preload_materials_catalogue(*, user, flush=False, replace=True):
    if flush:
        MaterialType.objects.filter(user=user).all().delete()

    with open("data/material-catalogue-starter.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        lines = list(reader)
        for line in lines:
            material_type = None
            sku_fields = ['sku1', 'sku2', 'sku3']
            skus = [line[sku_field].strip() for sku_field in sku_fields if line[sku_field].strip()]

            sku = ('-').join(skus)
            exists = MaterialType.objects.filter(sku=sku, user=user).first()
            if exists and replace:
                material_type = exists
            elif not exists:
                material_type = MaterialType(user=user, sku=sku)

            if material_type:
                material_type.name = line['name']
                material_type.description = line['description']
                material_type.cost_rate = line['cost_rate']
                material_type.charge_multiplier = line['charge_multiplier'] or 2

                material_type.save()


def preload_labor_catalogue(*, user, flush=False, replace=True):
    if flush:
        LaborType.objects.filter(user=user).all().delete()

    with open("data/labor-catalogue-starter.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        lines = list(reader)
        for line in lines:
            labor_type = None
            sku = line['sku']
            exists = LaborType.objects.filter(sku=sku, user=user).first()
            if exists and replace:
                labor_type = exists
            elif not exists:
                labor_type = LaborType(user=user, sku=sku)

            if labor_type:
                labor_type.name = line['name']
                labor_type.description = line['description']
                labor_type.cost_rate = line['cost_rate']
                labor_type.charge_multiplier = line['charge_multiplier'] or 2

                labor_type.save()