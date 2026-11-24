from django.db import models
from django.contrib.auth.models import User


class EstimableItemModel(models.Model):
    class Meta:
        abstract = True
        unique_together = ('sku', 'user')

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


class LaborType(EstimableItemModel):

    def __str__(self):
        return 'Labor Type <pk: {}>: {}'.format(
            self.pk,
            self.name,
        )


class MaterialType(EstimableItemModel):

    # TO DO sku and user need to be unique but Meta is already declared

    def __str__(self):
        return 'Material Type <pk: {}>: {}'.format(
            self.pk,
            self.name,
        )
