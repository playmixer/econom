from django.db import models
from django.contrib.auth.models import User


class Section(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='unique_section'),
        ]

    def __str__(self):
        return f"{self.user} - {self.title} - {self.id}"


class Wallet(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=100)
    cash = models.FloatField(default=0, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['section', 'title'], name='unique_wallet')
        ]

    def __str__(self):
        return f"{self.section} - {self.title} - {self.id}"


class CostCategory(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['section', 'title'], name='unique_cost_category')
        ]

    def __str__(self):
        return f"{self.section} - {self.title}"


class IncomeCategory(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['section', 'title'], name='unique_income_category')
        ]

    def __str__(self):
        return f"{self.section} - {self.title}"
