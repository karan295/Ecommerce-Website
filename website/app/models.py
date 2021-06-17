from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

STATE_CHOICES=(
    ('Andaman & Nicobar Island','Andaman & Nicobar Island'),
)

class Customer(models.Model):
    #user=models.ForeignKey(User,null=True, blank=True,on_delete=models.CASCADE)
    user = models.OneToOneField(User,unique=True,null=True, blank=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    zipcode=models.IntegerField(null=True,blank=True)
    state=models.CharField(choices=STATE_CHOICES,max_length=50)
    device=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        if self.name:
            name=self.name
        else:
            name=self.device
            
        return str(self.id)

CATEGORY_CHOICES=(
    ('fashion','Fashionable Jewel'),
    ('Antique','Antique Jewel'),
    ('design','Designable Jewel'),
    ('daily','Daily Useable Jewel'),
)

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=100)
    product_image=models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)



class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.total_cost for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICE=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
   # customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.PositiveIntegerField(default=1,null=True,blank=True)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICE,default='pending')



    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
            
        return shipping
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 