from django.urls import path
from foods import views

urlpatterns = [
    path('allfoods/', views.all_foods, name='allfoods'),
    path('allfoods/<str:category>/', views.category_foods, name='category_foods'),
    path('add/', views.add_food, name='add_food'),

    path('<int:id>/', views.food_details, name='food_details'),
    path('customize/<int:id>/', views.customize_food, name='customize_food'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart'),
    path('Edit-Cart/<int:id>/', views.edit_cart, name='edit_cart'),
    path('delete-cart/<int:id>/', views.delete_cart_item, name='delete_cart'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-allfoods/', views.admin_allfoods, name='admin_all_foods'),
    path('orders/', views.view_orders, name='view_orders'),
    path('contact-messages/', views.contact_messages, name='contact_messages'),
    path('add-food/', views.add_food, name='addnewfood'),
    path('make-order/', views.make_order, name='make_order'),
    path('edit-food/<int:id>/', views.edit_food, name='edit_food'),
    path('delete-food/<int:id>/', views.delete_food, name='delete_food'),
]