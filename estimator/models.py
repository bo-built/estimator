from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

from catalogue.models import (MaterialType, LaborType)


class AggregateCalculationModel(models.Model):
    class Meta:
        abstract = True

    project = models.OneToOneField('Project', on_delete=models.CASCADE)
    estimated_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    estimated_profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    realized_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    realized_profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    @property
    def queryset(self):
        raise NotImplementedError(
            f'{self.__class__.__name__} must implement the "queryset"'
            ' property.'
        )

    def aggregate_values(self):
        self.set_estimated_cost()
        self.set_estimated_charge()
        self.set_estimated_profit()
        self.set_realized_cost()
        self.set_realized_profit()
        self.save()

    def set_estimated_cost(self):
        sum = self.queryset.aggregate(total=Sum('estimated_cost'))
        self.estimated_cost = sum['total'] or 0

    def set_estimated_charge(self):
        sum = self.queryset.aggregate(total=Sum('estimated_charge'))
        self.estimated_charge = sum['total'] or 0

    def set_estimated_profit(self):
        sum = self.queryset.aggregate(total=Sum('estimated_profit'))
        self.estimated_profit = sum['total'] or 0

    def set_realized_cost(self):
        sum = self.queryset.aggregate(total=Sum('realized_cost'))
        self.realized_cost = sum['total'] or 0

    def set_realized_profit(self):
        sum = self.queryset.aggregate(total=Sum('realized_profit'))
        self.realized_profit = sum['total'] or 0


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
            LaborCalculation.objects.create(project=self)
            MaterialCalculation.objects.create(project=self)
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
            (self.materialcalculation.estimated_charge or Decimal('0')) +
            (self.laborcalculation.estimated_charge or Decimal('0'))
        )

    def set_estimated_cost(self):
        self.estimated_cost = (
            (self.materialcalculation.estimated_cost or Decimal('0')) +
            (self.laborcalculation.estimated_cost or Decimal('0'))
        )

    def set_realized_cost(self):
        self.realized_cost = (
            (self.materialcalculation.realized_cost or Decimal('0')) +
            (self.laborcalculation.realized_cost or Decimal('0'))
        )

    def set_estimated_profit(self):
        self.estimated_profit = (
            (self.materialcalculation.estimated_profit or Decimal('0')) +
            (self.laborcalculation.estimated_profit or Decimal('0'))
        )

    def set_realized_profit(self):
        if self.invoiced_charge:
            calcation_value = self.invoiced_charge
        else:
            calcation_value = self.estimated_charge

        self.realized_profit = (calcation_value or Decimal('0')) - self.realized_cost


class LaborCalculation(AggregateCalculationModel):

    @property
    def queryset(self):
        return self.project.laborestimate_set


class MaterialCalculation(AggregateCalculationModel):

    @property
    def queryset(self):
        return self.project.materialestimate_set


class EstimatableCalculationModel(models.Model):
    class Meta:
        abstract = True

    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    estimated_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_rate = models.DecimalField(
        help_text="Override the source value if needed",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    charge_multiplier = models.DecimalField(
        help_text="Override the source value if needed",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    actual_quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    estimated_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    realized_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    realized_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    PARENT_OBJECT_KEY = None

    def save(self, *args, **kwargs):

        created = self.pk is None
        if created:
            parent = getattr(self, self.PARENT_OBJECT_KEY)
            if not self.cost_rate:
                self.cost_rate = parent.cost_rate
            if not self.charge_multiplier:
                self.charge_multiplier = parent.charge_multiplier

        self.update_calculations()

        super().save(*args, **kwargs)

        self.project.laborcalculation.aggregate_values()
        self.project.materialcalculation.aggregate_values()
        self.project.save()

    def update_calculations(self):
        self.set_estimated_cost()
        self.set_estimated_charge()
        self.set_estimated_profit()
        self.set_realized_cost()
        self.set_realized_profit()

    def set_estimated_cost(self):
        self.estimated_cost = (
            (self.cost_rate or Decimal("0")) *
            (self.estimated_quantity or Decimal("0"))
        )

    def set_estimated_charge(self):
        self.estimated_charge = (
            (self.cost_rate or Decimal("0")) *
            (self.charge_multiplier or Decimal("0")) *
            (self.estimated_quantity or Decimal("0"))
        )

    def set_estimated_profit(self):
        self.estimated_profit = (
            (self.estimated_charge or Decimal("0")) - (self.estimated_cost or Decimal("0"))
        )

    def set_realized_cost(self):
        if self.actual_quantity:
            quantity_for_calculation = self.actual_quantity
        else:
            quantity_for_calculation = self.estimated_quantity
        self.realized_cost = (quantity_for_calculation or Decimal("0")) * (self.cost_rate or Decimal("0"))

    def set_realized_profit(self):
        if self.realized_cost:
            quantity_for_calculation = self.realized_cost
        else:
            quantity_for_calculation = self.estimated_cost

        self.realized_profit = (
            (self.estimated_charge or Decimal("0")) -
            (quantity_for_calculation or Decimal("0"))
        )


class LaborEstimate(EstimatableCalculationModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    labor_type = models.ForeignKey(LaborType, on_delete=models.CASCADE)

    PARENT_OBJECT_KEY = 'labor_type'

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.labor_type.name,
            self.project
        )


class MaterialEstimate(EstimatableCalculationModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)

    PARENT_OBJECT_KEY = 'material_type'

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.material_type.name,
            self.project
        )
