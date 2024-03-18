from django.db import models

# Create your models here.
class Department(models.Model):
    dname = models.CharField(max_length=100)

    def __str__(self):
        return f"{ self.dname }"

class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{ self.title }"

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

class Products(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.name }"