from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class EstimableItemModel(models.Model):
    class Meta:
        abstract = True
        unique_together = ('sku', 'user')

    field_help_texts = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for field_name, help_text in cls.field_help_texts.items():
            field = cls._meta.get_field(field_name)
            field.help_text = help_text

    sku = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cost_rate = models.DecimalField(max_digits=10, decimal_places=2)
    charge_multiplier = models.DecimalField(max_digits=10, decimal_places=2, default=2)

    @property
    def charge_rate(self):
        if self.cost_rate and self.charge_multiplier:
            return self.cost_rate * self.charge_multiplier
        return 0


class WorkType(EstimableItemModel):

    def __str__(self):
        return 'Work Type <pk: {}>: {}'.format(
            self.pk,
            self.name,
        )

    field_help_texts = {
        'sku': 'Give this work type a unique identifier in your catalogue.',
        'cost_rate': (
            'How much do YOU pay per hour of this work type? Do you pay yourself $25/hr? '
            'Do you pay an employee $30/hr? Do you pay a contractor $100/hr?.',
        ),
        'charge_multiplier': (
            'How do you charge for this work type? At cost (1.0)? 2 times your cost?'
        ),
    }

    @property
    def api_url(self):
        return reverse(
            'catalogue_api:work_catalogue_item',
            kwargs={'item_pk': self.pk}
        )


class MaterialType(EstimableItemModel):

    # TO DO sku and user need to be unique but Meta is already declared

    def __str__(self):
        return 'Material Type <pk: {}>: {}'.format(
            self.pk,
            self.name,
        )

    field_help_texts = {
        'sku': 'Give this material a unique identifier in your catalogue.',
        'cost_rate': (
            'How much do YOU pay per unit of this material?',
        ),
        'charge_multiplier': (
            'How do you charge per unit of this material?'
        ),
    }

    @property
    def api_url(self):
        return reverse(
            'catalogue_api:material_catalogue_item',
            kwargs={'item_pk': self.pk}
        )
