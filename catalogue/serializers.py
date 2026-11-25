from rest_framework import serializers
from catalogue.models import (
    LaborType,
    MaterialType,
)


class BaseItemTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = [
            'pk',
            'sku',
            'name',
            'description',
            'cost_rate',
            'charge_multiplier',
            # 'api_url',
        ]


class LaborTypeSerializer(BaseItemTypeSerializer):
    class Meta(BaseItemTypeSerializer.Meta):
        model = LaborType


class MaterialTypeSerializer(BaseItemTypeSerializer):
    class Meta(BaseItemTypeSerializer.Meta):
        model = MaterialType
