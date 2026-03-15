from django.contrib import admin
from django.utils.html import format_html
from .models import FoodItems


class FoodItemsAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'rating', 'Category', 'food_image')

    def food_image(self, obj):
        if obj.food_img:
            return format_html('<img src="{}" width="60" height="60" />', obj.food_img.url)
        return "No Image"

    food_image.short_description = "Image"


admin.site.register(FoodItems, FoodItemsAdmin)