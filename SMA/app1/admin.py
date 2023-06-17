from django.contrib import admin
# from .models import Stock_Companies
from .models import *

# Register your models here.
 
# Register Book model
@admin.register(Stock_Companies)
class Stock_CompaniesAdmin(admin.ModelAdmin):
    list_display = ("symbol", "name","sectorName")

# Register Profile Model
admin.site.register(Profile)