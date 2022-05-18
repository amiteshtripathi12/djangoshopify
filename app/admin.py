from django.contrib import admin
from .models import Customer, Product, Cart, OrderPlaced,Slider,Live_sale

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderPlaced)
admin.site.register(Slider)
admin.site.register(Live_sale)
# Register your models here.
