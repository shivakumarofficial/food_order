from django.urls import path
from learnapp import views

urlpatterns = [
    path('',views.registration,name='registration'),
    path('login/',views.user_login,name='login'),
    path('home/',views.home,name='home'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.user_profile,name='profile'),
    path('update/',views.user_update,name='update'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.user_details, name='user_details'),


]
