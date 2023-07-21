from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from datetime import datetime


class Slider(models.Model):

    discount_deal = (
        ('HOT-DEALS', 'HOTDEALS') ,
        ('NEW-ARRIVALS', 'NEW-ARRIVALS')
    )
    image = models.ImageField(upload_to='media/slider_images', null=True)
    discount_deal = models.CharField(choices=discount_deal, max_length=100)
    sale = models.IntegerField()
    brand_name = models.CharField(max_length=200)
    discount = models.IntegerField()
    link = models.CharField(max_length=500)

    def __str__(self) :
        return self.brand_name


class BannerArea(models.Model):
    image = models.ImageField(upload_to='media/banner_images')
    discount_deal = models.CharField(max_length=200)
    quote = models.CharField(max_length=200)
    offer_description = models.CharField(max_length=200, null=True)
    link = models.CharField(max_length=500, null=True)

    def __str__(self) :
        return self.quote



class MainCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) :
        return self.name
    
class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self) :
        return self.name + "--" + self.main_category.name
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self) :
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) :
        return self.name
    
    
class Color(models.Model):
    code = models.CharField(max_length=100)

    def __str__(self) :
        return self.code

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) :
        return self.name

    
class Product(models.Model):
    total_quantity = models.IntegerField()
    availability = models.IntegerField()
    product_name = models.CharField(max_length=100)
    featured_image = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    price = models.IntegerField()
    discount = models.IntegerField()
    tax = models.IntegerField(null=True)
    product_information = RichTextField()
    model_name = models.CharField(max_length=100)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    tags = models.CharField(max_length=100)
    description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self) :
        return self.product_name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "core_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)



class CouponCode(models.Model):
    code = models.CharField(max_length=100)
    discount = models.IntegerField()

    def __str__(self) :
        return self.code

    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200)

class AdditionalInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)




class UpcomingProduct(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/upcoming_product_images', null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self) :
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("up_product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "core_UpcomingProduct"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, UpcomingProduct)


class UpcomingProductImages(models.Model):
    product = models.ForeignKey(UpcomingProduct, on_delete=models.CASCADE)
    image = models.CharField(max_length=100)

class BlogSection(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) :
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    posted_by = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/blogs')
    posted_date = models.DateField(auto_now_add=True)
    tags = models.CharField(max_length=100, null=True)
    section = models.ForeignKey(BlogSection, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    


    def __str__(self) :
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("blog_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "core_Blog"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Blog.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Blog)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    postcode = models.IntegerField(null=True)
    email = models.EmailField()
    phone = models.IntegerField()
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    paid = models.BooleanField(default=False, null=True)
    date =models.DateField(default=datetime.today)

    def __str__(self) :
        return self.first_name
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    total = models.CharField(max_length=100)

    def __str__(self) :
        return self.product
    