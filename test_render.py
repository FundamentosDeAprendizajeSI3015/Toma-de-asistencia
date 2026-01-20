
import os
import django
import sys

# Setup Django environment
sys.path.append('D:\\App toma asistencia')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asistencia_app.settings')
django.setup()

from attendance.models import Student, Competency, StudentCompetency
from django.test import Client
from django.test.utils import override_settings

def run_test():
    print("Iniciando prueba de renderizado HTML (Validación Final Reordered)...")
    
    # 1. Obtener estudiante
    student = Student.objects.first()
    
    # 2. Asegurar estado True en DB
    competency = Competency.objects.first()
    StudentCompetency.objects.update_or_create(
        student=student, competency=competency,
        defaults={'is_achieved': True}
    )

    # 3. Hacer GET
    with override_settings(ALLOWED_HOSTS=['testserver']):
        c = Client()
        response = c.get(f'/student/{student.id}/')
        
    print(f"Status Code: {response.status_code}")
    
    html = response.content.decode()
    
    # Buscamos ambos atributos independientemente
    target_id = f'data-competency-id="{competency.id}"'
    target_checked = 'checked'
    
    # Encontrar el bloque del checkbox específico
    idx = html.find(target_id)
    if idx == -1:
         print("❌ FALLO: ID no encontrado")
         return

    # Buscar alrededor (50 chars antes y después)
    snippet = html[idx-50:idx+50]
    
    if target_checked in snippet:
        print(f"✅ ÉXITO: Se encontró '{target_checked}' cerca del ID.")
        print(f"Snippet: {snippet}")
    else:
        print(f"❌ FALLO: No se encontró '{target_checked}' cerca del ID.")
        print(f"Snippet: {snippet}")

if __name__ == '__main__':
    run_test()
