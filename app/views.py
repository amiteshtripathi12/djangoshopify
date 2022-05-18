from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Product, Customer, Cart, OrderPlaced, Slider, Live_sale
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages


class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        slideimage = Slider.objects.all()
        offer_banner = Live_sale.objects.all()
        offer = Product.objects.all()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles,
                            'slideimage': slideimage, 'totalitem': totalitem,'offer_banner':offer_banner,'offer':offer})


'''
def home(request):
 return render(request, 'app/home.html',)
def product_detail(request):
 return render(request, 'app/productdetail.html')
'''


class ProductDetailView(View):
    def get(self, request, pk):
        global totalitem
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',
                      {'product': product, 'item_already_in_cart': item_already_in_cart})




@login_required()
def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart/')
    if not request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart/')
        # return render (request ,'app/addtocart.html')


def show_cart(request):
    global totalamount
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount,
                                                          'totalitem': totalitem, 'amount': amount})
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) &
                             Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) &
                             Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) &
                             Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            # totalamount = amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount + shipping_amount
            }
            return JsonResponse(data)

@login_required()
def buy_now(request, pk):
    global totalitem, product
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
    return render(request, 'app/buynow.html', {'totalitem': totalitem,'product':product})


def address(request):
    global totalitem
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', {'add': add, 'totalitem': totalitem})


def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':order_placed})

'''
def orders1(request):
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders1.html',{'order_placed':order_placed,'product':product,})
'''
class OrderView(View):
    def get(self, request):
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        user = request.userb
        add = Customer.objects.filter(user=user)
        return render(request, 'app/orders1.html', {'product': product, 'add': add})
    '''
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        #order_placed = OrderPlaced.objects.filter(user=request.user)
        '''

'''
def change_password(request):
 return render(request, 'app/changepassword.html')
'''


def mobile(request, data=None):
    global mobiles
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'APPLE' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/mobile.html', {'mobiles': mobiles, 'totalitem': totalitem})


def topwear(request, data=None):
    global topwears
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Lewis' or data == 'PeterEngland':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=300)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=400)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/topwear.html', {'topwears': topwears, 'totalitem': totalitem})


def bottomwear(request, data=None):
    global bottomwears
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'Lewis' or data == 'PeterEngland':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=300)
    elif data == 'above':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=400)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears, 'totalitem': totalitem})


def electronics(request):
    return render(request, 'app/electronics.html')


def laptop(request):
    return render(request, 'app/laptop.html')


'''
def login(request):
 return render(request, 'app/login.html')
def customerregistration(request):
 return render(request, 'app/customerregistration.html')
'''



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'User Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

@login_required()
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    #product_id = request.GET.get('prod_id')
    #product = Product.objects.get(id=product_id)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user ==
                    request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add':add,
                     'totalamount':totalamount, 'cart_items':cart_items})

@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        user = request.user
        add = Customer.objects.filter(user=user)
        #Cart(product=product).save()
       # global totalitem
        #product = Product.objects.filter(user=request.user)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            #item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/checkout1.html',
                      {'product': product,'add':add})
'''
def checkout1(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    #product_id = request.GET.get('prod_id')
    #product = Product.objects.get(id=product_id)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user ==
                    request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout1.html', {'add':add,
                     'totalamount':totalamount, 'cart_items':cart_items})
'''

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product,
                    quantity = c.quantity).save()
        c.delete()
    return redirect("orders")

def payment_done1(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product,
                    quantity = c.quantity).save()
        c.delete()
    return redirect("orders1")







@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'totalitem': totalitem})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city,
                           state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile updates Successfully')
        return render(request, 'app/profile.html', {'form': form})


def search(request):
    return render(request, 'app/search.html')
