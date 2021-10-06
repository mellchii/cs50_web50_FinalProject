from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
import string
import random

from .models import User, Product, Order, OrderItem, Checkout, Wishlist, Reviews, Supply


def index(request):
    product = Product.objects.all()
    pager = Paginator(product, 8)  # Show 8 products per page.
    page_number = request.GET.get('page', 1)
    page = pager.page(page_number)

    if request.user.is_authenticated:
        order, create = Order.objects.get_or_create(creator=request.user, status=False)
        items = OrderItem.objects.filter(order=order).all()
        if order.order_number is None:
            ref_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            order.order_number = ref_id
            order.save()
    else:
        items = []
        order = {'cart_total': 0, 'item_total': 0}
    return render(request, "mart/index.html", {
        "products": page,
        "items": items,
        "order": order
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mart/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mart/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mart/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "mart/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mart/register.html")

def cart(request):
    if request.user.is_authenticated:
        order, create = Order.objects.get_or_create(creator=request.user, status=False)
        items = OrderItem.objects.filter(order=order).all()
    else:
        items = []
        order = {'cart_total': 0, 'item_total': 0}
    return render(request, "mart/cart.html", {
        "items": items,
        "order": order,
    })


def product(request, Product_id):

    if request.user.is_authenticated:
        order, create = Order.objects.get_or_create(creator=request.user, status=False)
        items = OrderItem.objects.filter(order=order).all()
    else:
        items = []
        order = {'cart_total': 0, 'item_total': 0}

    ids = []
    if request.user.is_authenticated:
        wish = Wishlist.objects.filter(creator=request.user)
        for w in wish:
            ids.append(w.product.id)

    return render(request, "mart/product.html", {
        "product": Product.objects.get(pk=Product_id),
        "reviews": Reviews.objects.filter(product=Product_id).all(),
        "items": items,
        "order": order,
        "ids": ids,
    })

@csrf_exempt
def edit(request, Product_id):
    # Query for requested product
    try:
        product = Product.objects.get(pk=Product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, status=404)

    # Return product contents
    if request.method == "GET":
        return JsonResponse(product.serialize())

    # Update stock value
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("stock") is not None:
            product.stock = data["stock"]
        product.save()
        return JsonResponse(product.serialize())

    # Save new Supply entry
    elif request.method == "POST":
        data = json.loads(request.body)
        supply = Supply(
            product=product,
            quantity=data["quantity"],
        )
        supply.save()
        return HttpResponse(status=204)

    # Post must be via GET or PUT or POST
    else:
        return JsonResponse({
            "error": "GET or PUT or POST request required."
        }, status=400)

@csrf_exempt
def review(request, Product_id):

    # Query for requested product
    try:
        product = Product.objects.get(pk=Product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, status=404)

    # Write a new review via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # Get content of review
    data = json.loads(request.body)
    body = data.get("body", "")
    rating = data.get("rating")

    if body:

        # Check if a review by user on product exists, then update content
        if Reviews.objects.filter(creator=request.user, product=Product_id).exists():
            review = Reviews.objects.get(creator=request.user, product=Product_id)
            review.review = data["body"]
            review.save()

            return JsonResponse({"message": "Review updated successfully."}, status=201)

        else:
            # Create a review for the specified product by the specified user
            review = Reviews (
                creator=request.user,
                product=product,
                review=body,
            )
            review.save()

            return JsonResponse({"message": "Review created successfully."}, status=201)

    elif rating:

        # Check if a review by user on product exists, then update content
        if Reviews.objects.filter(creator=request.user, product=Product_id).exists():
            review = Reviews.objects.get(creator=request.user, product=Product_id)
            review.rating = data["rating"]
            review.save()

            return JsonResponse({"message": "Rating updated successfully."}, status=201)

        else:
            # Create a review for the specified product by the specified user
            review = Reviews(
                creator=request.user,
                product=product,
                rating=rating,
                review=body,
            )
            review.save()

            return JsonResponse({"message": "Rating created successfully."}, status=201)

    else:
        return JsonResponse({"message": "No update made on Review."}, status=201)

def all(request):
    products = Product.objects.all()
    if request.method == "GET":
        return JsonResponse([product.serialize() for product in products], safe=False)

def category(request, category):
    if request.user.is_authenticated:
        order, create = Order.objects.get_or_create(creator=request.user, status=False)
        items = OrderItem.objects.filter(order=order).all()
    else:
        items = []
        order = {'cart_total': 0, 'item_total': 0}

    ids = []
    if request.user.is_authenticated:
        wish = Wishlist.objects.filter(creator=request.user)
        for w in wish:
            ids.append(w.product.id)

    context = Product.objects.filter(category=category).all()
    return render(request, "mart/category.html", {
        "products": context,
        "category": context[0].get_category_display,
        "items": items,
        "order": order,
        "ids": ids,
    })

@login_required
def wishlist(request):
    if request.user.is_authenticated:
        order, create = Order.objects.get_or_create(creator=request.user, status=False)
        items = OrderItem.objects.filter(order=order).all()
    else:
        items = []
        order = {'cart_total': 0, 'item_total': 0}
    return render(request, "mart/wishlist.html", {
        "lists": Wishlist.objects.filter(creator=request.user).all(),
        "items": items,
        "order": order,
    })

@login_required
def checkout(request):

    if request.user.is_authenticated:
        order, create = Order.objects.get_or_create(creator=request.user, status=False)
        items = OrderItem.objects.filter(order=order).all()
    else:
        items = []
        order = {'cart_total': 0, 'item_total': 0}

    if request.method == "POST":
        address = request.POST["address"]
        city = request.POST["country"]
        state = request.POST["state"]

        # Save shipping address, complete order and redirect to home page
        checkout = Checkout(
            creator=request.user,
            order=order,
            address=address,
            city=city,
            state=state,
        )
        checkout.save()

        order.status = True
        order.ordered_date = datetime.now()
        order.save()

        for item in items:
            product = Product.objects.get(pk=item.product.id)
            product.stock -= item.quantity
            product.save()

        messages.success(request, "Order Placed Successfully")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mart/checkout.html", {
            "items": items,
            "order": order,
        })

@login_required
def stock(request):
    order_total = 0
    orders = Order.objects.filter(status=True)
    for order in orders:
        order_total += order.cart_total

    products = Product.objects.all()
    stock_total = 0
    for product in products:
        stock_total += (product.price * product.stock)

    order_item = OrderItem.objects.filter(order__status=True)

    return render(request, "mart/stock.html", {
        "products": Product.objects.all(),
        "stock_total": stock_total,
        "users": User.objects.all().count(),
        "incomplete": Order.objects.filter(status=False),
        "complete": orders,
        "order_total": order_total,
        "order_items": order_item,
        "supplys": Supply.objects.all(),
    })

@csrf_exempt
def wish(request, Product_id):

    # Query for requested product
    try:
        product = Product.objects.get(pk=Product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, status=404)

    # Save new Wishlist entry
    if request.method == "POST":
        if Wishlist.objects.filter(creator=request.user, product=Product_id).exists():
            wish = Wishlist.objects.filter(creator=request.user, product=Product_id)
            wish.delete()
        else:
            wish = Wishlist(
                creator=request.user,
                product=product,
            )
            wish.save()
        return HttpResponse(status=204)

    # Post must be via POST
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)

def search(request):

    if request.user.is_authenticated:
        order, create = Order.objects.get_or_create(creator=request.user, status=False)
        items = OrderItem.objects.filter(order=order).all()
    else:
        items = []
        order = {'cart_total': 0, 'item_total': 0}

    query = request.GET.get('q')

    if query:
        results = Product.objects.filter(Q(name__icontains=query) | Q(long_description__icontains=query))
    else:
        results = Product.objects.all()

    pager = Paginator(results, 8)  # Show 8 products per page.
    page_number = request.GET.get('page', 1)
    page = pager.page(page_number)

    return render(request, "mart/index.html", {
        "products": page,
        "items": items,
        "order": order,
        "query": query
    })

@csrf_exempt
def update_cart(request):

    # Get Product id
    data = json.loads(request.body)
    product_id = data.get("product")

    customer = request.user
    product = Product.objects.get(pk=product_id)
    quantity = data.get("quantity")

    act = data.get("action")

    if request.method == "POST":
        order, create = Order.objects.get_or_create(creator=customer, status=False)
        orderitem, create = OrderItem.objects.get_or_create(product=product, order=order)

        orderitem.quantity += int(quantity)

        orderitem.save()

        return JsonResponse("Product added successfully.", safe=False)

    elif request.method == "PUT":
        if act == 'remove':
            order = Order.objects.get(creator=customer, status=False)
            orderitem = OrderItem.objects.get(product=product, order=order)

            orderitem.delete()

            return JsonResponse("Product removed successfully.", safe=False)

        elif act == 'update':
            order = Order.objects.get(creator=customer, status=False)
            orderitem = OrderItem.objects.get(product=product, order=order)

            orderitem.quantity = data.get("value")

            orderitem.save()

            return JsonResponse("Product updated successfully.", safe=False)

def cart_count(request):

    # Query for requested Order
    try:
        order = Order.objects.get(creator=request.user, status=False)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(order.serialize())