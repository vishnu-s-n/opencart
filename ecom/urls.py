"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [

    #404 error page
    path('404',views.Error404, name='404'),

    
    path('admin/', admin.site.urls),
    path('base/', views.Base,name='base'),
    path('',views.Home, name='home'),
    path('about',views.AboutUs, name="about"),
    path('contact',views.ContactUs, name='contact'),
    path('blog', views.BlogView, name='blogs'),
    path('faq',views.Faq, name='faq'),
    
    path('blog/<slug:slug>',views.BlogDetail, name='blog_detail'),
    path('shop',views.Shop, name='shop'),
    path('shop/filter-data',views.filter_data,name="filter-data"),

    path('product/<slug:slug>',views.ProductDetail, name='product_detail'),
    path('products/<slug:slug>',views.UpcomingProductDetail, name='up_product_detail'),
    path('account/login',views.MyAccount, name='handlelogin'),
    path('account/register',views.MyAccountSignup, name='handlesignup'),
    path('account/profile',views.Profile, name='profile'),
    path('account/profile/update', views.ProfileUpdate, name='profile_update'),

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('checkout/',views.Checkout,name='checkout'),
    path('cart/checkout/placeorder', views.PlaceOrder, name='placeorder'),
    path('success/',views.Success, name='success'),


    path('accounts/', include('django.contrib.auth.urls'))


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
