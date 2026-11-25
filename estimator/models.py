from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User

from estimator.model_classes import AggregateCalculationModel, EstimatableCalculationModel
from catalogue.models import (MaterialType, WorkType)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    estimated_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # override the estimated charge if desired:
    invoiced_charge = models.DecimalField(
        help_text='Set this if the invoiced amount is different from the estimated charge.',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    realized_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    estimated_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    realized_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('user', 'project_name')

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.project_name,
            self.user.username
        )

    def save(self, *args, **kwargs):
        created = self.pk is None
        if created:
            super().save(*args, **kwargs)
            WorkAggregate.objects.create(project=self)
            MaterialAggregate.objects.create(project=self)
            self.set_calculated_totals()
            self.save()
        else:
            self.set_calculated_totals()
            super().save(*args, **kwargs)

    def set_calculated_totals(self, save=False):
        self.set_estimated_charge()
        self.set_estimated_cost()
        self.set_realized_cost()
        self.set_estimated_profit()
        self.set_realized_profit()

    def set_estimated_charge(self):
        self.estimated_charge = (
            (self.materialaggregate.estimated_charge or Decimal('0')) +
            (self.workaggregate.estimated_charge or Decimal('0'))
        )

    def set_estimated_cost(self):
        self.estimated_cost = (
            (self.materialaggregate.estimated_cost or Decimal('0')) +
            (self.workaggregate.estimated_cost or Decimal('0'))
        )

    def set_realized_cost(self):
        self.realized_cost = (
            (self.materialaggregate.realized_cost or Decimal('0')) +
            (self.workaggregate.realized_cost or Decimal('0'))
        )

    def set_estimated_profit(self):
        self.estimated_profit = (
            (self.materialaggregate.estimated_profit or Decimal('0')) +
            (self.workaggregate.estimated_profit or Decimal('0'))
        )

    def set_realized_profit(self):
        if self.invoiced_charge:
            calcation_value = self.invoiced_charge
        else:
            calcation_value = self.estimated_charge

        self.realized_profit = (calcation_value or Decimal('0')) - self.realized_cost


class WorkAggregate(AggregateCalculationModel):

    def __str__(self):
        return "Work Aggregate Calculation <pk: {}> Project: {}".format(
            self.pk, self.project
        )

    @property
    def queryset(self):
        return self.project.workitemestimate_set


class MaterialAggregate(AggregateCalculationModel):

    def __str__(self):
        return "Material Aggregate Calculation <pk: {}> Project: {}".format(
            self.pk, self.project
        )

    @property
    def queryset(self):
        return self.project.materialitemestimate_set


class WorkItemEstimate(EstimatableCalculationModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)

    PARENT_OBJECT_KEY = 'work_type'

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.work_type.name,
            self.project
        )


class MaterialItemEstimate(EstimatableCalculationModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)

    PARENT_OBJECT_KEY = 'material_type'

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.material_type.name,
            self.project
        )
