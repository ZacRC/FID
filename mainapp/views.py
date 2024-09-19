from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Order
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

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
        # Add this debugging code
        logger.debug(f"POST data: {request.POST}")
        logger.debug(f"FILES data: {request.FILES}")

        order = Order(
            product=request.POST['product'],
            quantity=int(request.POST['quantity']),  # Ensure this line is present
            first_name=request.POST['first_name'],
            middle_name=request.POST['middle_name'],
            last_name=request.POST['last_name'],
            date_of_birth=request.POST['date_of_birth'],
            state_country=request.POST['state_country'],
            height_feet=int(request.POST['height_feet']),
            height_inches=int(request.POST['height_inches']),
            weight=int(request.POST['weight']),
            eyes=request.POST['eyes'],
            hair=request.POST['hair'],
            gender=request.POST['gender'],
            address1=request.POST['address1'],
            address2=request.POST['address2'],
            city=request.POST['city'],
            zip_code=request.POST['zip'],
            picture=request.FILES['picture'],
            signature=request.FILES.get('signature'),
            additional=request.POST['additional']
        )
        order.save()
        request.session['order_id'] = order.id
        return render(request, 'mainapp/checkout.html', {'order': order})
    except Exception as e:
        logger.error(f"Error in checkout: {str(e)}", exc_info=True)
        # Add this line to see the full POST data in the error template
        return render(request, 'mainapp/error.html', {'error_message': f'An error occurred during checkout. Please try again. POST data: {request.POST}'})

@require_POST
def payment(request):
    return render(request, 'mainapp/payment.html')

@require_POST
def confirmed(request):
    return render(request, 'mainapp/confirmed.html')
