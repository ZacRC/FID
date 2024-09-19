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
]
