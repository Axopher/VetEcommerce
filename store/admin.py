from django.contrib import admin
from .models import *
from django.utils.html import format_html

class ExtraImageInline(admin.StackedInline):
    model = ExtraImage
    extra = 0
    max_num = 5 



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'display_description', 'price','discount', 'created']
    list_filter = ['category__name']
    search_fields = ['name', 'category__name', 'price']
    inlines = [ExtraImageInline]  # Include the ExtraImageInline inlines

    def display_description(self, obj):
        max_length = 100  # Set the maximum number of characters to display
        if len(obj.description) > max_length:
            description = obj.description[:max_length] + '...'
        else:
            description = obj.description
        return format_html(description)

    display_description.short_description = 'Description'



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_total']
    can_delete = False

    def get_readonly_fields(self, request, obj=None):
        # Exclude all fields except for 'get_total'
        fields = [field.name for field in self.model._meta.get_fields() if field.name != 'get_total']
        return fields

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_ordered', 'status', 'transaction_id', 'get_order_total', 'get_order_items']
    list_editable = ['status']
    list_filter = ['status']
    search_fields = ['customer__username', 'transaction_id','date_ordered']
    inlines = [OrderItemInline]

    def get_order_total(self, obj):
        return obj.get_order_total
    get_order_total.short_description = 'Order Total'

    def get_order_items(self, obj):
        return obj.get_order_items
    get_order_items.short_description = 'Order Items Count'

    readonly_fields = ['id', 'customer', 'date_ordered', 'transaction_id', 'get_order_total', 'get_order_items']

    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'customer', 'date_ordered', 'status', 'transaction_id')
        }),
        ('Order Summary', {
            'fields': ('get_order_total', 'get_order_items')
        }),
    )

    # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False



class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['get_total']

class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created', 'updated', 'get_cart_total', 'get_cart_items']
    readonly_fields = ['get_cart_total', 'get_cart_items']
    search_fields = ['customer__username']
    inlines = [CartItemInline]

    def get_cart_total(self, obj):
        return obj.get_cart_total
    get_cart_total.short_description = 'Cart Total'

    def get_cart_items(self, obj):
        return obj.get_cart_items
    get_cart_items.short_description = 'Cart Items Count'


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude', 'date_added']
    search_fields = ['customer__username', 'order__status','order__transaction_id', 'address', 'country', 'state', 'city']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'created']




# Register your models here.
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)