from rest_framework import serializers
from catalogue.models import (
    WorkType,
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
            'charge_rate',
            # 'api_url',
        ]


class WorkTypeSerializer(BaseItemTypeSerializer):
    class Meta(BaseItemTypeSerializer.Meta):
        model = WorkType


class MaterialTypeSerializer(BaseItemTypeSerializer):
    class Meta(BaseItemTypeSerializer.Meta):
        model = MaterialType
