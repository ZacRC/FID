from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Order

# Create your views here.

def index(request):
    return render(request, 'mainapp/index.html')

def about(request):
    return render(request, 'mainapp/about.html')

def pricing(request):
    return render(request, 'mainapp/pricing.html')

def faq(request):
    return render(request, 'mainapp/faq.html')

def reviews(request):
    return render(request, 'mainapp/reviews.html')

def products(request):
    return render(request, 'mainapp/products.html')

def order(request):
    return render(request, 'mainapp/order.html')

def how_to_pay(request):
    return render(request, 'mainapp/howtopay.html')

@require_POST
def checkout(request):
    try:
        order = Order(
            product=request.POST['product'],
            quantity=request.POST['quantity'],
            first_name=request.POST['first_name'],
            middle_name=request.POST['middle_name'],
            last_name=request.POST['last_name'],
            state=request.POST['state'],
            address=request.POST['address'],
            id_photo=request.FILES['id_photo'],
            id_signature=request.FILES['id_signature']
        )
        order.save()
        request.session['order_id'] = order.id
        return render(request, 'mainapp/checkout.html', {'order': order})
    except Exception as e:
        # Log the error and return an error response
        print(f"Error in checkout: {str(e)}")
        return render(request, 'mainapp/error.html', {'error_message': 'An error occurred during checkout. Please try again.'})

@require_POST
def payment(request):
    return render(request, 'mainapp/payment.html')

@require_POST
def confirmed(request):
    return render(request, 'mainapp/confirmed.html')
