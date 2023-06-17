from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.models import User

from .forms import CustomUserCreationForm

from django.contrib import messages

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
            print("logged in")
            messages.success(request,"User successfully logged in")
            return redirect('store')
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
            return redirect('store')

    context ={'form':form, 'active_tab': 'register'}
    return render(request,'users/login_register.html',context)
