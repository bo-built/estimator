from decimal import Decimal
from django.db import models
from django.db.models import Sum


class AggregateCalculationModel(models.Model):
    """ This Model Class holds all of the aggregated calculations for a Project.
        It calculates the totals of e.g. all linked material estimates into a
        single sum.

        These values could just be properties of Project defined in the model,
        but this future proofs the application for planned features where project
        totals can be directly queried.
    """
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


class EstimatableCalculationModel(models.Model):
    """ This Model Class represents single instances of e.g. a material or work
        type, which needs to be estimated in order to calculate a total  estimate
        for a project.

        Properties from the source catalogue item are copied to the estimable item
        instance so that they can be tailored for a specific project.
    """
    class Meta:
        abstract = True

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.source.name,
            self.project
        )

    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

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

    def save(self, *args, **kwargs):
        """ If the user has not set specific cost/charge values for this instance
            copy them from the catalogue source instance. Otherwise, keep the
            provided user input values.

            Copy the name and description from the source instace. This future
            proofs this object from changes or deletion of the source object.

            Essentially, an estimate just gets initial information from the
            catalogue, but is not coupled to the catalogue item going forward.
        """
        created = self.pk is None
        if created:
            if not self.cost_rate:
                self.cost_rate = self.source.cost_rate
            if not self.charge_multiplier:
                self.charge_multiplier = self.source.charge_multiplier
            self.name = self.source.name
            self.description = self.source.description

        self.update_calculations()

        super().save(*args, **kwargs)

        self.project.workaggregate.aggregate_values()
        self.project.materialaggregate.aggregate_values()
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
        self.realized_cost = (
            (quantity_for_calculation or Decimal("0")) *
            (self.cost_rate or Decimal("0"))
        )

    def set_realized_profit(self):
        if self.realized_cost:
            quantity_for_calculation = self.realized_cost
        else:
            quantity_for_calculation = self.estimated_cost

        self.realized_profit = (
            (self.estimated_charge or Decimal("0")) -
            (quantity_for_calculation or Decimal("0"))
        )
