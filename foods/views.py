from django.shortcuts import render, redirect, get_object_or_404
from foods.models import FoodItems, SizeChart, BaseType, Toppings, Sauces, Cart, Order
from foods.forms import AddFoodForm, EditForm, FoodForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# ---------------- FOOD DETAILS ----------------
@login_required(login_url='login')
def food_details(request, id=0):
    fooditem = get_object_or_404(FoodItems, id=id)
    return render(request, "foods/foodDetails.html", {'fooditem': fooditem})

# ---------------- ALL FOODS ----------------
@login_required(login_url='login')
def all_foods(request):
    foods = FoodItems.objects.all()
    return render(request, 'foods/allFoods.html', {'foods': foods})

# ---------------- CATEGORY FOODS ----------------
@login_required(login_url='login')
def category_foods(request, category):
    foods = FoodItems.objects.filter(Category=category)
    return render(request, 'foods/allFoods.html', {
        'foods': foods,
        'selected_category': category
    })

# ---------------- ADD FOOD (ADMIN ONLY) ----------------
@login_required(login_url='login')
def add_food(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = FoodForm()

    return render(request, 'add_food.html', {'form': form})

# ---------------- CUSTOMIZE FOOD ----------------
@login_required(login_url='login')
def customize_food(request, id=0):
    fooditem = get_object_or_404(FoodItems, id=id)
    return render(request, 'foods/customize.html', {
        'fooditem': fooditem,
        'bases': BaseType.objects.all(),
        'sizes': SizeChart.objects.all(),
        'toppings': Toppings.objects.all(),
        'sauces': Sauces.objects.all(),
    })

# ---------------- ADD TO CART ----------------
@login_required(login_url='login')
def add_to_cart(request, id):
    food = get_object_or_404(FoodItems, id=id)
    Cart.objects.create(
    food=food,
    name=food.name,
    price=food.price,
    rating=food.rating,
    quantity=1,
    food_img=food.food_img
)
    return redirect('cart')

# ---------------- CART PAGE ----------------
@login_required(login_url='login')
def cart_page(request):
    cart_items = Cart.objects.all()
    total_price = sum(item.price * item.quantity for item in cart_items)
    return render(request, 'foods/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# ---------------- EDIT CART ----------------
@login_required(login_url='login')
def edit_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    if request.method == 'POST':
        eCart = EditForm(request.POST, instance=cart_item)
        if eCart.is_valid():
            eCart.save()
            return redirect('cart')
    else:
        eCart = EditForm(instance=cart_item)

    return render(request, 'foods/editcart.html', {
        'eCart': eCart,
        'cart_item': cart_item
    })

# ---------------- DELETE CART ----------------
@login_required(login_url='login')
def delete_cart_item(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.delete()
    return redirect('cart')

# ================= ADMIN PANEL =================

# -------- ADMIN DASHBOARD --------
@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    foods_count = FoodItems.objects.count()
    orders_count = Order.objects.count()
    users_count = User.objects.count()
    foods = FoodItems.objects.all()[:6]

    context = {
        'foods_count': foods_count,
        'orders_count': orders_count,
        'users_count': users_count,
        'foods': foods
    }
    return render(request, 'admin_dashboard.html', context)

# -------- ADMIN ALL FOODS --------
@login_required(login_url='login')
def admin_allfoods(request):
    if not request.user.is_superuser:
        return redirect('home')

    foods = FoodItems.objects.all()
    return render(request, 'admin_all_foods.html', {'foods': foods})

# -------- VIEW ORDERS --------
@login_required(login_url='login')
def view_orders(request):
    if not request.user.is_superuser:
        return redirect('home')

    orders = Order.objects.all()
    return render(request, 'view_orders.html', {'orders': orders})

# -------- ADMIN USER DETAILS --------
@login_required(login_url='login')
def user_details(request):
    if not request.user.is_superuser:
        return redirect('home')

    users = User.objects.all()
    return render(request, 'user_details.html', {'users': users})

# -------- CONTACT MESSAGES --------
@login_required(login_url='login')
def contact_messages(request):
    if not request.user.is_superuser:
        return redirect('home')

    return render(request, 'contact_messeges.html')

# ---------------- EDIT FOOD ----------------
def edit_food(request, id):
    food = get_object_or_404(FoodItems, id=id)
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            return redirect('admin_all_foods')
    else:
        form = FoodForm(instance=food)

    return render(request, 'edit_food.html', {'form': form})

# ---------------- DELETE FOOD ----------------
def delete_food(request, id):
    food = get_object_or_404(FoodItems, id=id)
    food.delete()
    return redirect('admin_all_foods')


def make_order(request):
    if request.method == "POST":
        cart_items = Cart.objects.all()  # or filter by user if you add a user field

        for item in cart_items:
            Order.objects.create(
                user=request.user,  # logged-in user
                food=item.food,     # now works!
                quantity=item.quantity
            )

        cart_items.delete()

    return redirect('cart')