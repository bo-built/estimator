from django.db import models
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
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    def __str__(self):
        return '<pk: {}> {} // {}'.format(
            self.pk,
            self.name,
            self.project
        )

    def save(self, *args, **kwargs):
        if not self.pay_rate:
            self.pay_rate = self.labor_type.pay_rate

        if not self.charge:
            self.charge = self.labor_type.charge

        super().save(*args, **kwargs)

    @property
    def total_cost(self):
        if self.hours and self.pay_rate:
            return self.hours * self.pay_rate
        return 0

    @property
    def total_charge(self):
        if self.hours and self.charge:
            return self.hours * self.charge
        return 0

    @property
    def profit(self):
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
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    charge_multiplier = models.DecimalField(
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

        super().save(*args, **kwargs)

    @property
    def total_cost(self):
        if self.quantity and self.unit_cost:
            return self.quantity * self.unit_cost
        return 0

    @property
    def total_charge(self):
        if self.total_cost and self.charge_multiplier:
            return self.total_cost * self.charge_multiplier
        return 0

    @property
    def profit(self):
        return self.total_charge - self.total_cost
