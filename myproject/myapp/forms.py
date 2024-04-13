from django import forms
from .models import Client, Product, Order

# Форма для модели Client
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone_number', 'address']

# Форма для модели Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ['name', 'description', 'price', 'quantity']

# Форма для модели Order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'products']
