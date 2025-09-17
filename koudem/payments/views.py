from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from course.models import Inscription,Course
from django.utils import timezone

from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

import urllib.parse
import json
from django.contrib.auth.models import User
from payments.models import CarItem,Order,OrderDetail, WebhookEvent
from user.models import CustomUser



# @login_required
# def CreateCheckoutSessionView(request, slug):
#     print("Checkout, sin tema")
  

#     #product = Course.objects.get(id=course_id)
#     course = get_object_or_404(Course, slug=slug)

#     YOUR_DOMAIN = f"{request.scheme}://{request.get_host()}"


#     # http or https
#     # 127.0.0.1:8000
#     # http://127.0.0.1:8000
    
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{
#             'price_data': {
#                 'currency': 'mxn',
#                 'product_data': {
#                     'name': course.name,
#                     'images': ["https://test-koudem.s3.us-east-2.amazonaws.com/Chivas.png"],                    
#                     'metadata': {
#                         'course_id': course,
#                     }
#                 },
#                 'unit_amount': int(course.cost*100),  
#             },
#             'quantity': 1,
#         }],
#         metadata = {
#             'course_id': course,
#             'user_email': request.user.email,
#         },
        
#         mode='payment',

#         success_url=YOUR_DOMAIN + f'/payment-success/{course}/',
#         cancel_url=YOUR_DOMAIN + f'/pricing/{course}/',
#     )

#     return redirect(checkout_session.url)

# views.py
import stripe
import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Configurar Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
WEBHOOK_SECRET="whsec_7a1dd39c365df49aa065fb289acdfe37f63a8f7b8bf7ea087fed9f20cb19b2de"


@login_required
def car_shop(request):
    """Vista principal del carrito de compras"""
    user = request.user
    car_items = CarItem.objects.filter(user=user)
    total_price = sum(float(i.course.cost) for i in car_items)
    
    context = {
        "in_car_users": car_items,
        "total_price": total_price,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, "./course/viewCarShop.html", context)

@csrf_exempt
def create_checkout_session(request, course_slug):
    if request.method == 'POST':
        try:
            course = get_object_or_404(Course, slug=course_slug)

            intent = stripe.PaymentIntent.create(
                amount=int(course.cost * 100),
                currency='usd',
                automatic_payment_methods={'enabled': True},
                metadata={
                    'course_id': course.id,
                    'course_slug': course.slug,
                    'user_id': request.user.id if request.user.is_authenticated else '',
                }
            )

            return JsonResponse({'clientSecret': intent.client_secret})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# def checkout_return(request, course_slug):
#     """Página de retorno después del pago"""
#     course = get_object_or_404(Course, slug=course_slug)
#     session_id = request.GET.get('session_id')
    
#     context = {
#         'course': course,
#         'session_id': session_id,
#         'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
#     }
    
#     if session_id:
#         try:
#             # Verificar el estado del pago
#             session = stripe.checkout.Session.retrieve(session_id)
#             context['session'] = session
#             context['payment_status'] = session.payment_status
            
#             if session.payment_status == 'paid':
#                 # Aquí puedes procesar el pago exitoso
#                 # Por ejemplo: enrollar al usuario, enviar email, etc.
#                 context['success'] = True
                
#         except Exception as e:
#             print(f"Error retrieving session: {e}")
#             context['error'] = 'Error verificando el pago'
    
#     return render(request, 'course/checkout_return.html', context)


# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, WEBHOOK_SECRET
#         )
#     except stripe.error.SignatureVerificationError:
#         return HttpResponse(status=400)

#     # Escuchar PaymentIntent completado
#     if event["type"] == "payment_intent.succeeded":
#         intent = event["data"]["object"]
#         course_id = intent.metadata.get("course_id")
#         user_id = intent.metadata.get("user_id")

#         try:
#             course = Course.objects.get(id=course_id)
#             user = User.objects.get(id=user_id)
#             Inscription.objects.get_or_create(
#                 alumno=user,
#                 course=course,
#                 defaults={"status": "Paid"}
#             )
#             print(f"✅ Inscripción creada: {user.username} en {course.name}")
#         except Exception as e:
#             print(f"❌ Error creando inscripción: {e}")

#     return HttpResponse(status=200)

# @login_required
# def check_enrollment(request, course_id):
#     user = request.user
#     enrolled = Inscription.objects.filter(alumno=user, course_id=course_id).exists()
#     return JsonResponse({"enrolled": enrolled})


def checkout_return(request, course_slug):
    """Página de retorno después del pago"""
    course = get_object_or_404(Course, slug=course_slug)
    context = {
        'course': course,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, "course/checkout_return.html", context)

@csrf_exempt
def stripe_webhook(request):
    """Webhook para procesar PaymentIntent completado"""
    print("Webhook")
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    print("Event",event["type"])
    if WebhookEvent.objects.filter(stripe_id=event["id"]).exists():
        print(f"⚠️ Evento duplicado ignorado: {event['id']}")
        return HttpResponse(status=200)

    WebhookEvent.objects.create(
        stripe_id=event["id"],
        payload=event
    )


    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        course_id = intent.metadata.get("course_id")
        user_id = intent.metadata.get("user_id")
        print("USER_ID",user_id)


        try:

            if event["type"] == "payment_intent.succeeded":
                intent = event["data"]["object"]
                course_id = intent.metadata.get("course_id")
                user_id = intent.metadata.get("user_id")
                print("USER_ID",user_id)

                course = Course.objects.get(id=course_id)
                user = CustomUser.objects.get(id=user_id) 

                orden=Order.objects.create(
                    user=user,
                    created_at=timezone.now(),
                    status='Paid'
                )

                orden_detail=OrderDetail.objects.create(
                    order=orden,
                    course=course,
                    price_unitary=200
                )

                Inscription.objects.get_or_create(

                    alumno=user,
                    order_detail=orden_detail,
                    course=course
                
                )
                print(f"✅ Inscripción creada: {user.username} en {course.name}")
        except Exception as e:
            print(f"❌ Error creando inscripción: {e}")

    return HttpResponse(status=200)

@login_required
def check_enrollment(request, course_id):
    """Verifica si el usuario ya está inscrito en el curso"""
    print("Enrooll")
    user = request.user
    enrolled = Inscription.objects.filter(alumno=user, course_id=course_id).exists()
    #enrolled = True
    return JsonResponse({"enrolled": enrolled})