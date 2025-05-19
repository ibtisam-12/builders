# ecommerce/views.py
from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, Cart, CartItem,Category
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .models import Product
def home(request):
    products = Product.objects.filter(is_active=True)  # Retrieve active products
    return render(request, 'ecommerce/home.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)  # Retrieve product by slug
    return render(request, 'ecommerce/product_detail.html', {'product': product})



def ecommerce_view(request, page_type=None, product_slug=None):
    """
    A unified view that handles:
    - Homepage
    - Product detail page
    - Add to cart
    - View cart
    - Checkout
    """
    # If the user is not logged in, redirect them to the login page (for non-authenticated pages)
    if not request.user.is_authenticated and page_type != 'login':
        return redirect('login')

    # Homepage: Display featured products
    if page_type == 'home' or page_type is None:
        products = Product.objects.filter(is_active=True)  # Get active products
        return render(request, 'ecommerce/home.html', {'products': products})

    # Product Detail Page
    if page_type == 'product_detail' and product_slug:
        product = get_object_or_404(Product, slug=product_slug)  # Get the product by slug
        return render(request, 'ecommerce/product_detail.html', {'product': product})

    # Add to Cart
    if page_type == 'add_to_cart' and product_slug:
        product = get_object_or_404(Product, slug=product_slug)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get or create the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Increase quantity if the item is already in the cart
        cart_item.quantity += 1
        cart_item.save()

        return redirect('view_cart')  # Redirect to the cart view

    # View Cart
    if page_type == 'view_cart':
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            return render(request, 'ecommerce/cart.html', {'cart': cart})
        else:
            return render(request, 'ecommerce/cart.html', {'message': 'Your cart is empty.'})

    # Checkout
    if page_type == 'checkout':
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            total_amount = cart.total  # Calculate total price
            return render(request, 'ecommerce/checkout.html', {'cart': cart, 'total_amount': total_amount})
        else:
            return render(request, 'ecommerce/checkout.html', {'message': 'Your cart is empty.'})

    # If no matching page_type found, show a 404 error
    return HttpResponse("Page not found", status=404)
from django.shortcuts import render
from .models import Product, Category

def equipment(request):
    # Get the 'Equipment' category
    category = Category.objects.get(name='Equipment')
    products = Product.objects.filter(category=category)
    return render(request, 'ecommerce/equipment.html', {'products': products})

def apparel(request):
    # Get the 'Apparel' category
    category = Category.objects.get(name='Apparel')
    products = Product.objects.filter(category=category)
    return render(request, 'ecommerce/apparel.html', {'products': products})

def supplements(request):
    # Get the 'Supplements' category
    category = Category.objects.get(name='Supplements')
    products = Product.objects.filter(category=category)
    return render(request, 'ecommerce/supplements.html', {'products': products})


def contact(request):
    if request.method == "POST":
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send an email (you can configure this in Django settings)
        try:
            send_mail(
                f'New message from {name}',  # Subject
                message,  # Message body
                email,  # From email
                [settings.DEFAULT_FROM_EMAIL],  # To email
                fail_silently=False,
            )
            return HttpResponse('<h3>Thank you for reaching out! We will get back to you soon.</h3>')
        except:
            return HttpResponse('<h3>Sorry, something went wrong. Please try again later.</h3>')

    return render(request, 'ecommerce/contact.html')
