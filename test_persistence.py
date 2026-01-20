
import os
import django
import json
import sys

# Setup Django environment
sys.path.append('D:\\App toma asistencia')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asistencia_app.settings')
django.setup()

from attendance.models import Student, Competency, StudentCompetency
from django.test import RequestFactory
from attendance.views import save_student_competencies

def run_test():
    print("Iniciando prueba de persistencia...")
    
    # 1. Obtener o crear estudiante y competencia de prueba
    student = Student.objects.first()
    if not student:
        print("No hay estudiantes para probar.")
        return

    competency = Competency.objects.first()
    if not competency:
        print("No hay competencias para probar.")
        return

    print(f"Probando con Estudiante: {student.full_name} (ID: {student.id})")
    print(f"Competencia: {competency.name} (ID: {competency.id})")

    # 2. Asegurar estado inicial False
    StudentCompetency.objects.update_or_create(
        student=student, competency=competency,
        defaults={'is_achieved': False}
    )
    print("Estado inicial: False")

    # 3. Simular request AJAX para marcar como True
    factory = RequestFactory()
    data = {'competencies': {str(competency.id): True}}
    request = factory.post(
        f'/student/{student.id}/competencies/save/',
        data=json.dumps(data),
        content_type='application/json'
    )

    # 4. Ejecutar vista
    response = save_student_competencies(request, student_id=student.id)
    print(f"Respuesta vista: {response.status_code}")
    print(f"Content: {response.content.decode()}")

    # 5. Verificar persistencia en DB
    sc = StudentCompetency.objects.get(student=student, competency=competency)
    print(f"Estado en DB después de guardar: {sc.is_achieved}")

    if sc.is_achieved:
        print("✅ ÉXITO: El cambio se persistió correctamente.")
    else:
        print("❌ FALLO: El cambio NO se persistió en la DB.")

if __name__ == '__main__':
    run_test()
