from celery import shared_task
from django.utils import timezone
from course.models import Inscription

@shared_task
def actualizar_inscripciones_en_progreso():
    print("Ejecutando tarea")
    ahora = timezone.now()

    inscripciones = Inscription.objects.filter(
        course__start_date__lte=ahora,
        status="Paid"
    )

    inscripciones.update(status="in_progress")

    return f"Actualizadas: {inscripciones.count()}"
