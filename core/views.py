from django.shortcuts import render,redirect
from core.models import Slider,BannerArea,MainCategory,Product,UpcomingProduct,Blog,Category,Color,Brand,CouponCode,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max, Min, Sum
from django.contrib.auth.decorators import login_required
from django.conf import settings
from cart.cart import Cart

from django.views.decorators.csrf import csrf_exempt

import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



def Base(request):
    return render(request, 'base.html')

def AboutUs(request):
    return render(request, 'main/about.html')

def ContactUs(request):
    return render(request, 'main/contact.html')

def Faq(request):
    return render(request, 'main/faq.html')

def BlogView(request):
    blog = Blog.objects.all()
    blogs = Blog.objects.filter(section__name = 'Popular Feeds')
    newblogs = Blog.objects.filter(section__name = 'New Blog')

    context ={
        'blog' : blog,
        'blogs' : blogs,
        'newblogs' : newblogs,
    }
    return render(request, 'main/blog.html', context)

def BlogDetail(request,slug):
    blog = Blog.objects.filter(slug = slug)

    if blog.exists():
        blog = Blog.objects.get(slug = slug)
    else:
        return redirect('404')
        
    context = {
        'blog' : blog,
    }
    return render(request, 'main/blog_detail.html', context)





def Home(request):
    sliders = Slider.objects.all()
    banners = BannerArea.objects.all()
    main_category = MainCategory.objects.all()
    product = Product.objects.filter(section__name = 'Top Deals Of The Day')
    products = Product.objects.filter(section__name = 'Top Featured Products')
    up_products = UpcomingProduct.objects.filter(section__name = 'New & Upcoming')
    
    context = {
        'sliders' : sliders,
        'banners' : banners,
        'main_category' : main_category,
        'product' : product,
        'products' : products,
        'up_products' : up_products
    }
    return render(request, 'main/home.html', context)


def Shop(request):
    category = Category.objects.all()
    product = Product.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    products = Product.objects.filter(section__name = 'Top Featured Products')

    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    ColorID = request.GET.get('ColorID')

    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)
        print(product)
    elif ColorID:
        product = Product.objects.filter(color = ColorID)
    
    else:
        product = Product.objects.all()
    

    context = {
        'category' : category,
        'product' : product,
        'min_price' : min_price,
        'max_price' : max_price,
        'FilterPrice' : FilterPrice,
        'color' : color, 
        'brand' : brand,   
        'products' : products,
    }

    return render(request, 'product/shop.html', context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()


    t = render_to_string('ajax/shop.html', {'product': allProducts})

    return JsonResponse({'data': t})


def ProductDetail(request,slug):
    product = Product.objects.filter(slug = slug)

    if product.exists():
        product = Product.objects.get(slug = slug)
    else:
        return redirect('404')
        
    context = {
        'product' : product,
    }
    return render(request, 'product/product_detail.html', context)

def Error404(request):
    return render(request,'error404/error404.html')


def UpcomingProductDetail(request,slug):
    up_product = UpcomingProduct.objects.filter(slug = slug)

    if up_product.exists():
        up_product = UpcomingProduct.objects.get(slug = slug)
    else:
        return redirect('404')
        
    context = {
        'up_product' : up_product,
    }
    return render(request, 'product/upcoming.html', context)

def MyAccount(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Email or Password")
            return redirect('login')
        

    return render(request, 'registration/login.html')

def MyAccountSignup(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username = username).exists():
            messages.error(request, "Username Already Exists")
            return redirect('handlesignup')
        
        if User.objects.filter(email = email).exists():
            messages.error(request, "Email already Exists")
            return redirect('handlesignup')

        user = User(
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account Created Successfully")
        return redirect('login')
    else:
        return render(request, 'registration/signup.html')

   

@login_required(login_url='/account/login')
def Profile(request):
    return render(request, 'profile/profile.html')


@login_required(login_url='/accounts/login/')
def ProfileUpdate(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        

        if password != None and password != "":
            user.set_password(password)
        user.save()
        return  redirect('profile')
    

@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    cart = request.session.get('cart')
    tax = sum(i.get('tax', 0) for i in cart.values() if i)

    coupon = None
    valid_coupon = None
    invalid_coupon = None

    if request.method =='GET':
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = CouponCode.objects.get(code=coupon_code)
                valid_coupon = "Are Applicable on Current Product"
            except:
                invalid_coupon = "Invalid Coupon code"


    context = {
        'tax' : tax,
        'coupon' : coupon,
        'valid_coupon' : valid_coupon,
        'invalid_coupon' : invalid_coupon,


    }
    return render(request, 'cart/cart.html', context)


def Checkout(request):
    amount_str = request.POST.get('amount')
    amount = int(float(amount_str) * 100)
    cart = request.session.get('cart')
    tax = sum(i.get('tax', 0) for i in cart.values() if i)


    payment = client.order.create(
        {
            "amount": amount, 
            "currency": "INR",
            "payment_capture" : "1"
        }
    )
    
    order_id = payment['id']

    context = {
        'tax' : tax,
        'order_id' : order_id,
        'payment' : payment,
    }
    return render(request, 'checkout/checkout.html', context)


def PlaceOrder(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        cart = request.session.get('cart')
        print(cart)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        district = request.POST.get('district')
        postcode = request.POST.get('postcode')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
       

        order_id = request.POST.get('order_id')
        tax = sum(i.get('tax', 0) for i in cart.values() if i)

        total_amount = 0 

        payment = request.POST.get('payment')

        
        context = {
            'order_id' : order_id,
            'tax' : tax,
            
        }

        order = Order(
            user = user,
            first_name = first_name,
            last_name = last_name,
            address = address,
            city = city,
            district = district,
            postcode = postcode,
            email = email,
            phone = phone,
            payment_id = order_id,
            amount = amount,
            
        )
        order.save()
        
        for i in cart:

            a = cart[i]['price']
            b = cart[i]['quantity']
            tax = sum(i.get('tax', 0) for i in cart.values() if i)

            print(type(a))
            print(type(b))

            item_total = a * b + tax  
            total_amount += item_total
            

            item = OrderItem(
                order = order,
                product = cart[i]['product_name'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = item_total
                
            )
            item.save()
            total = total_amount + tax  # Calculate the overall total amount

            context['total'] = total  # Add the 
        
        return render(request, 'checkout/placeorder.html', context)

@csrf_exempt
def Success(request):
    if request.method == 'POST':
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        user = Order.objects.filter(payment_id = order_id).first()
        user.paid = True
        user.save()
    return render(request, 'checkout/success.html')

    