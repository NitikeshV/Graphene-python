from django.contrib import admin
from .models import Category,Pet,Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Pet)
admin.site.register(Product)