import random
import json
from app.utils import cookieCart, cartData, guestOrder

from django.shortcuts import render,redirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages

from django.db.models import Q
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import math
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class ProductView(View):
    totalitem=0
    def get(self,request):
        fashions=Product.objects.filter(category='fashion')#from model
        Antiques=Product.objects.filter(category='Antique')
        designs=Product.objects.filter(category='design')
        dailys=Product.objects.filter(category='daily')
        
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        
        else:
            
            items=[]
            order={'get_cart_total':0 , 'get_cart_items':0}
            totalitem=order['get_cart_items']



        return render(request,'app/home.html',
        {'fashions':fashions,'Antiques':Antiques,'designs':designs,'dailys':dailys,'totalitem':totalitem}
        )

#def home(request):
# return render(request, 'app/home.html')

class ProductDetailView(View):
    def get(self,request,pk):
        totalitem=0
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))        
            
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

        else:
            try:
                cart=json.loads(request.COOKIES['cart'])
                print('22244111',cart)
            except:
                cart={}
            print('Cart:',cart)
            items=[]
            order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
            cartItems=order['get_cart_items']
        
            for i in cart:
                cartItems+=cart[i]["quantity"]
                product=Product.objects.get(id=i)
                total=(product.discounted_price * cart[i]["quantity"])
                order['get_cart_total']+=total
                order['get_cart_items']+=cart[i]["quantity"]
            
                item={
                   'product':{
                           'id':product.id,
                           'name':product.title,
                           'price':product.discounted_price,
                           'imageURL':product.product_image.url,
                            },
                
                    'quantity':cart[i]["quantity"],
                    'get_total':total
                     }
            #items.append(item)
            #totalitem=len(item)


            return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

#def product_detail(request):
# return render(request, 'app/productdetail.html')

#@login_required
def add_to_cart(request):
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))   
        user=request.user
        product_id=request.GET.get('prod_id')
        product=Product.objects.get(id=product_id)
        Cart(user=user,product=product).save()
        return redirect('/cart',{'totalitem':totalitem})
    
    else:
        print('adddddtotttoocarrrtttt')
        items=[]
        order={'get_cart_total':0 , 'get_cart_items':0}
        totalitem=order['get_cart_items']
        return redirect('/cart',{'totalitem':totalitem})



#@login_required
def show_cart(request):
    print('44441111111111')
    totalitem=0
    if request.user.is_authenticated:
       
        totalitem=len(Cart.objects.filter(user=request.user))  
        #order,created=Cart.objects.get_or_create(user=request.user) 
        print('44444333333333')
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        totalamount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        print('55555500000000')

        if cart_product:
            print('5555533333')
            for p in cart_product:
                print('55555555555')
                tempamount=(p.quantity * p.product.discounted_price)
                amount+=tempamount
                #totalamount=totalamount+ shipping_amount
                print('555555999999999')
            totalamount=amount+ shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart, 'totalamount':totalamount,'amount':amount,'totalitem':totalitem})

        else:
            print('666633333333')
            return render(request,'app/emptycart.html',{'totalitem':totalitem})
    else:

        '''
        device=request.COOKIES['device']
        print('11111')

       # customer=Customer.objects.get_or_create(device=device)
        customer=Customer.objects.get_or_create(device=device)
        #cart=Cart.objects.get_or_create(user=customer)
        password='1234567a'


        u=User.objects.create(username=u,first_name='guest', last_name='guest', email='guest@gmail.com', is_active=True, is_staff=True)
        u.save()
       # u = authenticate(username=u, password=password)


        print('customerrrr1116666',customer)
        #cart1=Cart.objects.get_or_create(user=customer)
        print('1111666666666')
        #User.objects.create_user(username=customer)
        c=User.objects.filter(username=customer)

        print('cc===',c)
        #orderplaced=OrderPlaced.objects.get_or_create(user=c)
        
       
        product_id = request.GET.get('product_id')

        cart=Cart.objects.create(user=u,product=product_id)
        print('13333322222222')
        totalitem=len(Cart.objects.filter(user=u))

       # Cart.quantity=request.POST.get('quantity',False)
       # print('cartquantiyyyy',Cart.quantity)
        print('1112222111')

        #Cart.Save()
        
        print('111224444')
       # cart=Cart.objects.filter(user=c)
        print('111888')
        amount=0.0
        shipping_amount=70.0
        totalamount=0.0
        print('11155555555555')
        cart_product=[p for p in Cart.objects.all() if p.user==u]
        print('cart+producctccccccccc',cart_product)
        print('55555500000000')

        if cart_product:
            print('5555533333')
            for p in cart_product:
                print('55555555555')
                tempamount=(p.quantity * p.product.discounted_price)
                amount+=tempamount
                #totalamount=totalamount+ shipping_amount
                print('555555999999999')
            totalamount=amount+ shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart, 'totalamount':totalamount,'amount':amount,'totalitem':totalitem})

        else:
            print('666633333333')
            return render(request,'app/emptycart.html',{'totalitem':totalitem})
        
        #return render(request,'app/emptycart.html')
        #return render(request,'app/emptycart.html',{'totalitem':totalitem})
        '''
        try:
            cart=json.loads(request.COOKIES['cart'])
            print('22244111',cart)
        except:
            cart={}
        print('Cart:',cart)
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
        
        for i in cart:
            cartItems+=cart[i]["quantity"]
            product=Product.objects.get(id=i)
            total=(product.discounted_price * cart[i]["quantity"])
            order['get_cart_total']+=total
            order['get_cart_items']+=cart[i]["quantity"]
            
            item={
                'product':{
                   'id':product.id,
                   'name':product.title,
                   'price':product.discounted_price,
                   'imageURL':product.product_image.url,
                    },
                
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)


        
        

        context={'items':items,'order':order,'cartItems':cartItems}

        return render(request,'app/cart.html',context)

    
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'app/store.html', context)
   



def plus_cart(request):
    print('66666661111111111')
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user)) 
        
    
    
    if not request.user.is_authenticated:
        try:
            cart=json.loads(request.COOKIES['cart'])
        except:
            cart={}
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
        
        for i in cart:
            cartItems+=cart[i]["quantity"]
            product=Product.objects.get(id=i)
            total=(product.discounted_price * cart[i]["quantity"])
            order['get_cart_total']+=total
            order['get_cart_items']+=cart[i]["quantity"]
            
            item={
                'product':{
                   'id':product.id,
                   'name':product.title,
                   'price':product.discounted_price,
                   'imageURL':product.product_image.url,
                    },
                
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)

        print('ooooooo',order['get_cart_items'])
        print('iiiiiiti',cartItems)
        print('iiitemmmm',items)
        
        totalitem=len(item)

        

        context={'items':items,'order':order,'cartItems':cartItems}


    


    if request.method=='GET':
        print('66666662222222222')
        prod_id=request.GET['prod_id']
        print('7722222222222222')
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        print('77777774444444')
        c.quantity =c.quantity +1
        print('qqqquantityyyyyyyyyyy',c.quantity) 
        print('777777777766666666')
        c.save()
        print('7777777777777')

        amount=0.0
        shipping_amount=70.0
        print('666666666666699999999999')
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]

        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
            print('7777777766666666666')

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
            }

    
        
        return JsonResponse(data)

def minus_cart(request):
    print('99999955555')
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))   


    if request.method=='GET':
        print('9999999999977777')
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity=c.quantity - 1
        c.save()

        amount=0.0
        shipping_amount=70.0
        print('1000000005555')
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        print('100000000000077777')

        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
            print('11111222222')

        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        
        return JsonResponse(data)


def remove_cart(request):
    print('1111111222333333333')
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user)) 



    if request.method=='GET':
        print('111111122222222255555555555')
        prod_id=request.GET['prod_id']
        c=Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))

        c.delete()

        amount=0.0
        shipping_amount=70.0
        print('133333333333333')
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]

        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
            print('13333333999')

        data={
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        
        return JsonResponse(data)



def buy_now(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user)) 

    else:
        try:
            cart=json.loads(request.COOKIES['cart'])
        except:
            cart={}
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
        
        for i in cart:
            cartItems+=cart[i]["quantity"]
            product=Product.objects.get(id=i)
            total=(product.discounted_price * cart[i]["quantity"])
            order['get_cart_total']+=total
            order['get_cart_items']+=cart[i]["quantity"]
            
            item={
                'product':{
                   'id':product.id,
                   'name':product.title,
                   'price':product.discounted_price,
                   'imageURL':product.product_image.url,
                    },
                
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)

        print('ooooooo',order['get_cart_items'])
        print('iiiiiiti',cartItems)
        print('iiitemmmm',items)
        
        totalitem=len(item)

    




    return render(request, 'app/buynow.html',{'totalitem':totalitem})


@login_required
def address(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user)) 


    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add,
    'active':'btn-primary','totalitem':totalitem})


#@login_required
def orders(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))   
    


    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})

#def change_password(request):
# return render(request, 'app/changepassword.html')




def mobile(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))   


    if data==None:
        mobiles=Product.objects.filter(category='fashion')
    elif data=='Redmi' or data=='samsung':
        mobiles=Product.objects.filter(category='fashion').filter(brand=data)

    elif data=='below':
        mobiles=Product.objects.filter(category='fashion').filter(discounted_price__lt=10000)
           
    elif data=='above':
        mobiles=Product.objects.filter(category='fashion').filter(discounted_price__gt=10000)
       
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def laptop(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))  


    if data==None:
        laptops=Product.objects.filter(category='design')
    elif data=='Asus' or data=='Dell':
        laptops=Product.objects.filter(category='design').filter(brand=data)
    
    elif data=='above':
        laptops=Product.objects.filter(category='design').filter(discounted_price__gt=10000)

    elif data=='below':
        laptops=Product.objects.filter(category='above').filter(discounted_price__lt=10000) 

    return render(request, 'app/laptop.html',{'laptops':laptops,'totalitem':totalitem})


def top_wear(request,data=None):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user)) 



    if data==None:
        top_wears=Product.objects.filter(category='daily')
    elif data=='top_wear1' or data=='top_wear2':
        top_wears=Product.objects.filter(category='daily').filter(brand=data)

    elif data=='above':
        top_wears=Product.objects.filter(category='daily').filter(discounted_price__gt=1000)
    
    elif data=='below':
        top_wears=Product.objects.filter(category='daily').filter(discounted_price__lt=1000)
    
    return render(request, 'app/top.html',{'top_wears':top_wears,'totalitem':totalitem})


def bottom_wear(request,data=None):
    totalitem=0
  

    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user)) 



    if data==None:
        bottom_wears=Product.objects.filter(category='Antique')

    elif data=='bottom_wear1' or data=='bottom_wear2':
        bottom_wears=Product.objects.filter(category='Antique').filter(brand=data)

    elif data=='above':
        bottom_wears=Product.objects.filter(category='Antique').filter(discounted_price__gt=1000)
    
    elif data=='below':
        bottom_wears=Product.objects.filter(category='Antique').filter(discounted_price__lt=1000)
    
    return render(request, 'app/bottom.html',{'bottom_wears':bottom_wears,'totalitem':totalitem})


class CustomerRegistrationView(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user)) 


        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',
        {'form':form,'totalitem':totalitem})

    def post(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user)) 


    
        form=CustomerRegistrationForm(request.POST)

        if form.is_valid():
            messages.success(request,'congratulations!! Registered sucessfully')
            form.save()
        return render(request, 'app/customerregistration.html',
        {'form':form,'totalitem':totalitem})

#@login_required
def checkout(request):

    totalitem=0

    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user)) 
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        totalamount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discounted_price)
                
                amount+=tempamount
                totalamount=amount + shipping_amount
        return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})

    else:
        try:
            cart=json.loads(request.COOKIES['cart'])
        except:
            cart={}
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
        
        for i in cart:
            cartItems+=cart[i]["quantity"]
            product=Product.objects.get(id=i)
            totalamount=(product.discounted_price * cart[i]["quantity"])
            order['get_cart_total']+=totalamount
            order['get_cart_items']+=cart[i]["quantity"]
            
            item={
                'product':{
                   'id':product.id,
                   'name':product.title,
                   'price':product.discounted_price,
                   'imageURL':product.product_image.url,
                    },
                
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)

        print('ooooooo',order['get_cart_items'])
        print('iiiiiiti',cartItems)
        print('iiitemmmm',items)
        
        totalitem=len(item)
        return render(request, 'app/checkout.html',{'totalamount':totalamount,'cart_items':items,'totalitem':totalitem})


@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()

    return redirect("orders")

@method_decorator(login_required,name='dispatch')
class ProfileView(View):


    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user)) 
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,
        'active':'btn-primary','totalitem':totalitem,'totalitem':totalitem})


    def post(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user)) 

        form=CustomerProfileForm(request.POST)
                     

        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()

            messages.success(request,'congratulations !! Profile Updated Sucessfully')
            return render(request,'app/profile.html',{'form':form,'active':'btn-primary',
            'totalitem':totalitem
            })


def searchMatch(query, item):
    if query in item.category or query in item.title :
        print('33339777777777')
        return True
    else:
        return False

def search(request):
    query= request.GET.get('search')
    print('444440003333')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    print('44444006666666')
    cats = {item['category'] for item in catprods}
    print('4444000999')
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        print('441111222')
        prod=[item for item in prodtemp if searchMatch(query, item)]
        print('4444415555')
        n = len(prod)
        nSlides = n // 4 + math.ceil((n / 4) - (n // 4))
        print('4444418888888')
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
            print('44442222111')
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        print('444442224444')
        params={'msg':"Please make sure to enter relevant search query"}
        print('4444422266666')
    print('444427777777777')
    return render(request, 'app/search.html', params)