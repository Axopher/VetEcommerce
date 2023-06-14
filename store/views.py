from django.shortcuts import render,redirect
from .models import *

from django.http import JsonResponse, HttpResponse
import json



# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
    else:
        print("guess user")

    products = Product.objects.all()
    context = {'products':products,'items':items,'cart':cart}
    return render(request,"home.html",context)


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
    else:
        print("guess user")


    products = Product.objects.all()
    context = {'products':products,'items':items,'cart':cart}
    return render(request,"store/store.html",context)


def product_detail(request,pk):
    product = Product.objects.get(id=pk)
    customer = request.user.customer
    cart, created = Cart.objects.get_or_create(customer=customer)
    try:
        cartItem = CartItem.objects.get(cart__customer=customer,product=product)
        quantity = cartItem.quantity
        if quantity < 1:
            quantity = 0
    except:
        quantity = 0

    context = {"product":product,"quantity":quantity,'cart':cart}
    return render(request,"store/product_details.html",context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
    else:
        print("guess user")

        

    context = {'items':items,'cart':cart}
    return render(request,"store/cart.html",context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
    else:
        print("guess user")


    context = {'items':items,'cart':cart}
    return render(request,"store/checkout.html",context)


def update_cart(request):
    if request.method == 'POST':
        # Get the updated quantity values from the form data
        quantities = request.POST.getlist('quantity')
        print(quantities)
        # Get the cart items associated with the current user
        cart_items = CartItem.objects.filter(cart__customer=request.user.customer)
        # Update the quantities of the cart items
        for cart_item, quantity in zip(cart_items, quantities):
            cart_item.quantity = int(quantity)
            cart_item.save()

    # Redirect the user to a different page if the request method is not POST
    return redirect('cart')  

def clear_cart(request):
    # Get the cart items associated with the current user
    cart_items = CartItem.objects.filter(cart__customer=request.user.customer)

    # Delete all the cart items
    cart_items.delete()

    # Redirect the user to a different page if the request method is not POST
    return redirect('cart')

def updateCartItem(request):
    if request.method == 'GET':
        data = request.GET  # Get the data from the request
        product_id = data.get('product_id')  # Access the 'product_id' parameter
        action = data.get('action')  # Access the 'action' parameter

        if request.user.is_authenticated:
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                try:
                    product = Product.objects.get(id=product_id)
                    try:
                        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
                        cartItem, created = CartItem.objects.get_or_create(cart=cart,product=product)
                        print(cartItem)
                        if action == 'add':
                            cartItem.quantity = (cartItem.quantity + 1)
                        cartItem.save()
                        cartItems = cart.get_cart_items
                        return JsonResponse({"status":"Success","message":"added product to the cart","cartItems":cartItems})
                    except Exception as e:
                        print(e)
                        return JsonResponse({"status":"failed","message":"cart funcitonality failed"})
                            
                except Exception as e:
                    print(e)
                    return JsonResponse({'status':'Failed','message':'This product does not exists!!'})    
        else:
            return JsonResponse({'status':'Failed','message':'Please login to continue'})       
    else:
        return JsonResponse({'status':'Failed','message':'Invalid request!!'})       

def delete_from_cart(request):
    if request.method == 'GET':
        data = request.GET  # Get the data from the request
        cartItemID = data.get('cartItemID')  # Access the 'product_id' parameter
        action = data.get('action')  # Access the 'action' parameter
        print(cartItemID,action)
        if request.user.is_authenticated:
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                try:
                    print("inside here")
                    cartItem = CartItem.objects.get(id=cartItemID)
                    print(cartItem.quantity)
                    print(cartItem.cart.customer)
                    cartItem.delete()          
                    return JsonResponse({'status':'Success','message':'This cart item exists!!'})                 
                except Exception as e:
                    print(e)
                    return JsonResponse({'status':'Failed','message':'This product does not exists!!'})    
        else:
            return JsonResponse({'status':'Failed','message':'Please login to continue'})       
    else:
        return JsonResponse({'status':'Failed','message':'Invalid request!!'})       

