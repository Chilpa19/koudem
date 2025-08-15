from models import Order,OrderDetail


class PaymentService:

    @staticmethod
    def create_order(user, course_list):
        order=Order.objects.create(user=user)

        for course in course_list:
            OrderDetail.objects.create(
                order=order,
                course=course,
                price=course.price
            )
