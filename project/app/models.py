from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#  ProductCategory model
class ProductCategory(models.Model):
    product_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_image = models.ImageField(upload_to='category_images/')
    category_description = models.TextField()
    
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.category_name

    def save(self,*args,**kwargs):
        self.slug = str(self.category_name).replace(' ','-')
        super().save(*args,**kwargs)



# SizeCategory model
class SizeCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

# Brand model
class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=255)
    brand_description = models.TextField()

    def __str__(self):
        return self.brand_name

# Product model
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    # model_height = models.FloatField()
    # model_wearing = models.CharField(max_length=255)
    care_instructions = models.TextField()
    about = models.TextField()
    slug = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.product_name
    
    def save(self,*args,**kwargs):
        self.slug = str(self.product_category) +'-'+str(self.product_id).replace(' ','-')
        super().save(*args,**kwargs)


    

# ProductImage model
class ProductImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    product_item = models.ForeignKey('ProductItem', on_delete=models.CASCADE)
    image_filename = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product_item}"




# Colour model
class Colour(models.Model):
    colour_id = models.AutoField(primary_key=True)
    colour_name = models.CharField(max_length=255)

    def __str__(self):
        return self.colour_name


# ProductItem model
class ProductItem(models.Model):
    product_item_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.CharField(max_length=100,null=True,blank=True)
    image1=models.ImageField(upload_to='product_images/',blank=True,null=True)
    image2=models.ImageField(upload_to='product_images/',blank=True,null=True)
    image3=models.ImageField(upload_to='product_images/',blank=True,null=True)
    image4=models.ImageField(upload_to='product_images/',blank=True,null=True)

    def __str__(self):
        return  str(self.product_item_id)
    
    def save(self,*args,**kwargs):
        self.slug = str(self.product.product_category) +'-'+str(self.product).replace(' ','-')
        super().save(*args,**kwargs)

# ProductVariation model
class ProductVariation(models.Model):
    variation_id = models.AutoField(primary_key=True)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    size_option = models.ForeignKey('SizeOption', on_delete=models.CASCADE)
    qty_in_stock = models.IntegerField()

    def __str__(self):
        return f"{self.product_item} - {self.size_option}"

# SizeOption model
class SizeOption(models.Model):
    size_id = models.AutoField(primary_key=True)
    size_name = models.CharField(max_length=255)
    sort_order = models.IntegerField()
    size_category_id = models.ForeignKey('SizeCategory',on_delete=models.CASCADE,null=True,blank=True)
    slug = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.size_name
    
    def save(self,*args,**kwargs):
        self.slug = (str(self.size_category_id) +'-'+self.size_name).replace(' ','-')
        super().save(*args,**kwargs)


# user Model

from django_countries.fields import CountryField

class UserModel(User):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username}"


class OrderItem(models.Model):
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE,null=True,blank=True)
    ordered = models.BooleanField(default=False)
    product_item = models.ForeignKey('ProductItem', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.ForeignKey('SizeOption', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.product_item)

    def get_productitem_price(self):
        return self.product_item.original_price * self.quentity
        
    def get_discounted_price(self):
        return self.product_item.sale_price * self.quentity

    def amount_saved(self):
        return self.get_productitem_price()-self.get_discounted_price()

    # def get_final_price(self):
    #     if self.product_item.sale_price:



add =[
    ['B','Billing'],['S','Shipping']
]

    
class Address(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_addresses',null=True,blank=True)  # changed 'address' to 'addresses'
    street_address = models.CharField(max_length=100, null=False)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100,null=False,blank=False)
    pincode = models.IntegerField(null=True,blank=True)
    address_type = models.CharField(max_length=1, choices=[('B', 'Billing'), ('S', 'Shipping')], null=False)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street_address}, {self.country}"

class Payment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    stripe_charge_id=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"Payment of ${self.amount} by {self.user.username if self.user else 'Guest'}"




class Order(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,null=True,blank=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ForeignKey(OrderItem,on_delete=models.CASCADE, blank=True,null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=False)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='shipping_address')
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='billing_address')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)  # Added null=True here
    being_delivered = models.BooleanField(default=False)  
    received = models.BooleanField(default=False)  
    refund_requested = models.BooleanField(default=False)  
    refund_granted = models.BooleanField(default=False) 

    def __str__(self):
        return f"Order {self.id} by {self.user.username} ({'Completed' if self.ordered else 'Pending'})"