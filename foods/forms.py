from django import forms
from .models import FoodItems, Cart


class AddFoodForm(forms.ModelForm):
    class Meta:
        model = FoodItems
        fields = ['name', 'price', 'rating', 'Category', 'food_img', 'description']


class EditForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']


class FoodForm(forms.ModelForm):

    class Meta:
        model = FoodItems
        fields = ['name','price','rating','Category','description','food_img']