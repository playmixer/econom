from django.contrib import admin
from .models import Section, Wallet, CostCategory, IncomeCategory

# Register your models here.

admin.site.register(Section)
admin.site.register(Wallet)
admin.site.register(CostCategory)
admin.site.register(IncomeCategory)
