from django.shortcuts import render,redirect,get_object_or_404
from .models import *

from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.decorators import login_required

from .utils import searchProducts,paginateProducts

from users.models import Customer

from users.forms import UserProfileForm
from .forms import BillingForm
from django.contrib import messages
import uuid

from django.db.models import Sum

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()

    else:
        items = {}
        cart = {}

    new_arrivals = Product.objects.order_by('-created')[:8]
    best_sellers = Product.objects.annotate(sold_quantity=Sum('orderitem__quantity')).order_by('-sold_quantity')[:8]
    sale_items = Product.objects.filter(is_on_sale=True).order_by('-discount')[:8]

    products = Product.objects.all()
    context = {'products':products,'items':items,'cart':cart,'new_arrivals':new_arrivals,'best_sellers':best_sellers,'sale_items':sale_items}
    return render(request,"home.html",context)


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
    else:
        items = {}
        cart = {}


    category_id = request.GET.get('category_id')
    products, search_query = searchProducts(request, category_id)
    custom_range , products, num_of_results, total_results = paginateProducts(request,products,20)

    # categories operation
    categories = Category.objects.all()


    context = {'products':products,'items':items,'cart':cart,'search_query':search_query,'custom_range':custom_range,'total_results':total_results,'num_of_results':num_of_results,'categories':categories}
    return render(request,"store/store.html",context)


def product_detail(request,pk):
    product = Product.objects.get(id=pk)
    
    try:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        cartItem = CartItem.objects.get(cart__customer=customer,product=product)
        quantity = cartItem.quantity
        if quantity < 1:
            quantity = 0
            cartItem.delete()
            
        items = cart.cartitem_set.all()    
    except:
        cart = {}
        items = {}
        quantity = 0

    context = {"product":product,"quantity":quantity,'cart':cart,'items':items}
    return render(request,"store/product_details.html",context)

@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
    else:
        items = {}
        cart = {}

        

    context = {'items':items,'cart':cart}
    return render(request,"store/cart.html",context)

@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Customer,user=request.user)
        # preparing billing forms
        profile_form = UserProfileForm(instance=profile)
        billing_form = BillingForm(instance=profile)
        # showing custom cart info 
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()

        if not items:  # Add this check to see if the cart is empty
            messages.error(request, "Your cart is empty. Please add items before proceeding to checkout.", "empty_cart")
            return redirect('cart')  # Redirect back to the cart page

        if request.method == "POST":
            print(request.POST)
            print("inside request.POST")
            # Retrieve form data and store it in session variables
            request.session['billing_details'] = {
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'username': request.POST['username'],
                'address': request.POST['address'],
                'country': request.POST['country'],
                'city': request.POST['city'],
                'state': request.POST['state'],
                'pin_code': request.POST['pin_code'],
                'latitude': request.POST['latitude'],
                'longitude': request.POST['longitude'],
                'phone': request.POST['phone'],
                'email': request.POST['email'],
                'message': request.POST['message'],
            }
            
            
            return redirect('confirmation')

    else:
        items = {}
        cart = {}
        billing_form = {}

    

    context = {'items':items,'cart':cart,'billing_form':billing_form,'profile_form':profile_form}
    return render(request,"store/checkout.html",context)

@login_required(login_url='login')
def confirmation(request):
    billing_details = request.session.get('billing_details')
    print("here i am in confirmation page")
    print(billing_details)

    if billing_details:
        customer = request.user.customer
        print(customer)
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        
        context = {'items':items,'cart':cart,'billing_details': billing_details}
        return render(request, "store/confirmation.html", context)
    else:
        return redirect('checkout')


@login_required(login_url='login')
def process_order(request):
    billing_details = request.session.get('billing_details')
    username = billing_details['username']
    first_name = billing_details['first_name']
    last_name = billing_details['last_name']
    address = billing_details['address']
    country = billing_details['country']
    city = billing_details['city']
    state = billing_details['state']
    pin_code = billing_details['pin_code']
    latitude = billing_details['latitude']
    longitude = billing_details['longitude']
    phone = billing_details['phone']
    email = billing_details['email']
    order_notes = billing_details['message']

    if request.POST:
        try:
            customer = Customer.objects.get(username=username,email=email)  
            cart= Cart.objects.get(customer=customer)
            items = cart.cartitem_set.all()

            transaction_id = str(uuid.uuid4())

            order = Order.objects.create(
                customer=customer,
                transaction_id=transaction_id,
                order_notes=order_notes
            )

            for item in items:
                OrderItem.objects.create(
                    product=item.product,
                    order=order,
                    quantity=item.quantity,
                )

            order.complete = True
            order.save()

            items.delete()
            cart.delete()

            shipping_address = ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=address,
                country=country,
                state=state,
                city=city,
                pin_code=pin_code,
                latitude=latitude,
                longitude=longitude
            )

            messages.success(request,f"Your transaction id is {transaction_id}","payment_successful")
            del request.session['billing_details']
            return redirect("profile")
        except Exception as e:
            messages.error(request,"customer details did not match")
            return redirect('checkout')   
    else:
         messages.error(request,f"Payment Failed!!")   
    

@login_required(login_url='login')
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
        messages.success(request,"Cart Updated!")    

    # Redirect the user to a different page if the request method is not POST
    return redirect('cart')  

@login_required(login_url='login')
def clear_cart(request):
    # Get the cart items associated with the current user
    cart_items = CartItem.objects.filter(cart__customer=request.user.customer)

    # Delete all the cart items
    cart_items.delete()
    messages.success(request,"Cart Cleared!") 
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
                        if action == 'add':
                            cartItem.quantity = (cartItem.quantity + 1)
                        elif action == 'subtract':
                            if cartItem.quantity > 0:
                                cartItem.quantity -= 1

                        cartItem.save()  

                        count = cartItem.quantity
                        if count == 0:                           
                            if cartItem.quantity <= 0:
                                cartItem.delete()
                                count=0

                        cartItems = cart.get_cart_items

                        return JsonResponse({"status":"Success","message":action,"cartItems":cartItems,'count':count})
                    except Exception as e:
                        print(e)
                        return JsonResponse({"status":"Failed","message":"You do not have this item in your cart"})
                            
                except Exception as e:
                    print(e)
                    return JsonResponse({'status':'Failed','message':'This product does not exist!!'})    
        else:
            return JsonResponse({'status':'login_required','message':'Please login to continue'})       
    else:
        return JsonResponse({'status':'Failed','message':'Invalid request!!'})       

@login_required(login_url='login')
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
            return JsonResponse({'status':'login_required','message':'Please login to continue'})       
    else:
        return JsonResponse({'status':'Failed','message':'Invalid request!!'})       

