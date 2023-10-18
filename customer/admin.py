from django.contrib import admin
from .models import *
from .models import Post

from .models import SellerApprovedProduct

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','selling_price','discount_price','brand','category','product_image']



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['user','name','locality','city','pincode','state']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['user','customer','product','quantity','Order_date','status']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['user','product','quantity','size']




class PostAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug', 'status', 'created_on')
  list_filter = ('status',)
  search_fields = ['title', 'content']
  
admin.site.register(Post, PostAdmin)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display=['ban_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['cat_name']


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display=['f_name','l_name']


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display=['poster_name']


admin.site.register(Whishlist)

@admin.register(CustProfile)
class CustProfileAdmin(admin.ModelAdmin):
    list_display=['user']


from .models import Seller

class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_address', 'mobile_no')
    list_filter = ('company_name',)
    search_fields = ('company_name', 'company_address', 'mobile_no')
    ordering = ('company_name',)

# Register the Seller model with the SellerAdmin class
admin.site.register(Seller, SellerAdmin)



@admin.register(SellerProduct)
class SellerProductAdmin(admin.ModelAdmin):
    list_display=['title','selling_price','discount_price','brand','category','product_image']



admin.site.register(SellerApprovedProduct)