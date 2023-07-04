from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'username', 'full_name', 'email','phone','created_at','modified_at']
    search_fields = ['username','first_name','last_name','email','phone']


# Register your models here.
admin.site.register(Customer,CustomerAdmin)