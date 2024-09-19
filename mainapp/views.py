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
        # ... other fields ...
        date_of_birth = request.POST['date_of_birth']
        # Validate date format
        try:
            datetime.strptime(date_of_birth, '%m/%d/%Y')
        except ValueError:
            raise ValueError("Invalid date format. Please use MM/DD/YYYY.")
        
        order = Order(
            # ... other fields ...
            date_of_birth=date_of_birth,
            # ... rest of the fields ...
        )
        order.save()
        request.session['order_id'] = order.id
        return render(request, 'mainapp/checkout.html', {'order': order})
    except Exception as e:
        logger.error(f"Error in checkout: {str(e)}", exc_info=True)
        return render(request, 'mainapp/error.html', {'error_message': 'An error occurred during checkout. Please try again.'})

@require_POST
def payment(request):
    return render(request, 'mainapp/payment.html')

@require_POST
def confirmed(request):
    return render(request, 'mainapp/confirmed.html')
