from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Order, Group, GroupMember, GroupMemberOrderInfo, VenmoPayment
import logging
from datetime import datetime
import random
import string
from django.contrib import messages
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Order, Group, GroupMember, GroupMemberOrderInfo, VenmoPayment, BitcoinPayment
from django.urls import reverse

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
    image_urls = [
        "https://i2.paste.pics/65db2880c52399b66d82ba50375ee59f.png?rand=YmxQNpMhLv",
        "https://i2.paste.pics/54db3917411403806505fd2190fcc4bf.png?rand=JkFKRcxgPG",
        "https://i2.paste.pics/af26abc2fabc133d45be1d87647fed8b.png?rand=1uexkE3Ml7",
        "https://i2.paste.pics/7dfa819c0ece2dab9fb444b5aec0f213.png?rand=UzrW5iV1ag",
        "https://i2.paste.pics/f11b7926a96fc1e471d4d1cfde1af695.png?rand=NE2rXaSmq4",
        "https://i2.paste.pics/375cb20c97a7e9057776e335977c12cc.png?rand=avJUq3eycG",
        "https://i2.paste.pics/930f751cc5a204792fbfc6a82b90ada1.png?rand=LXysZxA4iM",
        "https://i2.paste.pics/54cf77ab9b02a834e0496bb26867a902.png?rand=3u1A7kgKN6",
        "https://i2.paste.pics/642f6c3d4af74944387f9ca07a6516e0.png?rand=Tfd8oies9h",
        "https://i2.paste.pics/766da6059e88d5cdd7023550d0688443.png?rand=f0mxsq95ot",
        "https://i2.paste.pics/a7730b900f9eae3a94546d4da9cb5cfe.png?trs=c78d6c299eb295e412d652481d6bcfda99b00e18f6cbe0ad33c87c02fad8600f&rand=wFtCKduDEV",
        "https://i2.paste.pics/157240e193495821c8ad2b0a084ccda2.png?trs=c78d6c299eb295e412d652481d6bcfda99b00e18f6cbe0ad33c87c02fad8600f&rand=u7j2w9NSQE",
        "https://i2.paste.pics/b9666cf0d74a7a476b367f607dfd7157.png?trs=c78d6c299eb295e412d652481d6bcfda99b00e18f6cbe0ad33c87c02fad8600f&rand=Um1N3Gw0Pe",
        "https://i2.paste.pics/59f830f156ca44b163a8fa3345e1729d.png?trs=c78d6c299eb295e412d652481d6bcfda99b00e18f6cbe0ad33c87c02fad8600f&rand=HwZ5jdyugA",
        "https://i2.paste.pics/9faea0e6f3f9519c8d67f8fddbd96e1c.png?trs=c78d6c299eb295e412d652481d6bcfda99b00e18f6cbe0ad33c87c02fad8600f&rand=3uXShofdmJ",
        "https://i2.paste.pics/c879cdc34dce3f8a83db95c6a1fe3f97.png?trs=c78d6c299eb295e412d652481d6bcfda99b00e18f6cbe0ad33c87c02fad8600f&rand=HB8Pmy4S1b",
        "https://i2.paste.pics/af52ce72ed265558113b936096ac443b.png?trs=c78d6c299eb295e412d652481d6bcfda99b00e18f6cbe0ad33c87c02fad8600f&rand=gDN4Wf9r8a",
        "https://i2.paste.pics/75a1b0b4b842422e1cca2fd858a458fe.png?trs=c78d6c299eb295e412d652481d6bcfda99b00e18f6cbe0ad33c87c02fad8600f&rand=q0eLP15p43",
    ]
    return render(request, 'mainapp/products.html', {'image_urls': image_urls})

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
            quantity=request.POST['quantity'],
            first_name=request.POST['first_name'],
            middle_name=request.POST['middle_name'],
            last_name=request.POST['last_name'],
            date_of_birth=request.POST['date_of_birth'],
            state=request.POST['state'],
            height_feet=request.POST['height_feet'],
            height_inches=request.POST['height_inches'],
            weight=request.POST['weight'],
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
            shipping=request.POST['shipping'],
            shipping_name=request.POST['shipping_name'],
            shipping_email=request.POST['shipping_email'],
            shipping_address1=request.POST['shipping_address1'],
            shipping_address2=request.POST['shipping_address2'],
            shipping_city=request.POST['shipping_city'],
            shipping_state=request.POST['shipping_state'],
            shipping_zip=request.POST['shipping_zip'],
        )
        order.save()
        
        request.session['order_id'] = order.id
        return render(request, 'mainapp/checkout.html', {'order': order})
    except Exception as e:
        logger.error(f"Error in checkout view: {str(e)}")
        return render(request, 'mainapp/error.html', {'error_message': 'An error occurred during checkout. Please try again.'})

def payment(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('order')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'mainapp/payment.html', {'order': order})

def generate_tracking_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

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
        group_id = request.POST.get('group_id')
        name = request.POST.get('name')
        
        if not group_id or not name:
            messages.error(request, 'Invalid group ID or name.')
            return redirect('grouporder')

        group = get_object_or_404(Group, id=group_id)
        
        if group.members.count() >= 10:
            messages.error(request, 'This group is already full.')
            return redirect('group', group_id=group_id)

        # Check if the name is already taken in this group
        if GroupMember.objects.filter(group=group, name=name).exists():
            messages.error(request, 'This name is already taken in the group. Please choose a different name.')
            return redirect('group', group_id=group_id)

        member = GroupMember.objects.create(
            group=group,
            name=name,
            member_id=''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        )
        
        request.session['member_id'] = member.member_id
        messages.success(request, f'You have successfully joined the group as {name}.')
        return render(request, 'mainapp/group_joined.html', {'group': group, 'member': member})
    return redirect('grouporder')

def calculate_price_per_id(member_count):
    if member_count >= 25:
        return 40
    elif member_count >= 10:
        return 50
    elif member_count >= 5:
        return 70
    elif member_count >= 3:
        return 90
    elif member_count >= 2:
        return 100
    else:
        return 120

def group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    creator = GroupMember.objects.get(group=group, member_id=group.creator_member_id)
    members = GroupMember.objects.filter(group=group)
    
    # Check if the user is a member of the group
    is_member = False
    current_member = None
    if 'member_id' in request.session:
        current_member = GroupMember.objects.filter(group=group, member_id=request.session['member_id']).first()
        is_member = current_member is not None

    # Calculate price per ID based on member count
    member_count = group.members.count()
    price_per_id = calculate_price_per_id(member_count)

    # Calculate members needed for next price drop
    next_price_threshold = get_next_price_threshold(member_count)
    members_needed_for_next_price = next_price_threshold - member_count if next_price_threshold else 0

    context = {
        'group': group,
        'creator': creator,
        'members': members,
        'current_member': current_member,
        'is_member': is_member,
        'price_per_id': price_per_id,
        'members_needed_for_next_price': members_needed_for_next_price,
    }
    return render(request, 'mainapp/group.html', context)

def calculate_price_per_id(member_count):
    if member_count >= 20:
        return 45
    elif member_count >= 10:
        return 60
    elif member_count >= 5:
        return 70
    elif member_count >= 3:
        return 85
    elif member_count >= 2:
        return 100
    else:
        return 120

def get_next_price_threshold(member_count):
    if member_count < 2:
        return 2
    elif member_count < 3:
        return 3
    elif member_count < 5:
        return 5
    elif member_count < 10:
        return 10
    elif member_count < 20:
        return 20
    else:
        return None

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
        order_info.quantity = int(request.POST.get('quantity', 1))
        order_info.first_name = request.POST.get('first_name', '')
        order_info.middle_name = request.POST.get('middle_name', '')
        order_info.last_name = request.POST.get('last_name', '')
        order_info.date_of_birth = request.POST.get('date_of_birth', '')
        order_info.state = request.POST.get('state', '')
        order_info.height_feet = int(request.POST.get('height_feet') or 0)
        order_info.height_inches = int(request.POST.get('height_inches') or 0)
        order_info.weight = int(request.POST.get('weight') or 0)
        order_info.eyes = request.POST.get('eyes', '')
        order_info.hair = request.POST.get('hair', '')
        order_info.gender = request.POST.get('gender', '')
        order_info.address1 = request.POST.get('address1', '')
        order_info.address2 = request.POST.get('address2', '')
        order_info.city = request.POST.get('city', '')
        order_info.zip_code = request.POST.get('zip', '')
        order_info.shipping_name = request.POST.get('shipping_name', '')
        order_info.shipping_email = request.POST.get('shipping_email', '')
        order_info.shipping_address1 = request.POST.get('shipping_address1', '')
        order_info.shipping_address2 = request.POST.get('shipping_address2', '')
        order_info.shipping_city = request.POST.get('shipping_city', '')
        order_info.shipping_state = request.POST.get('shipping_state', '')
        order_info.shipping_zip_code = request.POST.get('shipping_zip', '')
        
        if 'picture' in request.FILES:
            order_info.picture = request.FILES['picture']
        if 'signature' in request.FILES:
            order_info.signature = request.FILES['signature']
        
        order_info.additional = request.POST.get('additional', '')
        
        try:
            order_info.save()
            current_member.order_info_completed = True
            current_member.save()
            messages.success(request, 'Order information saved successfully.')
        except Exception as e:
            messages.error(request, f'Error saving order information: {str(e)}')
        
        return redirect('group', group_id=group_id)

    return redirect('add_group_order_info', group_id=group_id)

def edit_group_order_info(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    current_member_id = request.session.get('member_id')
    current_member = GroupMember.objects.get(member_id=current_member_id, group=group)
    order_info = GroupMemberOrderInfo.objects.get(member=current_member)

    if request.method == 'POST':
        # Handle form submission (similar to save_group_order_info)
        # Update the existing order_info object
        # Redirect to group page after saving
        return redirect('group', group_id=group_id)

    return render(request, 'mainapp/grouporderinfo.html', {
        'group': group,
        'member': current_member,
        'order_info': order_info,
        'is_edit': True
    })

def group_id_order(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    current_member_id = request.session.get('member_id')
    current_member = GroupMember.objects.get(member_id=current_member_id, group=group)
    order_info = GroupMemberOrderInfo.objects.get(member=current_member)
    
    member_count = group.members.count()
    price_per_id = calculate_price_per_id(member_count)
    total_price = price_per_id * order_info.quantity

    return render(request, 'mainapp/groupidorder.html', {
        'group': group,
        'order_info': order_info,
        'price_per_id': price_per_id,
        'total_price': total_price,
    })

@require_POST
def confirm_group_payment(request, group_id):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        screenshot = request.FILES.get('screenshot')
        group = get_object_or_404(Group, id=group_id)
        current_member = get_object_or_404(GroupMember, group=group, member_id=request.session.get('member_id'))

        if screenshot:
            if payment_method == 'venmo':
                venmo_order_id = request.POST.get('order_id')
                VenmoPayment.objects.create(
                    group=group,
                    member=current_member,
                    order_id=venmo_order_id,
                    screenshot=screenshot
                )
            elif payment_method == 'bitcoin':
                BitcoinPayment.objects.create(
                    group=group,
                    member=current_member,
                    screenshot=screenshot
                )
            else:
                return JsonResponse({'success': False, 'error': 'Invalid payment method'})

            current_member.paid = True
            current_member.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No screenshot provided'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def purchase_group_order(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    current_member_id = request.session.get('member_id')
    current_member = GroupMember.objects.get(member_id=current_member_id, group=group)

    if current_member.member_id != group.creator_member_id:
        messages.error(request, "Only the group creator can purchase group orders.")
        return redirect('group', group_id=group_id)

    members_with_info = GroupMember.objects.filter(group=group, order_info_completed=True, paid=False)
    total_members = group.members.count()
    unpaid_members = members_with_info.count()

    total_quantity = sum(member.order_info.quantity for member in members_with_info)
    price_per_id = calculate_price_per_id(total_members)
    total_price = price_per_id * total_quantity

    context = {
        'group': group,
        'total_members': total_members,
        'members_with_info': members_with_info.count(),
        'unpaid_members': unpaid_members,
        'total_price': total_price,
    }

    return render(request, 'mainapp/purchasegrouporder.html', context)

@require_POST
def confirm_group_purchase(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    current_member_id = request.session.get('member_id')
    current_member = GroupMember.objects.get(member_id=current_member_id, group=group)

    payment_method = request.POST.get('payment_method')
    screenshot = request.FILES.get('screenshot')

    if screenshot:
        if payment_method == 'venmo':
            order_id = request.POST.get('order_id')
            VenmoPayment.objects.create(
                group=group,
                member=current_member,
                order_id=order_id,
                screenshot=screenshot
            )
        elif payment_method == 'bitcoin':
            BitcoinPayment.objects.create(
                group=group,
                member=current_member,
                screenshot=screenshot
            )
        else:
            return JsonResponse({'success': False, 'error': 'Invalid payment method'})

        # Mark all unpaid members as paid for group purchase
        unpaid_members = GroupMember.objects.filter(group=group, order_info_completed=True, paid=False)
        for member in unpaid_members:
            member.paid = True
            member.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No screenshot provided'})

import json
from django.http import JsonResponse

def confirm_venmo_payment(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        current_member_id = request.session.get('member_id')
        current_member = GroupMember.objects.get(member_id=current_member_id, group=group)

        order_id = request.POST.get('order_id')
        screenshot = request.FILES.get('screenshot')

        # Save the screenshot and update the payment status
        if screenshot:
            payment = VenmoPayment.objects.create(
                group=group,
                member=current_member,
                order_id=order_id,
                screenshot=screenshot
            )
            
            if current_member.member_id == group.creator_member_id:
                # Mark all unpaid members as paid for group purchase
                unpaid_members = GroupMember.objects.filter(group=group, order_info_completed=True, paid=False)
                for member in unpaid_members:
                    member.paid = True
                    member.save()
            else:
                # Mark only the current member as paid for individual purchase
                current_member.paid = True
                current_member.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No screenshot provided'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


from .models import Order, IndividualVenmoPayment, IndividualBitcoinPayment

def confirm_individual_payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        screenshot = request.FILES.get('screenshot')
        order = Order.objects.get(id=request.session.get('order_id'))

        if screenshot:
            if payment_method == 'venmo':
                venmo_order_id = request.POST.get('order_id')
                IndividualVenmoPayment.objects.create(
                    order=order,
                    venmo_order_id=venmo_order_id,
                    screenshot=screenshot
                )
            elif payment_method == 'bitcoin':
                IndividualBitcoinPayment.objects.create(
                    order=order,
                    screenshot=screenshot
                )
            else:
                return JsonResponse({'success': False, 'error': 'Invalid payment method'})

            order.paid = True
            order.save()
            return JsonResponse({'success': True, 'redirect_url': reverse('confirmed')})
        else:
            return JsonResponse({'success': False, 'error': 'No screenshot provided'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

