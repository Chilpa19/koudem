from django.db import models
from django.conf import settings


# Create your models hee.


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(null=False,blank=False,default='Pending')
    total_price=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
    @staticmethod
    def calculateTotal(order,courses_ids):

        orderItems=OrderDetail.objects.filter(order=order,course_id__in=courses_ids)

        return sum(orderItem.price_unitary for orderItem in orderItems)
    

    

class OrderDetail(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    course=models.ForeignKey('course.Course', on_delete=models.CASCADE)
    price_unitary= models.DecimalField(max_digits=10,decimal_places=2,default=0.0)


    def __str__(self):
        return f" Order detail {self.course.name} -${self.price_unitary}"

class CarItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    course=models.ForeignKey('course.Course', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)



class WebhookEvent(models.Model):
    stripe_id = models.CharField(max_length=255, unique=True)
    payload = models.JSONField()  # guarda todo el evento
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stripe Event {self.stripe_id}"