from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.models import User

from .forms import CustomUserCreationForm

from django.contrib import messages

from .models import Customer

from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm

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
    profile = get_object_or_404(Customer,user=request.user)
    profile_form = UserProfileForm(instance=profile)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request,"settings updated.")
            return redirect('profile')
        else:
            print(profile_form.errors)


    context = {
        'profile_form':profile_form
    }
    return render(request,"users/profile.html",context)