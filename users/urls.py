from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerUser,name="register"),
    path('myAccount/',views.profile,name="profile"),
    path('order_details/<str:pk>/',views.order_details,name="order_details"),
    path('change_password/',views.changePassword,name='change_password'),
]
