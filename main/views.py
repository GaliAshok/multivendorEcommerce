from django.db import IntegrityError
from django.http import Http404, JsonResponse
from django.shortcuts import render
from rest_framework import generics, pagination, viewsets
from rest_framework.response import Response
from . import serializers
from main.models import *
from main import models
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.hashers import make_password
import razorpay


class VendorList(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = serializers.VendorSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'fetch_limit' in self.request.GET:
            limit = int(self.request.GET['fetch_limit'])
            qs = qs.annotate(downloads=Count('product')).order_by('-downloads','-id')
            qs = qs[:limit]
        return qs


class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = serializers.VendorDetailSerializer


# vendorCustomerList
class VendorProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        vendor_id = self.kwargs['vendor_id']
        qs = qs.filter(vendor__id=vendor_id)
        return qs



@csrf_exempt 
def vendor_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        try:
            # Check if the user with the given username or email already exists
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                raise IntegrityError("User with this username or email already exists.")
            
            #hash the password before creating the user
            hashpassword = make_password(password=password)
            
            user = User.objects.create(first_name=first_name, 
                                        last_name=last_name,
                                        email=email, 
                                        username=username,
                                        password=hashpassword,  #assinging hash password 
                                        )
            vendor = models.Vendor.objects.create(
                user=user, 
                mobile=mobile,
                address=address
                )
            msg = {
                'bool': True,
                'user': user.id,
                'vendor': vendor.id,
                'username':user.username,
                'msg': 'Thank you for registration! Please login.'
            }
        except IntegrityError as e:
            # Handle the case where the user already exists
            msg = {
                'bool': False,
                'msg': 'Oops! Username or email already exists.'
            }

        return JsonResponse(msg)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
    

#vendorLogin
    
@ csrf_exempt 
def vendor_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username,password=password)
    print(username,password,user)
    if user:
        try:
            vendor = Vendor.objects.get(user=user)
            msg = {
                'bool':True,
                'user':user.username,
                'id':vendor.id
            }
        except Vendor.DoesNotExist:
            msg ={
                'bool': False,
                'msg': 'Vendor does not exist'
            }
        
    else:
        msg={
            'bool':False,
            'msg':'invalid username/password'
    }
    return JsonResponse(msg)
    

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    pagination_class = pagination.PageNumberPagination
    # allowed_methods = ['POST']

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.GET.get('category')
        
        if "category" in self.request.GET:
            category = self.request.GET['category']
            category = models.ProductCategory.objects.get(id=category)
            qs = qs.filter(category=category)
        if 'fetch_limit' in self.request.GET:
            limit = int(self.request.GET['fetch_limit'])
            qs = qs[:limit]
        if 'popular' in self.request.GET:
            limit = int(self.request.GET['popular'])
            qs = qs.order_by('-downloads','-id')
            qs = qs[:limit]
        return qs
    

class TagProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.kwargs['tags']
        print(tag)
        qs = qs.filter(tags__icontains=tag)
        return qs
    
class ProductImgsList(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer
    # pagination_class = pagination.PageNumberPagination    //dont need pagination here. so i commented

    

class ProductImgsDetail(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        qs = super().get_queryset()
        product_id = self.kwargs['product_id']
        qs = qs.filer(product__id=product_id)
        return qs
    
class ProductImgDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer


class RelatedProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    # pagination_class = pagination.PageNumberPagination    dont need pagination here. so i commented

    def get_queryset(self):
        qs = super().get_queryset()
        product_id = self.kwargs['pk']
        product = models.Product.objects.get(id=product_id)
        qs = qs.filter(category=product.category).exclude(id=product_id)
        return qs


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductDetailSerializer


#Customer
    
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerDetailSerializer  

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer 

def null_view(request):
    # Handle the GET request
    data = {'message': 'This endpoint does not exist.'}
    return JsonResponse(data)

@csrf_exempt
def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print('user is',user)

        if user is not None:
            if user.is_authenticated:
                try:
                    customer = Customer.objects.get(user=user)
                    msg = {
                        'bool': True,
                        'user': user.username,
                        'id': customer.id
                    }
                    return JsonResponse(msg)
                except Customer.DoesNotExist:
                    msg = {
                        'bool': False,
                        'msg': 'Customer does not exist'
                    }
            else:
                msg = {
                    'bool': False,
                    'msg': 'User is not authenticated'
                }
        else:
            msg = {
                'bool': False,
                'msg': 'Invalid username/password'
            }
    else:
        msg = {
            'bool': False,
            'msg': 'Method not allowed'
        }

    return JsonResponse(msg)

    # username = request.POST.get('username')
    # password = request.POST.get('password')
    # user = authenticate(username=username, password=password)

    # if user:
    #     try:
    #         customer = Customer.objects.get(user=user)
    #         msg = {
    #             'bool': True,
    #             'user': user.username,
    #             'id': customer.id
    #         }
    #     except Customer.DoesNotExist:
    #         msg = {
    #             'bool': False,
    #             'msg': 'Customer does not exist'
    #         }
    # else:
    #     msg = {
    #         'bool': "false",
    #         'msg': 'Invalid username/password'
    #     }

    # return JsonResponse(msg)



@csrf_exempt 
def customer_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        try:
            # Check if the user with the given username or email already exists
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                raise IntegrityError("User with this username or email already exists.")
            
            # Check the mobile number is exists
            if models.Customer.objects.filter(mobile=mobile).exists():
                msg={
                    'bool':False,
                    'msg':'Oops! Mobile number is already Exists.'
                }
                return JsonResponse(msg)

            # Create the new user
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            customer = models.Customer.objects.create(user=user, mobile=mobile)
            msg = {
                'bool': True,
                'user': user.id,
                'customer': customer.id,
                'username':user.username,
                'msg': 'Thank you for registration! Please login.'
            }
        except IntegrityError as e:
            # Handle the case where the user already exists
            msg = {
                'bool': False,
                'msg': 'Oops! Username or email already exists.'
            }

        return JsonResponse(msg)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
    

# order
class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    # pagination_class = pagination.PageNumberPagination

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     return super().post(request, *args, **kwargs)


# ModifyOrderStatus
class OrderModify(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

# orderItem
class OrderItemList(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
    # pagination_class = pagination.PageNumberPagination

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     return super().post(request, *args, **kwargs)


# customerOrderItemList
class CustomerOrderItemList(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        customer_id = self.kwargs['pk']
        qs = qs.filter(order__customer__id=customer_id)
        return qs
    

# vendorOrderItemList
class VendorOrderItemList(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        vendor_id = self.kwargs['pk']
        qs = qs.filter(product__vendor__id=vendor_id)
        return qs
    

# vendorCustomerList
class VendorCustomerList(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        vendor_id = self.kwargs['pk']
        qs = qs.filter(product__vendor__id=vendor_id)
        return qs
    


# vendorCustomerList
class VendorCustomerOrderItemList(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        customer_id = self.kwargs['pk']
        vendor_id = self.kwargs['pk']
        qs = qs.filter(order__customer__id=customer_id,product__vendor__id=vendor_id)
        return qs


class OrderDetail(generics.ListAPIView):
    # queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderDetailSerializer

    def get_queryset(self):
        order_id = self.kwargs['pk']
        order = Order.objects.get(id=order_id)
        return OrderItem.objects.filter(order=order)
    

class CustomerAddressViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CustomerAddresSerializer
    queryset = CustomerAddress.objects.all()


class ProductRatingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProductRatingSerializer
    queryset = ProductRating.objects.all()


#category

class CategoryList(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'popular' in self.request.GET:
            limit = int(self.request.GET['popular'])
            qs = qs.annotate(downloads=Count('category_product')).order_by('-downloads','-id')
            qs = qs[:limit]
        return qs


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = serializers.CategoryDetailSerializer


from django.contrib.auth.hashers import make_password
@csrf_exempt
def vendor_change_password(request,vendor_id):
    password = request.POST.get('password')
    vendor = Vendor.objects.get(id=vendor_id)
    user = vendor.user
    user.password=make_password(password)
    user.save()
    msg = {'bool':True,"msg":"password has been changed"}
    return JsonResponse(msg)

@csrf_exempt
def customer_change_password(request,customer_id):
    password = request.POST.get('password')
    customer = Customer.objects.get(id=customer_id)
    user = customer.user
    user.password=make_password(password)
    user.save()
    msg = {'bool':True,"msg":"password has been changed"}
    return JsonResponse(msg)

         
@csrf_exempt
def update_oder_status(request,order_id):
    if request.method == 'POST':
        print(request.POST)
        if 'payment_mode' in request.POST:
            trans_ref = request.POST.get('trans_ref')
            payment_mode = request.POST.get('payment_mode')
            updateRes = models.Order.objects.filter(id=order_id).update(order_status=True,trans_ref=trans_ref,payment_mode=payment_mode)
        else:
            updateRes = models.Order.objects.filter(id=order_id).update(order_status=True)
            msg={
                'bool':False,
            }
        if updateRes:
            msg={
                'bool':True,
                }
    return JsonResponse(msg)

@csrf_exempt
def delete_customer_orders(request,customer_id):
    msg = {'bool':'false'}
    if request.method=='DELETE':
        try:
            result = Order.objects.filter(customer_id=customer_id).delete()
            if result:
                msg={
                    'bool':'true',
                }
        except Exception as e:
            print(e)

    return JsonResponse(msg)


@csrf_exempt
def update_product_download_count(request,product_id):
    if request.method == 'POST':
        product = models.Product.objects.get(id=product_id)
        totaldownloads = product.downloads
        totaldownloads +=1
        if totaldownloads == 0:
            totaldownloads=1
        updateRes = models.Product.objects.filter(id=product_id).update(downloads=totaldownloads)
        msg={
            'bool':False,
        }
        if updateRes:
            msg={
                'bool':True,
                }
    return JsonResponse(msg)


class WishList(generics.ListCreateAPIView):
    queryset = WishList.objects.all()
    serializer_class = serializers.WishListSerializer


@csrf_exempt
def check_in_wishlist(request):
    from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from . import models

@csrf_exempt
def check_in_wishlist(request):
    # if request.method == 'POST':
    #     product_id = request.POST.get('product')
    #     customer_id = request.POST.get('customer')
    #     CheckWishList = models.WishList.objects.filter(product__id=product_id,customer__id=customer_id).count()
    #     msg={
    #         'bool':False,
    #     }
    #     if CheckWishList > 0:
    #         msg={
    #             'bool':True,
    #             }
    # return JsonResponse(msg)
    if request.method == 'POST':
        product_id = request.POST.get('product')
        customer_id = request.POST.get('customer')
        
        # Check if the user is authenticated (logged in)
        if request.user.is_authenticated:
            # Query the wish list only if the user is authenticated
            check_wishlist = WishList.objects.filter(
                product__id=product_id,
                customer__id=customer_id
            ).count()
            
            msg = {'bool': check_wishlist > 0}
        else:
            msg = {'bool': False, 'msg': 'User is not authenticated.'}
        
        return JsonResponse(msg)
    else:
        return JsonResponse({'msg': 'Invalid request method.'}, status=400)



# customerWishItemList
class CustomerWishItemList(generics.ListAPIView):
    queryset = models.WishList.objects.all()
    serializer_class = serializers.WishListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        customer_id = self.kwargs['pk']
        qs = qs.filter(customer__id=customer_id)
        return qs
    

# customerWishItemList
class CustomerAddressList(generics.ListAPIView):
    queryset = models.CustomerAddress.objects.all()
    serializer_class = serializers.CustomerAddresSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        customer_id = self.kwargs['pk']
        qs = qs.filter(customer__id=customer_id).order_by('id')
        return qs
    

@csrf_exempt
def remove_from_wishlist(request):
    if request.method == 'POST':
        wishlist_item_id = request.POST.get('item_id')
        result = models.WishList.objects.filter(id=wishlist_item_id).delete()
        msg={
            'bool':False,
        }
        if result:
            msg={
                'bool':True,
                }
    return JsonResponse(msg)


@csrf_exempt
def mark_default_address(request,pk):
    msg={'bool':False,}
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        models.CustomerAddress.objects.all().update(default_address=False)
        result = models.CustomerAddress.objects.filter(id=address_id).update(default_address=True)
        if result:
            msg={
                'bool':True,
                }
    return JsonResponse(msg)


def customer_dashboard(request,pk):
    msg={'bool':False,}
    # customer_id = request.GET.get(pk)      not working
    customer_id = pk
    print(customer_id)
    totalAddress = models.CustomerAddress.objects.filter(customer__id=customer_id).count()
    totalOrder = models.Order.objects.filter(customer__id=customer_id).count()
    totalWishlist = models.WishList.objects.filter(customer__id=customer_id).count()
    msg={
        'totalAddress':totalAddress,
        'totalOrder' :totalOrder,  
        'totalWishlist':totalWishlist,
        }
    return JsonResponse(msg)


def vendor_dashboard(request,pk):
    vendor_id = pk
    totalProducts = models.Product.objects.filter(vendor_id=vendor_id).count()
    totalOrders = models.OrderItem.objects.filter(product__vendor__id=vendor_id).count()
    totalCustomers = models.OrderItem.objects.filter(product__vendor__id=vendor_id).values("order__customer").distinct().count()
    msg={
        'totalProducts':totalProducts,
        'totalOrders' :totalOrders,  
        'totalCustomers':totalCustomers,
        }
    return JsonResponse(msg)

@csrf_exempt
def create_razorpay_order(request):
    print(request.POST)
    client = razorpay.Client(auth=("rzp_test_e6xCFhzSwhLr96", "jb8PC96aAe7rOOcyp2EKJb5e"))
    DATA = {
        "amount": int(request.POST.get('amount')),
        "currency": "INR",
        "receipt": (request.POST.get('order_id')),
        # "notes": {
        #     "key1": "value3",
        #     "key2": "value2"
        # }
    }
    res = client.order.create(data=DATA)
    if res:
        msg={
            'bool':True,
             'Data':res
            }
    else:
        msg={
            'bool':False,
        }
    return JsonResponse(msg)