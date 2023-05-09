from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
    path('store/<int:pk>/', views.item, name='item'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('thanks/', views.thanks, name='thanks'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),
    path('get_cart_total/', views.get_guest_cart_total),
    path('<slug:url>/', views.text_page, name='text_page'),
]

