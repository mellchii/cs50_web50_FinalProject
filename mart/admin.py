from django.contrib import admin
from .models import User, Product, Order, OrderItem, Checkout, Wishlist, Reviews

# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Reviews)
admin.site.register(Wishlist)
admin.site.register(Checkout)