from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Order
import logging
from datetime import datetime
import random
import string

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
        logger.debug(f"POST data: {request.POST}")
        logger.debug(f"FILES data: {request.FILES}")

        order = Order(
            quantity=int(request.POST['quantity']),
            first_name=request.POST['first_name'],
            middle_name=request.POST['middle_name'],
            last_name=request.POST['last_name'],
            date_of_birth=request.POST['date_of_birth'],
            state=request.POST['state'],
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
            additional=request.POST['additional'],
            tracking_number=generate_tracking_number()
        )
        order.save()
        request.session['order_id'] = order.id
        return render(request, 'mainapp/checkout.html', {'order': order})
    except Exception as e:
        logger.error(f"Error in checkout: {str(e)}", exc_info=True)
        return render(request, 'mainapp/error.html', {'error_message': f'An error occurred during checkout. Please try again. Error: {str(e)}'})

@require_POST
def payment(request):
    return render(request, 'mainapp/payment.html')

def generate_tracking_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

@require_POST
def confirmed(request):
    order_id = request.session.get('order_id')
    if order_id:
        order = Order.objects.get(id=order_id)
        order.tracking_number = generate_tracking_number()
        order.save()
        return render(request, 'mainapp/confirmed.html', {'order': order})
    return redirect('index')

def track(request):
    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number')
        try:
            order = Order.objects.get(tracking_number=tracking_number)
            return render(request, 'mainapp/track.html', {'order': order})
        except Order.DoesNotExist:
            return render(request, 'mainapp/track.html', {'error': 'Invalid tracking number'})
    return render(request, 'mainapp/track.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group, GroupMember

def grouporder(request):
    return render(request, 'mainapp/grouporder.html')

@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        group = Group.objects.create(creator=request.user)
        GroupMember.objects.create(group=group, user=request.user, name=name)
        return redirect('group', group_id=group.id)
    return render(request, 'mainapp/create_group.html')

@login_required
def join_group(request):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=request.POST['group_id'])
        if not GroupMember.objects.filter(group=group, name=request.POST['user_name']).exists():
            GroupMember.objects.create(group=group, user=request.user, name=request.POST['user_name'])
            return redirect('group', group_id=group.id)
        else:
            return render(request, 'mainapp/grouporder.html', {'error': 'Name already taken in this group'})
    return redirect('grouporder')

@login_required
def group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    user_member = group.members.get(user=request.user)
    return render(request, 'mainapp/group.html', {'group': group, 'user': user_member})

@login_required
def change_name(request, group_id, member_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        member = get_object_or_404(GroupMember, id=member_id, group=group)
        new_name = request.POST['new_name']
        if not GroupMember.objects.filter(group=group, name=new_name).exists():
            member.name = new_name
            member.save()
    return redirect('group', group_id=group_id)

@login_required
def kick_member(request, group_id, member_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id, creator=request.user)
        member = get_object_or_404(GroupMember, id=member_id, group=group)
        if member.user != group.creator:
            member.delete()
    return redirect('group', group_id=group_id)

@login_required
def leave_group(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        member = get_object_or_404(GroupMember, group=group, user=request.user)
        if member.user != group.creator:
            member.delete()
        else:
            # If the creator leaves, delete the entire group
            group.delete()
        return redirect('grouporder')
    return redirect('group', group_id=group_id)

def my_group(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        try:
            member = GroupMember.objects.get(member_id=member_id)
            return redirect('group', group_id=member.group.id)
        except GroupMember.DoesNotExist:
            return render(request, 'mainapp/grouporder.html', {'error': 'Invalid Member ID'})
    return redirect('grouporder')
