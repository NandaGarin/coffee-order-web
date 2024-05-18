from django.contrib import admin
from . models import Product, Customer, Cart, Payment, WishList


# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "discounted_price", "category", "product_image"]


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user","locality","city","state","zipcode"]


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','paid']




@admin.register(WishList)
class WishListModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']
