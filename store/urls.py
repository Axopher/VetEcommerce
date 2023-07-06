from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("store/",views.store,name="store"),
    path("product_detail/<str:pk>",views.product_detail,name="product_detail"),
    path("cart/",views.cart,name="cart"),
    path("checkout/",views.checkout,name="checkout"),
    path("contact/",views.contact,name="contact"),
    path("confirmation/",views.confirmation,name="confirmation"),
    path("process_order/",views.process_order,name="process_order"),
    path("update_cart/",views.update_cart,name="update_cart"),
    path("clear_cart/",views.clear_cart,name="clear_cart"),
    path("update_cart_item/",views.updateCartItem,name="update_cart_item"),
    path("delete_from_cart/",views.delete_from_cart,name="delete_from_cart"),
]
