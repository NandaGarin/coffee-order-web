from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views import View
from .models import Product, Customer, Cart, WishList
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe


def home(request):
    totalitem = 0
    wishitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    return render(request, "app/home.html", locals())


def about(request):
    totalitem = 0
    wishitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    return render(request, "app/about.html",locals())


def contact(request):
    totalitem = 0
    wishitem =0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    return render(request, "app/contact.html",locals())


def login(request): 
    return render(request, "app/login.html")




class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values("title")
        return render(request, "app/category.html", locals())


class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values("title")
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, "app/category.html", locals())


class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = WishList.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, "app/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, "app/customerregistration.html", locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Registered Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "app/customerregistration.html", locals())




class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, "app/profile.html", locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            mobile = form.cleaned_data["mobile"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]

            reg = Customer(
                user=user,
                name=name,
                locality=locality,
                city=city,
                mobile=mobile,
                state=state,
                zipcode=zipcode,
            )
            reg.save()
            messages.success(request, "Congratulations! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "app/profile.html", locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/address.html", locals())


class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, "app/updateAddress.html", locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data["name"]
            add.locality = form.cleaned_data["locality"]
            add.city = form.cleaned_data["city"]
            add.mobile = form.cleaned_data["mobile"]
            add.state = form.cleaned_data["state"]
            add.zipcode = form.cleaned_data["zipcode"]
            add.save()
            messages.success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    if not product_id:
        return HttpResponseBadRequest("Product ID is missing or invalid.")

    try:
        product_id = int(product_id)
    except ValueError:
        return HttpResponseBadRequest("Product ID is not a valid number.")
    
    product = get_object_or_404(Product, id=product_id)
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/addtocart.html", locals())


def add_to_wishlist(request):
    user = request.user
    product_id = request.GET.get("wish_id")
    product = get_object_or_404(Product, id=product_id)
    WishList(user=user, product=product).save()
    return redirect("/list")


def show_wishlist(request):
    user = request.user
    wishlist = WishList.objects.filter(user=user)
    amount = 0
    for p in wishlist:
        value = p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(WishList.objects.filter(user=request.user))
    return render(request, "app/wishlist.html", locals())

def remove_from_wishlist(request):
    product_id = request.GET.get('prod_id')
    print(f"Product ID received: {product_id}")  # Debugging statement
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        wishlist = WishList.objects.filter(user=request.user, product=product)
        if wishlist.exists():
            print("Wishlist item found, deleting...")  # Debugging statement
            wishlist.delete()
        return redirect('/list')
    else:
        # Handle the case where no product_id is provided
        print("No Product ID provided")  # Debugging statement
        return redirect('/list')


class checkout(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        return render(request, "app/checkout.html", locals())


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {"quantity": c.quantity, "amount": amount, "totalamount": totalamount}
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {"quantity": c.quantity, "amount": amount, "totalamount": totalamount}
        return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {"quantity": c.quantity, "amount": amount, "totalamount": totalamount}
        return JsonResponse(data)
    
def logout_view(request):
    logout(request)
    return redirect('login')

def plus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        product = Product.objects.get(id=prod_id)    
        product_detail_url = reverse('product-detail', args=[product.id])
        user = request.user
        WishList(user=user,product=product).save()
        data = {
            'message':"Wishlist Added Successfully"
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"] 
        product = Product.objects.get(id=prod_id)   
        product_detail_url = reverse('product-detail', args=[product.id])
        user = request.user
        WishList.objects.filter(user=user,product=product).delete()
        data ={
            'message':"Wishlist Remove Successfully"
        }
        return JsonResponse(data)
    
def search(request):
    query = request.GET['search']
    totaliem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    product = Product.objects.filter(title__icontains=query)
    return render(request, "app/search.html",locals())

def home(request):
    return render(request, 'app/home.html')


stripe.api_key = 'sk_test_51PFoRTJxLPcyjYS8OOJ2RLiGq2BnT3pAJSSEMB0giVi7bAFxnd9TxII8xy8B2RlaQ4Yp6NebpduRllospC8CMp6q00WFswqx0J'


def payment(request):
    checkout_session = stripe.checkout.Session.create(
            payment_method_types=[
                'card'
            ],
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1PGMlqJxLPcyjYS8cK0FReQF',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://lcocalhost:8000',
            cancel_url='http://lcocalhost:8000',
        )
    return redirect(checkout_session.url, code=303)



