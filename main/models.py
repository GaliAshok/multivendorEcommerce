from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Count
import datetime



class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.PositiveBigIntegerField(unique=True,null=True)
    address = models.TextField(null = True)
    profile_img = models.ImageField(upload_to="seller_imgs/",null=True)

    
    def __str__(self) -> str:
        return self.user.username
    
    @property
    def show_chart_daily_orders(self):
        orders = OrderItem.objects.filter(product__vendor=self).values('order__order_time__date').annotate(Count('id'))
        dateList = []
        countList = []
        dataset = {}
        if orders:
            for order in orders:
                countList.append(order['id__count'])
                dateList.append(order['order__order_time__date'])
        dataset = {'dates':dateList, 'data':countList}
        return dataset
    
    @property
    def show_chart_monthly_orders(self):
        orders = OrderItem.objects.filter(product__vendor=self).values('order__order_time__month').annotate(Count('id'))
        dateList = []
        countList = []
        dataset = {}
        if orders:
            for order in orders:
                monthinteger = order['order__order_time__month']
                month = datetime.date(1900, monthinteger, 1).strftime('%B')                
                countList.append(order['id__count'])
                dateList.append(month)
                # dateList.append(order['order__order_time__month'])
        dataset = {'dates':dateList, 'data':countList}
        return dataset
    
    @property
    def show_chart_yearly_orders(self):
        orders = OrderItem.objects.filter(product__vendor=self).values('order__order_time__year').annotate(Count('id'))
        dateList = []
        countList = []
        dataset = {}
        if orders:
            for order in orders:
                countList.append(order['id__count'])
                dateList.append(order['order__order_time__year'])
        dataset = {'dates':dateList, 'data':countList}
        return dataset
    
    @property
    def total_products(self):
        product_count = Product.objects.filter(vendor=self).count()
        return product_count

    @property
    def categories(self):
        product_count = Product.objects.filter(vendor=self).values('category__title','category__id').order_by('category__title','category__id').distinct('category__title','category__id')
        return product_count


class ProductCategory(models.Model):
    title = models.CharField(max_length = 200)
    details = models.TextField(null = True)
    cat_img = models.FileField(upload_to='category_imgs/',null=True)


    def __str__(self) -> str:
        return self.title
    
    @property
    def total_downloads(self):
        total_downloads = 0
        products = Product.objects.filter(category=self)
        for product in products:
            if product.downloads:
                total_downloads += int(product.downloads)
        return total_downloads
    

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete = models.SET_NULL, null=True, related_name='category_product')
    vendor = models.ForeignKey(Vendor, on_delete = models.SET_NULL, null=True)
    title = models.CharField(max_length = 200)
    details = models.TextField(null = True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    usd_price = models.DecimalField(max_digits=10,decimal_places=2,default=80)
    slug = models.SlugField(unique=True, null=True)
    tags = models.TextField(null=True)
    image = models.ImageField(upload_to='product_imgs/',null=True)
    demo_url = models.URLField(null=True, blank=True)
    product_file = models.FileField(upload_to='product_files/',null=True)
    downloads = models.IntegerField(default=0)
    published_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generate the slug automatically when saving the object
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.title
    
    def tag_list(self):
        if self.tags:
            return self.tags.split(',') 
        else:
            return ['hi']

    
#Images

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_imgs')
    image = models.ImageField(upload_to='product_imgs/',null=True)

    def __str__(self):
        return self.image.url

# Customer

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.PositiveBigIntegerField()
    customer_image = models.ImageField(upload_to="customer_images/",null=True)

    def __str__(self) -> str:
        return f'{self.user.username}'
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_orders')
    order_time = models.DateTimeField(auto_now_add=True)
    order_status = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_usd_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    trans_ref = models.TextField(null=True, blank=True)
    payment_mode = models.TextField(max_length=200,null=True, blank=True)

    def __str__(self):
        return "%s" % (self.order_time)

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    usd_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)


    def __str__(self):
        return self.product.title
    

#customerAddress
class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name = 'customer_addresses')
    address = models.TextField()
    default_address = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.address
    
    class Meta:
        verbose_name_plural = 'Customer Addresses'
    

class ProductRating(models.Model):
    customer = models.ForeignKey(Customer, related_name='rating_customer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_rating', on_delete=models.CASCADE)
    rating = models.IntegerField()
    reviews = models.TextField()
    date_time = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'rating is: {self.rating} & review is : {self.reviews}'
    

class WishList(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Wish List'

    def __str__(self) -> str:
        return f'{self.product.title}-{self.customer.user.first_name}'