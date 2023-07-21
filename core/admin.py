from django.contrib import admin
from .models import *

class ProductImage(admin.TabularInline):
    model = ProductImages

class AdditionalInformations(admin.TabularInline):
    model = AdditionalInformation

class Product_Admin(admin.ModelAdmin):
    inlines = (ProductImage, AdditionalInformations)
    list_display = ('product_name', 'categories','color', 'section', 'price')
    list_editable = ('categories', 'section', 'color')


class UpProductImage(admin.TabularInline):
    model = UpcomingProductImages

class Upcoming_Product_Admin(admin.ModelAdmin):
    inlines = (UpProductImage,)



admin.site.register(Section)
admin.site.register(Product, Product_Admin)
admin.site.register(ProductImages)
admin.site.register(AdditionalInformation)

admin.site.register(Slider)
admin.site.register(BannerArea)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(UpcomingProduct,Upcoming_Product_Admin)

admin.site.register(Blog)
admin.site.register(BlogSection)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(CouponCode)
admin.site.register(Order)
admin.site.register(OrderItem)