from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Order, Group, GroupMember, GroupMemberOrderInfo
import logging
from datetime import datetime
import random
import string
from django.contrib import messages

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

def grouporder(request):
    return render(request, 'mainapp/grouporder.html')

def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        member_id = generate_member_id()
        group = Group.objects.create(creator_member_id=member_id)
        member = GroupMember.objects.create(group=group, name=name, member_id=member_id)
        request.session['member_id'] = member_id
        return render(request, 'mainapp/group_created.html', {'group': group, 'member': member})
    return render(request, 'mainapp/create_group.html')

def join_group(request):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=request.POST['group_id'])
        name = request.POST['user_name']
        if not GroupMember.objects.filter(group=group, name=name).exists():
            member_id = generate_member_id()
            member = GroupMember.objects.create(group=group, name=name, member_id=member_id)
            request.session['member_id'] = member_id
            return render(request, 'mainapp/group_joined.html', {'group': group, 'member': member})
        else:
            return render(request, 'mainapp/grouporder.html', {'error': 'Name already taken in this group'})
    return redirect('grouporder')

def group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    creator = group.members.get(member_id=group.creator_member_id)
    current_member_id = request.session.get('member_id')
    current_member = GroupMember.objects.get(member_id=current_member_id, group=group)
    return render(request, 'mainapp/group.html', {
        'group': group,
        'creator': creator,
        'current_member': current_member
    })

def change_name(request, group_id, member_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        member = get_object_or_404(GroupMember, id=member_id, group=group)
        if request.POST.get('member_id') == group.creator_member_id:
            new_name = request.POST['new_name']
            if not GroupMember.objects.filter(group=group, name=new_name).exists():
                member.name = new_name
                member.save()
    return redirect('group', group_id=group_id)

def kick_member(request, group_id, member_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        member = get_object_or_404(GroupMember, id=member_id, group=group)
        if request.POST.get('member_id') == group.creator_member_id and member.member_id != group.creator_member_id:
            member.delete()
    return redirect('group', group_id=group_id)

def leave_group(request, group_id, member_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        member = get_object_or_404(GroupMember, id=member_id, group=group)
        if member.member_id == group.creator_member_id:
            group.delete()
            return redirect('grouporder')
        else:
            member.delete()
    return redirect('group', group_id=group_id)

def my_group(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        try:
            member = GroupMember.objects.get(member_id=member_id)
            request.session['member_id'] = member_id
            return redirect('group', group_id=member.group.id)
        except GroupMember.DoesNotExist:
            return render(request, 'mainapp/grouporder.html', {'error': 'Invalid Member ID'})
    return redirect('grouporder')

def generate_member_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def add_group_order_info(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    current_member_id = request.session.get('member_id')
    current_member = GroupMember.objects.get(member_id=current_member_id, group=group)
    
    try:
        order_info = current_member.order_info
    except GroupMemberOrderInfo.DoesNotExist:
        order_info = None

    return render(request, 'mainapp/grouporderinfo.html', {
        'group': group,
        'member': current_member,
        'order_info': order_info
    })

def save_group_order_info(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        current_member_id = request.session.get('member_id')
        current_member = GroupMember.objects.get(member_id=current_member_id, group=group)

        order_info, created = GroupMemberOrderInfo.objects.get_or_create(member=current_member)
        
        # Update order info fields
        order_info.quantity = request.POST.get('quantity')
        order_info.first_name = request.POST.get('first_name')
        order_info.middle_name = request.POST.get('middle_name')
        order_info.last_name = request.POST.get('last_name')
        order_info.date_of_birth = request.POST.get('date_of_birth')
        order_info.state = request.POST.get('state')
        order_info.height_feet = request.POST.get('height_feet')
        order_info.height_inches = request.POST.get('height_inches')
        order_info.weight = request.POST.get('weight')
        order_info.eyes = request.POST.get('eyes')
        order_info.hair = request.POST.get('hair')
        order_info.gender = request.POST.get('gender')
        order_info.address1 = request.POST.get('address1')
        order_info.address2 = request.POST.get('address2')
        order_info.city = request.POST.get('city')
        order_info.zip_code = request.POST.get('zip')
        
        if 'picture' in request.FILES:
            order_info.picture = request.FILES['picture']
        if 'signature' in request.FILES:
            order_info.signature = request.FILES['signature']
        
        order_info.additional = request.POST.get('additional')
        order_info.save()

        current_member.order_info_completed = True
        current_member.save()

        messages.success(request, 'Order information saved successfully.')
        return redirect('group', group_id=group_id)

    return redirect('add_group_order_info', group_id=group_id)