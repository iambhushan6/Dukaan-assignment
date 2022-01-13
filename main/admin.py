from itertools import product
from django.contrib import admin
from main.models import User, Store, Product, Cart, Category, Order
# Register your models here.

admin.site.register(User)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order)