# app/management/commands/actualizar_inscripciones.py

from django.core.management.base import BaseCommand

from course.models import Inscription,Course
from django.utils import timezone

class Command(BaseCommand):
    help = "Actualiza las inscripciones cuando el curso ya comenzó"

    def handle(self, *args, **kwargs):
        ahora = timezone.now()

        cursos = Course.objects.filter(start_time__lte=ahora)

        actualizadas = Inscription.objects.filter(
            course__in=cursos,
            status="paid"
        ).update(status="in_progress")

        self.stdout.write(self.style.SUCCESS(
            f"Inscripciones actualizadas: {actualizadas}"
        ))
