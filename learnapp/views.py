from django.shortcuts import render, redirect
from learnapp.forms import UserForm, UserProfileForm, UserUpdateForm, UserProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from foods.models import FoodItems
from foods.forms import FoodForm
from django.contrib.auth.models import User


# ------------------ REGISTRATION ------------------

def registration(request):
    registered = False

    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = UserProfileForm(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():

            # Create user
            user = form1.save(commit=False)
            user.set_password(user.password)
            user.save()

            # Create profile
            profile = form2.save(commit=False)
            profile.user = user
            profile.save()

            registered = True

    else:
        form1 = UserForm()
        form2 = UserProfileForm()

    context = {
        'form1': form1,
        'form2': form2,
        'registered': registered
    }

    return render(request, "registration.html", context)


# ------------------ LOGIN ------------------
def user_login(request):

    # If already logged in
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            # Admin login
            if user.is_superuser:
                return redirect('admin_dashboard')

            # Normal user
            else:
                return redirect('home')

        else:
            return HttpResponse("Invalid username or password")

    return render(request, 'login.html')


# ------------------ LOGOUT ------------------

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


# ------------------ HOME PAGE ------------------

@login_required(login_url='login')
def home(request):
    foods = FoodItems.objects.all()

    return render(request, 'home.html', {
        'foods': foods
    })


# ------------------ ADMIN DASHBOARD ------------------

@login_required(login_url='login')
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect('home')

    foods = FoodItems.objects.all()

    context = {
        'foods': foods,
        'foods_count': foods.count(),
        'users_count': User.objects.count(),
        'orders_count': 0
    }

    return render(request, 'admin_dashboard.html', context)


# ------------------ USER PROFILE ------------------

@login_required(login_url='login')
def user_profile(request):

    return render(request, 'profile.html')


# ------------------ UPDATE PROFILE ------------------

@login_required(login_url='login')
def user_update(request):

    if request.method == 'POST':

        form = UserUpdateForm(request.POST, instance=request.user)
        form1 = UserProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.userdetails
        )

        if form.is_valid() and form1.is_valid():

            user = form.save()

            profile = form1.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('profile')

    else:

        form = UserUpdateForm(instance=request.user)
        form1 = UserProfileUpdateForm(instance=request.user.userdetails)

    context = {
        'form': form,
        'form1': form1
    }

    return render(request, 'update.html', context)


# ------------------ VIEW ALL USERS (ADMIN ONLY) ------------------

@login_required(login_url='login')
def user_details(request):

    if not request.user.is_superuser:
        return redirect('home')

    users = User.objects.all()

    return render(request, 'user_details.html', {
        'users': users
    })


def add_food(request):

    if request.method == 'POST':

        form = FoodForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('admin_allfoods')

    else:
        form = FoodForm()

    return render(request,'add_food.html',{'form':form})