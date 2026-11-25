import csv

from catalogue.models import MaterialType, WorkType


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


def preload_work_catalogue(*, user, flush=False, replace=True):
    if flush:
        WorkType.objects.filter(user=user).all().delete()

    with open("data/work-catalogue-starter.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        lines = list(reader)
        for line in lines:
            work_type = None
            sku = line['sku']
            exists = WorkType.objects.filter(sku=sku, user=user).first()
            if exists and replace:
                work_type = exists
            elif not exists:
                work_type = WorkType(user=user, sku=sku)

            if work_type:
                work_type.name = line['name']
                work_type.description = line['description']
                work_type.cost_rate = line['cost_rate']
                work_type.charge_multiplier = line['charge_multiplier'] or 2

                work_type.save()