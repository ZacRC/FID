from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('pricing/', views.pricing, name='pricing'),
    path('faq/', views.faq, name='faq'),
    path('reviews/', views.reviews, name='reviews'),
    path('products/', views.products, name='products'),
    path('order/', views.order, name='order'),
    path('how-to-pay/', views.how_to_pay, name='how_to_pay'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('confirmed/', views.confirmed, name='confirmed'),
    path('track/', views.track, name='track'),
    path('grouporder/', views.grouporder, name='grouporder'),
    path('create-group/', views.create_group, name='create_group'),
    path('join-group/', views.join_group, name='join_group'),
    path('group/<int:group_id>/', views.group, name='group'),
    path('group/<int:group_id>/change-name/<int:member_id>/', views.change_name, name='change_name'),
    path('group/<int:group_id>/kick/<int:member_id>/', views.kick_member, name='kick_member'),
    path('group/<int:group_id>/leave/<int:member_id>/', views.leave_group, name='leave_group'),
    path('my-group/', views.my_group, name='my_group'),
    path('group/<int:group_id>/add-order-info/', views.add_group_order_info, name='add_group_order_info'),
    path('group/<int:group_id>/save-order-info/', views.save_group_order_info, name='save_group_order_info'),
    path('group/<int:group_id>/edit-order-info/', views.edit_group_order_info, name='edit_group_order_info'),
    path('group/<int:group_id>/order/', views.group_id_order, name='group_id_order'),
    path('group/<int:group_id>/confirm-payment/', views.confirm_group_payment, name='confirm_group_payment'),
    path('group/<int:group_id>/purchase-order/', views.purchase_group_order, name='purchase_group_order'),
    path('group/<int:group_id>/confirm-purchase/', views.confirm_group_purchase, name='confirm_group_purchase'),
]