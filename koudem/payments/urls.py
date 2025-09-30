from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # Página del carrito
    path('cart/', views.car_shop, name='car_shop'),
    
    # API para crear sesión de checkout
    path('api/create-checkout-session/', 
         views.create_checkout_session, 
         name='create_checkout_session'),
    
    # Página de retorno después del pago
    path('checkout/return/', 
         views.checkout_return, 
         name='checkout_return'),
     
     path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),

     path('api/check-enrollment/', views.check_enrollment, name='check_enrollment'),


     
]