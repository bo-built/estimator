from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.name,
            self.user.username
        )

    @property
    def material_cost_total(self):
        sum = self.material_set.aggregate(total=Sum("total_cost"))
        return sum['total']

    @property
    def material_charge_total(self):
        sum = self.material_set.aggregate(total=Sum("total_charge"))
        return sum['total']

    @property
    def profit_on_materials(self):
        return self.material_charge_total - self.material_cost_total

    @property
    def labor_cost_total(self):
        sum = self.labor_set.aggregate(total=Sum("total_cost"))
        return sum['total']

    @property
    def labor_charge_total(self):
        sum = self.labor_set.aggregate(total=Sum("total_charge"))
        return sum['total']

    @property
    def profit_on_labor(self):
        return self.labor_charge_total - self.labor_cost_total


class LaborType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2)
    charge = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}: {} ${}/hr at ${}/hr'.format(
            self.user.username,
            self.name,
            self.pay_rate,
            self.charge,
        )


class Labor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    labor_type = models.ForeignKey(LaborType, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=10, decimal_places=2)
    pay_rate = models.DecimalField(
        help_text="This is initially copied from the source Labor type, but you can override it for this specific project.",  # noqa
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    charge = models.DecimalField(
        help_text="This is initially copied from the source Labor type, but you can override it for this specific project.",  # noqa
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    total_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.labor_type.name,
            self.project
        )

    def save(self, *args, **kwargs):
        if not self.pay_rate:
            self.pay_rate = self.labor_type.pay_rate

        if not self.charge:
            self.charge = self.labor_type.charge

        self.total_cost = self.set_total_cost()
        self.total_charge = self.set_total_charge()
        self.profit = self.set_profit()

        super().save(*args, **kwargs)

    def set_total_cost(self):
        if self.hours and self.pay_rate:
            return self.hours * self.pay_rate
        return 0

    def set_total_charge(self):
        if self.hours and self.charge:
            return self.hours * self.charge
        return 0

    def set_profit(self):
        return self.total_charge - self.total_cost


class MaterialType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    charge_multiplier = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}: {} ${}/hr at ${}/hr'.format(
            self.user.username,
            self.name,
            self.unit_cost,
            self.charge_multiplier,
        )


class Material(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(
        help_text="This is initially copied from the source Material type, but you can override it for this specific project.",  # noqa
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    charge_multiplier = models.DecimalField(
        help_text="This is initially copied from the source Material type, but you can override it for this specific project.",  # noqa
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    total_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.material_type.name,
            self.project
        )

    def save(self, *args, **kwargs):
        if not self.unit_cost:
            self.unit_cost = self.material_type.unit_cost

        if not self.charge_multiplier:
            self.charge_multiplier = self.material_type.charge_multiplier

        self.total_cost = self.set_total_cost()
        self.total_charge = self.set_total_charge()
        self.profit = self.set_profit()

        super().save(*args, **kwargs)

    def set_total_cost(self):
        if self.quantity and self.unit_cost:
            return self.quantity * self.unit_cost
        return 0

    def set_total_charge(self):
        if self.quantity and self.total_cost and self.charge_multiplier:
            return self.quantity * self.unit_cost * self.charge_multiplier
        return 0

    def set_profit(self):
        if self.total_charge and self.total_cost:
            return self.total_charge - self.total_cost
        return 0
