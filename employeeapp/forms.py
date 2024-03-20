from django import forms
from .models import Products, Cart

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'image']

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']