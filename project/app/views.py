from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,SetPasswordForm
from .forms import loginform
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .forms import (identify,EmailForm,RegisterForm,CheckoutForm)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .models import (ProductItem,Product,ProductCategory,SizeOption,OrderItem,UserModel,SizeOption,ProductVariation,Address,Order,Payment)



# Create your views here.
def  create_user(request):
    fm=RegisterForm()
    context={
        'form':fm
    }
    if request.method == 'POST':
        fm=RegisterForm(data=request.POST)
        if fm.is_valid():

            fm.save()
            messages.success(request,'user register successfully')
            return redirect('signin')
           
    return render(request,'register.html',context)

def signin(request):
    fm=loginform()
    context={
        'form':fm
    }
    if request.method == 'POST':
        fm=loginform(data=request.POST)
        if fm.is_valid():
            username=fm.cleaned_data['username']
            pwd=fm.cleaned_data['password']
            user=authenticate(request,username=username,password=pwd)
            if user:
                if user.is_authenticated:
                    login(request,user)
                    messages.success(request,'user account created successfully')
                    return redirect('home')
                    
                messages.error(request,'invalid username and password')
                # return HttpResponse('invalid username and password')
    return render(request,'login.html',context)

@login_required(login_url='/signin/')
def home(request):
    return render(request,'home.html')

def signout(request):
    return redirect('signin')

@login_required(login_url='/signin/')
def PasswordChange(request):
    username=request.user
    user=User.objects.get(username=username)
    fm=PasswordChangeForm(user)
    context={
        'form':fm
    }
    if request.method== 'POST':
        fm=PasswordChangeForm(user,data=request.POST)
        if fm.is_valid():
            user=fm.save()
            return HttpResponse('Password changed')
            send_mail('user login',
                    user.username+'password change',
                    'prakruthimp016@gmail.com',
                    [email],
                     fail_silently=True)
            
        return HttpResponse('invalid password')
    return render(request,'pwd_change.html',context)


def reset_password(request, username):
        user = User.objects.get(username=username)  
        fm = SetPasswordForm(user) 
        context = {
            'form': fm,
        }
        if request.method == "POST":
            form = SetPasswordForm(user, data=request.POST)  
            if form.is_valid():
                form.save() 
                messages.success(request, "Password has been reset successfully.")
                return redirect("login") 
            else:
                messages.error(request, "Please correct the errors below.")
       
        return render(request, 'resetpwd.html', context)



    
def identifyview(request):
    fm=identify()
    context={
        'form':fm
    }
    if request.method == 'post':
        fm=identify(request.POST)
        if fm.is_valid():
            username=fm.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                url='/resetpwd/'+username+'/'
                return redirect(url)
            return redirect('signin')
    return render(request,'identify.html',context)
    
# display product
def product(request):
    products = ProductItem.objects.all()
    context={
        'products':products
    }
    return render(request,'product.html',context)

# single product
def product_details(request,slug):
    if ProductItem.objects.filter(slug=slug).exists():
        product = ProductItem.objects.get(slug=slug)

        context={
            'products':product,
        }
        return render(request,'products_details.html',context)
    return HttpResponse('Product does not exist')


def category_detail(request, slug):
    if ProductCategory.objects.filter(slug=slug).exists():
        category = ProductCategory.objects.get(slug=slug)
        
        products=Product.objects.filter(product_category__exact=category)
        product_items=ProductItem.objects.filter(product__in=products)
        context={
                 
            'products':    product_items
        }
        return render(request, 'category_detail.html', context)
    return HttpResponse('invalid category')


def home(request):
    categories=ProductCategory.objects.all()
    products = ProductItem.objects.all()
    context={
        'categories':categories,
        'products':products
    }
    return render(request,'home.html',context)


@login_required(login_url='signin/')
def add_to_cart(request,productitemslug,sizeslug):
    username=request.user
    user =UserModel.objects.get(username=username)
    productitem=ProductItem.objects.get(slug=productitemslug)
    sizeoption=SizeOption.objects.get(slug=sizeslug)
    if OrderItem.objects.filter(user=user,product_item=productitem).exists():
        item=OrderItem.objects.get(user=user,product_item=productitem)
        url='/increment/'+str(item.id)+'/'
        return redirect(url)
    OrderItem.objects.create(user=user,product_item=productitem,size=sizeoption)
    return HttpResponse('product added to cart successfully')

def increment_quentity(request,id):
    orderitem=OrderItem.objects.get(id=id)
    product_item=ProductItem.objects.get(slug=orderitem.product_item.slug)
    size=SizeOption.objects.get(slug=orderitem.size.slug)
    product_variation=ProductVariation.objects.get(product_item= product_item,size_option=size)

    if orderitem.quantity < product_variation.qty_in_stock:
        orderitem.quantity +=1
        orderitem.save()
        return HttpResponse("quantity incremented successfully")
    return HttpResponse('product out of stock')

def decrement_quentity(request,id):
    orderitem=OrderItem.objects.get(id=id)
    
    if orderitem.quantity > 1:
        orderitem.quantity -=1
        orderitem.save()
        return HttpResponse("quantity decrement successfully")
    return HttpResponse('product out of stock')


def remove_orderitem(request,id):
    user=UserModel.objects.get(username=request.user)
    if OrderItem.objects.filter(id=id,user=user).exists():
        orderitem=OrderItem.objects.get(id=id,user=user)
        orderitem.delete()
        return HttpResponse('order removed from the cart')
    return HttpResponse('item does not exists in cart')

from datetime import datetime

def Checkout(request):
    user = UserModel.objects.get(username=request.user)
    checkoutform = CheckoutForm()
    context = {
        'checkoutform': checkoutform
    }
    if request.method == 'POST':
        
        checkoutform = CheckoutForm(request.POST)
        if checkoutform.is_valid():
            use_default_shipping_address = checkoutform.cleaned_data['use_default_shipping_address']

            if use_default_shipping_address and  Address.objects.filter(user=user,address_type='S',default=True).exists():
                shipping_address = Address.objects.get(user=user,address_type='S',default=True)
                    
            else:
                address1 = checkoutform.cleaned_data['shipping_address1']
                address2 = checkoutform.cleaned_data['shipping_address2']
                pincode = checkoutform.cleaned_data['shipping_pincode']
                country = checkoutform.cleaned_data['shipping_country']
                set_default_shipping_address = checkoutform.cleaned_data['set_default_shipping_address']
                if set_default_shipping_address:
                        default = True
                        if Address.objects.filter(user=user,address_type='S',default=True).exists():
                            shipping_address = Address.objects.get(user=user,address_type='S',default=True)
                            shipping_address.default=False
                            shipping_address.save()

                else:
                    default= False

                if address1 and address2 and pincode and country:
                    shipping_address = Address.objects.create(
                                user = user,
                                street_address = address1,
                                apartment_address = address2,
                                country = country,
                                pincode = pincode,
                                address_type = 'S',
                                default = default
                            )
                else:
                    return HttpResponse('Fill the data')
                
            use_default_billing_address = checkoutform.cleaned_data['use_default_billing_address']
            same_billing_address = checkoutform.cleaned_data['same_billing_address']
            if same_billing_address and use_default_shipping_address :
                set_default_billing_address = checkoutform.cleaned_data['set_default_billing_address']
                if set_default_billing_address:
                    default = True
                    if Address.objects.filter(user=user,address_type='B',default=True).exists():
                        billing_address = Address.objects.get(user=user,address_type='B',default=True)
                        billing_address.default=False 
                        billing_address.save()
                else:
                    default= False
                billing_address = Address.objects.create(
                    user = user,
                    street_address = shipping_address.street_address,
                    apartment_address = shipping_address.apartment_address,
                    country = shipping_address.country,
                    pincode = shipping_address.pincode,
                    address_type = 'B',
                    default = default
                )

            elif same_billing_address:
                billing_address = Address.objects.create(
                    user = user,
                    street_address = address1,
                    apartment_address = address2,
                    country = country,
                    pincode = pincode,
                    address_type = 'B',
                    default = default
                )
            
            elif use_default_billing_address and Address.objects.filter(user=user,address_type='B',default=True).exists():
                    billing_address = Address.objects.get(user=user,address_type='B',default=True)
            else:
                address1 = checkoutform.cleaned_data['billing_address1']
                address2 = checkoutform.cleaned_data['billing_address2']
                pincode = checkoutform.cleaned_data['billing_pincode']
                country = checkoutform.cleaned_data['billing_country']
                set_default_billing_address = checkoutform.cleaned_data['set_default_billing_address']
                if set_default_billing_address:
                    default = True
                    if Address.objects.filter(user=user,address_type='B',default=True).exists():
                        billing_address = Address.objects.get(user=user,address_type='B',default=True)
                        billing_address.default=False 
                        billing_address.save()
                else:
                    default= False
                if address1 and address2 and pincode and country:
                    billing_address = Address.objects.create(
                    user = user,
                    street_address = address1,
                    apartment_address = address2,
                    country = country,
                    pincode = pincode,
                    address_type = 'B',
                    default = default
                    )
                else:
                    return HttpResponse('Fill the data')
            
                           
            
            cartitems = OrderItem.objects.filter(user_id=user,ordered=False)
            for item in cartitems:
                order =Order.objects.create(
                   user = user,
                   items = item,
                   billing_address= billing_address,
                   shipping_address = shipping_address,
                   ordered_date =  datetime.now()
                )
            return redirect('payment')
        
    return render(request, 'checkout.html',context)

import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def paymentview(request):
    context={
        'stripe_public_key':settings.STRIPE_TEST_PUBLIC_KEY
    }
    if request.method =='POST':
        try:
            charge=stripe.Charge.create(
                amount=1000,
                currency='inr',
                description ='charge discription',
                source=request.POST['stripeToken']
            )
            user=UserModel.objects.get(username=request.user)
            payment=Payment.objects.create(stripe_charge_id=change['id'],
                    user=user,amount=1000)
            return render(request,'paymentsuccess.html')
        except stripe.error.StripeError:
            return render(request,'error.html')
            
        return render(request,'payment.html',context)

def headerview(request):
    return render(request,'base.html')