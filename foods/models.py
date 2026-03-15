from django.db import models
from django.contrib.auth.models import User


Categories = [
    ("PIZZA","Pizza"),
    ("BURGERS","Burger"),
    ("FRENCH FRIES","French Fries"),
    ("DESSARTS","Dessarts"),
    ("BREVERAGES","Beverages"),
    ("MAIN_COURSE","Main Course"),
    ("ROOLS AND SANDWICH","Rools and Sandwich")
]


class FoodItems(models.Model):

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    rating = models.FloatField()
    description = models.TextField()
    food_img = models.ImageField(upload_to='foodimg/', blank=True, null=True)
    Category = models.CharField(max_length=100, choices=Categories)

    def __str__(self):
        return self.name


class SizeChart(models.Model):

    size_type = models.CharField(max_length=100)
    size_in_cm = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.size_type


class BaseType(models.Model):

    base_name = models.CharField(max_length=50)
    base_image = models.ImageField(upload_to='customizeimg/baseimg/')

    def __str__(self):
        return self.base_name


class Toppings(models.Model):

    topping_name = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    price = models.IntegerField()
    topping_image = models.ImageField(upload_to='customizeimg/toppingsimg/')

    def __str__(self):
        return self.topping_name


class Sauces(models.Model):

    sauce_name = models.CharField(max_length=50)
    sauce_image = models.ImageField(upload_to='customizeimg/saucesimg/')
    price = models.IntegerField()

    def __str__(self):
        return self.sauce_name


class Customized_Options(models.Model):

    food_name = models.CharField(max_length=100, choices=Categories)
    Sizechart = models.ForeignKey(SizeChart, on_delete=models.CASCADE)
    Base_type = models.ForeignKey(BaseType, on_delete=models.CASCADE)
    toppings = models.ForeignKey(Toppings, on_delete=models.CASCADE)
    sauces = models.ForeignKey(Sauces, on_delete=models.CASCADE)


class Cart(models.Model):

    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    rating = models.IntegerField()
    quantity = models.IntegerField(default=1)
    food_img = models.ImageField(upload_to='cartimg/', blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"