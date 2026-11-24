import csv

from catalogue.models import MaterialType


def preload_starter_catalogue(*, user, flush=False, replace=True):
    if flush:
        MaterialType.objects.filter(user=user).all().delete()

    with open("data/catalogue-starter.csv", mode="r", newline="", encoding="utf-8") as file:
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