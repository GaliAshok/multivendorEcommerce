from rest_framework import serializers
from rest_framework.fields import empty
from main.models import *
from django.contrib.auth.models import User



class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id','user','mobile','profile_img','categories']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.Meta.depth = 1
    
    def to_representation(self, instance):
        response =  super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response

class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id','user','address','mobile','profile_img','show_chart_daily_orders','show_chart_monthly_orders','show_chart_yearly_orders','total_products',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.Meta.depth = 1

    def to_representation(self, instance):
        response =  super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response

#Product

class ProductListSerializer(serializers.ModelSerializer):
    product_ratings = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id','category','vendor','demo_url','title','slug','tag_list',"details","price","usd_price",'product_ratings','image',
                  'product_file','tags','published_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.Meta.depth = 1 

#Image Serializer
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','product','image']


class ProductDetailSerializer(serializers.ModelSerializer):
    # product_rating=serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # will give only primarykey value(1,2,3..)
    product_imgs = ProductImageSerializer(many=True, read_only=True)
    product_rating = serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        many = True
        model = Product
        fields = ['id','category',"vendor",'title','slug','tag_list',"details","price","usd_price",'product_rating', 
                  "product_imgs",'demo_url','image','product_file',"downloads",'published_status','tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.Meta.depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['vendor'] = VendorSerializer(instance.vendor).data
        return response


#user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.Meta.depth = 1
 

 #Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','user', 'mobile','customer_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = 1
    

class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','user','mobile','customer_image','customer_orders']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = 1


# order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','customer','order_time','order_status','total_amount','total_usd_amount','payment_mode','trans_ref']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.Meta.depth = 1
        
# orderItems
class OrderItemSerializer(serializers.ModelSerializer):
    # order = OrderSerializer()
    # product = ProductDetailSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','order','product','qty','price','usd_price']

    def to_representation(self, instance):      #here we are sending the data 1 to 2, for the representation we are showing the data, by commenting above
        response = super().to_representation(instance)
        response['order'] = OrderSerializer(instance.order).data
        response['customer'] = CustomerSerializer(instance.order.customer).data
        response['user'] = UserSerializer(instance.order.customer.user).data
        response['product'] = ProductDetailSerializer(instance.product).data
        return response

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','order','product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = 1


class CustomerAddresSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ['id','customer','address','default_address',]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.Meta.depth = 1


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['id','customer','product','reviews','rating','date_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.Meta.depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = CustomerSerializer(instance.customer).data
        return response



# Category
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id','title', 'cat_img','details','total_downloads']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = 1

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id','title', 'details']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = 1


#WishListSerializer
class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ['id','product', 'customer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.Meta.depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = CustomerSerializer(instance.customer).data
        response['product'] = ProductDetailSerializer(instance.product).data
        return response