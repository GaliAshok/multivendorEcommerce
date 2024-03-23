from django.contrib import admin
from main.models import *

# Register your models here.

admin.site.register(Customer)

admin.site.register(Vendor)
admin.site.register(ProductCategory)
# admin.site.register(Customer)
# admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CustomerAddress)
admin.site.register(ProductRating)

admin.site.register(ProductImage)

class ProductImageInline(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price','usd_price','downloads']
    list_editable = ['usd_price']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]


class CutomerAdmin(admin.ModelAdmin):
    list_display = ['get_username','mobile']
    def get_username(self,obj):
        return obj.user.username
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','order_time','total_amount','total_usd_amount','order_status','payment_mode','trans_ref']
admin.site.register(Order,OrderAdmin)

#wihlist
class WishListAdmin(admin.ModelAdmin):
    list_display = ['id','customer','product']

admin.site.register(WishList,WishListAdmin)
