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
            f"{self.__class__.__name__} must implement the 'queryset'"
            ' property.'
        )

    def get_estimated_cost(self):
        sum = self.queryset.aggregate(total=Sum("estimated_cost"))
        return sum['total'] or 0

    def get_estimated_charge(self):
        sum = self.queryset.aggregate(total=Sum("estimated_charge"))
        return sum['total'] or 0

    def get_estimated_profit(self):
        sum = self.queryset.aggregate(total=Sum("estimated_profit"))
        return sum['total'] or 0

    def get_realized_cost(self):
        sum = self.queryset.aggregate(total=Sum("realized_cost"))
        return sum['total'] or 0

    def get_realized_profit(self):
        sum = self.queryset.aggregate(total=Sum("realized_profit"))
        return sum['total'] or 0


class EstimatableCalculationModel(models.Model):
    class Meta:
        abstract = True

    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    estimated_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    charge_multiplier = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    actual_quanitity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    realized_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    realized_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        '''needed?
        '''
        self.update_calculations()
        super().save(*args, **kwargs)

    def update_calculations(self):
        self.get_estimated_cost()
        self.get_estimated_charge()
        self.get_estimated_profit()
        self.get_realized_cost()
        self.get_realized_profit()

    def get_estimated_cost(self):
        return self.cost_per_unit * self.estimated_quantity

    def get_estimated_charge(self):
        return self.cost_per_unit * self.charge_multiplier * self.estimated_quantity

    def get_estimated_profit(self):
        return self.estimated_charge - self.estimated_cost

    def get_realized_cost(self):
        if self.actual_quanitity:
            quantity_for_calculation = self.actual_quanitity
        else:
            quantity_for_calculation = self.estimated_quantity
        return quantity_for_calculation * self.cost_per_unit

    def get_realized_profit(self):
        if self.realized_cost:
            quantity_for_calculation = self.realized_cost
        else:
            quantity_for_calculation = self.estimated_cost
        return self.total_charge - quantity_for_calculation


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    estimated_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # override the estimated charge if desired:
    realized_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

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
        created = self.pk is not None
        if created:
            LaborCalculation.objects.create(project=self)
            MaterialCalculation.objects.create(project=self)
        super().save(*args, **kwargs)


class LaborCalculation(AggregateCalculationModel):

    @property
    def queryset(self):
        self.project.labor_set


class MaterialCalculation(AggregateCalculationModel):

    @property
    def queryset(self):
        self.project.material_set


class LaborEstimate(EstimatableCalculationModel):
    labor_type = models.ForeignKey(LaborType, on_delete=models.CASCADE)

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.labor_type.name,
            self.project
        )


class MaterialEstimate(EstimatableCalculationModel):
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.material_type.name,
            self.project
        )

