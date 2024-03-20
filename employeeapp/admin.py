from django.contrib import admin
from .models import Department, Position, Employee, Products, Cart

# Register your models here.
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(Products)
admin.site.register(Cart)