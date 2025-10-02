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

from django.views.decorators.http import require_POST



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
    print("Carrito de compras view")
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
@login_required
def create_checkout_session(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    else:
        print("Checkout")
    

    try:
        print("Post check")
        data = json.loads(request.body)
        print("data",data)
        course_ids = data.get("course_ids", [])
        if not course_ids:
            return JsonResponse({"error": "No se recibieron cursos"}, status=400)

        # Obtener cursos
        courses = Course.objects.filter(id__in=course_ids)
        if not courses.exists():
            return JsonResponse({"error": "Cursos no encontrados"}, status=404)

        # Calcular monto total
        total_amount = int(sum(course.cost for course in courses) * 100)  # centavos

        # Crear PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=total_amount,
            currency="mxn",
            automatic_payment_methods={"enabled": True},
            metadata={
                "course_ids": ",".join(str(c.id) for c in courses),
                "user_id": request.user.id,
            }
        )

        return JsonResponse({"clientSecret": intent.client_secret})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def checkout_return(request):
    """Página de retorno después de pagar carrito completo"""
    # Traemos los cursos del carrito del usuario
    car_items = CarItem.objects.filter(user=request.user)

    courses = [item.course for item in car_items]
    course_ids = [item.course.id for item in car_items]  # <- IDs para JS

    print(courses)

    context = {
        "course":courses,
        "courses": courses,
        "total_price": sum(item.course.cost for item in car_items),
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
        "course_ids_json": json.dumps(course_ids),  # <- Pasamos como JSON seguro
    }



    return render(request, "course/checkout_return.html", context)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        user_id = intent.metadata.get("user_id")
        course_ids = intent.metadata.get("course_ids", "").split(",")

        try:
            #print("USER_ID",user_id)
            car_items = CarItem.objects.filter(user=user_id)
            #print("CAR obtenido con exito")
            user = CustomUser.objects.get(id=user_id)
            #print("DATOS OBTENIDOS")

            # Crear orden
            orden = Order.objects.create(
                user=user,
                created_at=timezone.now(),
                status="Paid"
            )
            print("ORDEN CREADA")

            for cid in course_ids:
                course = Course.objects.get(id=int(cid))

                order_detail = OrderDetail.objects.create(
                    order=orden,
                    course=course,
                    price_unitary=course.cost
                )


                Inscription.objects.get_or_create(
                        alumno=user,
                        order_detail=order_detail,
                        course=course,
                        status= "Paid"
                    )
                
            orden.total_price=Order.calculateTotal(orden,course_ids)
            orden.save()
            car_items.delete()

            print(f"✅ Orden {orden.id} creada para {user.username} con {len(course_ids)} cursos")


        except Exception as e:
            print(f"❌ Error creando inscripción múltiple: {e}")

    return HttpResponse(status=200)


@login_required
@csrf_exempt
def check_enrollment(request):
    """Verifica si el usuario está inscrito en todos o algunos de los cursos"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            course_ids = data.get("course_ids", [])
            
            user = request.user

            # Buscar cursos en los que el usuario ya está inscrito
            enrolled_courses = Inscription.objects.filter(
                alumno=user, course_id__in=course_ids
            ).values_list("course_id", flat=True)

            enrolled_courses_list = list(enrolled_courses)

            print( "Enrooled courses",enrolled_courses_list)

            return JsonResponse({
                "enrolled_courses": enrolled_courses_list,
                "all_enrolled": len(enrolled_courses_list) == len(course_ids)
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)