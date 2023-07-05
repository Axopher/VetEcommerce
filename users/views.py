from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.models import User

from .forms import CustomUserCreationForm

from django.contrib import messages

from .models import Customer
from store.models import Order,Cart

from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm

from .filters import OrderFilter
from .utils import paginateOrders

from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def loginUser(request):
    form = CustomUserCreationForm()
    context = {'form':form, 'active_tab': 'login'}
    if request.user.is_authenticated:
        return redirect('store')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            pass
        # authenticate queries the the database to check if username and password match
        user = authenticate(request,username=username,password=password)

        if user is not None:
            # it creates session id in session table and also adds it to browser cookies
            login(request,user)
            messages.success(request,"User successfully logged in")
            return redirect('profile')
        else:
            messages.error(request,"Failed to log in!!")
            

    return render(request,'users/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.success(request,"User successfully logged out")
    return redirect('login')

def registerUser(request):
    form = CustomUserCreationForm()
    if request.user.is_authenticated:
        return redirect('store')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,"Your account has been registered successfully")
            login(request, user)            
            return redirect('profile')

    context ={'form':form, 'active_tab': 'register'}
    return render(request,'users/login_register.html',context)

@login_required(login_url='login')
def profile(request):
    # getting profile information
    profile = get_object_or_404(Customer,user=request.user)
    profile_form = UserProfileForm(instance=profile)
    
    # getting customer orders data
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(customer=customer)

    orderFilter = OrderFilter(request.GET,queryset=orders)
    orders = orderFilter.qs
    
    active_tab = request.GET.get('active_tab', 'dashboard')

    custom_range, orders = paginateOrders(request, orders,10)

    form = CustomPasswordChangeForm(request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST,instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            # Assign the user value to the profile instance
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
        else:
            print(profile_form.errors)

    # getting cart items
    cart, created = Cart.objects.get_or_create(customer=customer)
    items = cart.cartitem_set.all()

    context = {
        'profile_form':profile_form,
        'orders':orders,
        'orderFilter':orderFilter,
        'active_tab':active_tab,
        'custom_range':custom_range,
        'form':form,
        'items':items,
        'cart':cart,
    }

    return render(request,"users/profile.html",context)

def order_details(request,pk):
    order  = Order.objects.get(id=pk)
    print(order)
    for orderitem in order.orderitem_set.all():
        print(orderitem.product.name)

    context = {'order':order}
    return render(request,"users/order_details.html",context) 

@login_required(login_url="login")
def changePassword(request):
    print("password change")
    form = CustomPasswordChangeForm(request.user)
    if request.method == 'POST':

        print("changing password here ")
        form = CustomPasswordChangeForm(request.user, request.POST)

        if(form.is_valid()):
            user = form.save()
            update_session_auth_hash(request, user)  # Update session
            messages.success(request, 'Password was successfully updated!! Please log in again')
            logout(request)  # Log out the user
            return redirect('login')
    
    context = {
        'form':form,
    }
    return render(request,"profile.html",context)       