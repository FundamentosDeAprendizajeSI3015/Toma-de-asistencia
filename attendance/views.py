import json
from datetime import date

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Student, AttendanceSession, AttendanceRecord, Competency, StudentCompetency


def index(request):
    """Vista principal: muestra el listado de estudiantes para tomar asistencia del día."""
    today = date.today()
    students = Student.objects.filter(is_active=True)
    
    # Obtener o crear la sesión del día
    session, created = AttendanceSession.objects.get_or_create(
        date=today,
        defaults={'description': f'Clase del {today.strftime("%d/%m/%Y")}'}
    )
    
    # Obtener registros existentes para hoy
    existing_records = {
        record.student_id: record.is_present 
        for record in session.records.all()
    }
    
    # Preparar datos de estudiantes con su estado de asistencia
    students_data = []
    for student in students:
        students_data.append({
            'student': student,
            'is_present': existing_records.get(student.id, False)
        })
    
    context = {
        'students_data': students_data,
        'session': session,
        'today': today,
        'total_students': len(students_data),
        'present_count': sum(1 for s in students_data if s['is_present']),
        'absent_count': sum(1 for s in students_data if not s['is_present']),
    }
    return render(request, 'attendance/index.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def save_attendance(request):
    """API endpoint para guardar la asistencia via AJAX."""
    try:
        data = json.loads(request.body)
        today = date.today()
        
        # Obtener o crear la sesión del día
        session, _ = AttendanceSession.objects.get_or_create(
            date=today,
            defaults={'description': f'Clase del {today.strftime("%d/%m/%Y")}'}
        )
        
        attendance_data = data.get('attendance', {})
        
        for student_id, is_present in attendance_data.items():
            student = get_object_or_404(Student, id=int(student_id))
            AttendanceRecord.objects.update_or_create(
                student=student,
                session=session,
                defaults={'is_present': is_present}
            )
        
        # Calcular estadísticas actualizadas
        present_count = session.records.filter(is_present=True).count()
        absent_count = session.records.filter(is_present=False).count()
        
        return JsonResponse({
            'success': True,
            'message': 'Asistencia guardada correctamente',
            'present_count': present_count,
            'absent_count': absent_count,
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def history(request):
    """Vista para mostrar el historial de sesiones de asistencia."""
    sessions = AttendanceSession.objects.all().prefetch_related('records', 'records__student')
    
    sessions_data = []
    for session in sessions:
        total = session.records.count()
        present = session.present_count
        sessions_data.append({
            'session': session,
            'total': total,
            'present': present,
            'absent': session.absent_count,
            'percentage': round((present / total * 100) if total > 0 else 0, 1)
        })
    
    return render(request, 'attendance/history.html', {'sessions_data': sessions_data})


def session_detail(request, session_id):
    """Vista para ver el detalle de una sesión específica."""
    session = get_object_or_404(AttendanceSession, id=session_id)
    records = session.records.select_related('student').order_by('student__last_name', 'student__first_name')
    today = date.today()
    
    # Solo se puede editar si la sesión es del día actual
    can_edit = session.date == today
    
    context = {
        'session': session,
        'records': records,
        'present_count': session.present_count,
        'absent_count': session.absent_count,
        'can_edit': can_edit,
    }
    return render(request, 'attendance/session_detail.html', context)


def edit_session(request, session_id):
    """Vista para editar la asistencia de una sesión (solo si es del día actual)."""
    session = get_object_or_404(AttendanceSession, id=session_id)
    today = date.today()
    
    # Verificar que la sesión sea del día actual
    if session.date != today:
        return render(request, 'attendance/session_detail.html', {
            'session': session,
            'records': session.records.select_related('student'),
            'present_count': session.present_count,
            'absent_count': session.absent_count,
            'can_edit': False,
            'error': 'Solo puedes editar sesiones del día actual.'
        })
    
    students = Student.objects.filter(is_active=True)
    
    # Obtener registros existentes para esta sesión
    existing_records = {
        record.student_id: record.is_present 
        for record in session.records.all()
    }
    
    # Preparar datos de estudiantes con su estado de asistencia
    students_data = []
    for student in students:
        students_data.append({
            'student': student,
            'is_present': existing_records.get(student.id, False)
        })
    
    context = {
        'students_data': students_data,
        'session': session,
        'today': today,
        'total_students': len(students_data),
        'present_count': sum(1 for s in students_data if s['is_present']),
        'absent_count': sum(1 for s in students_data if not s['is_present']),
        'is_edit_mode': True,
    }
    return render(request, 'attendance/edit_session.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def save_session_attendance(request, session_id):
    """API endpoint para guardar la asistencia de una sesión específica via AJAX."""
    try:
        session = get_object_or_404(AttendanceSession, id=session_id)
        today = date.today()
        
        # Verificar que la sesión sea del día actual
        if session.date != today:
            return JsonResponse({
                'success': False, 
                'error': 'Solo puedes editar sesiones del día actual.'
            }, status=403)
        
        data = json.loads(request.body)
        attendance_data = data.get('attendance', {})
        
        for student_id, is_present in attendance_data.items():
            student = get_object_or_404(Student, id=int(student_id))
            AttendanceRecord.objects.update_or_create(
                student=student,
                session=session,
                defaults={'is_present': is_present}
            )
        
        # Calcular estadísticas actualizadas
        present_count = session.records.filter(is_present=True).count()
        absent_count = session.records.filter(is_present=False).count()
        
        return JsonResponse({
            'success': True,
            'message': 'Asistencia actualizada correctamente',
            'present_count': present_count,
            'absent_count': absent_count,
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ========================================
# Vistas de Estudiantes y Competencias
# ========================================

def students_list(request):
    """Vista para mostrar el listado de estudiantes."""
    students = Student.objects.filter(is_active=True).prefetch_related('student_competencies')
    total_competencies = Competency.objects.count()
    
    students_data = []
    for student in students:
        students_data.append({
            'student': student,
            'attendance_percentage': student.attendance_percentage,
            'competencies_achieved': student.competencies_achieved,
            'total_competencies': total_competencies,
        })
    
    return render(request, 'attendance/students_list.html', {
        'students_data': students_data,
        'total_students': len(students_data),
    })


def student_detail(request, student_id):
    """Vista para ver el detalle de un estudiante con sus competencias."""
    student = get_object_or_404(Student, id=student_id)
    competencies = Competency.objects.all()
    
    # Obtener las competencias del estudiante
    student_competency_map = {
        sc.competency_id: sc 
        for sc in student.student_competencies.all()
    }
    
    # Preparar datos de competencias
    competencies_data = []
    for competency in competencies:
        sc = student_competency_map.get(competency.id)
        competencies_data.append({
            'competency': competency,
            'is_achieved': sc.is_achieved if sc else False,
            'notes': sc.notes if sc else '',
        })
    
    context = {
        'student': student,
        'competencies_data': competencies_data,
        'attendance_count': student.attendance_count,
        'absence_count': student.absence_count,
        'attendance_percentage': student.attendance_percentage,
        'competencies_achieved': student.competencies_achieved,
        'total_competencies': len(competencies_data),
    }
    return render(request, 'attendance/student_detail.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def save_student_competencies(request, student_id):
    """API endpoint para guardar las competencias de un estudiante via AJAX."""
    try:
        student = get_object_or_404(Student, id=student_id)
        data = json.loads(request.body)
        competencies_data = data.get('competencies', {})
        
        for competency_id, is_achieved in competencies_data.items():
            competency = get_object_or_404(Competency, id=int(competency_id))
            StudentCompetency.objects.update_or_create(
                student=student,
                competency=competency,
                defaults={'is_achieved': is_achieved}
            )
        
        return JsonResponse({
            'success': True,
            'message': 'Competencias guardadas correctamente',
            'competencies_achieved': student.competencies_achieved,
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def students_manage(request):
    """Vista para gestionar estudiantes (añadir/retirar)."""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip() or None
            github_username = request.POST.get('github_username', '').strip() or None
            
            if first_name and last_name:
                Student.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    github_username=github_username,
                    is_active=True
                )
        
        elif action == 'deactivate':
            student_id = request.POST.get('student_id')
            if student_id:
                Student.objects.filter(id=student_id).update(is_active=False)
        
        elif action == 'activate':
            student_id = request.POST.get('student_id')
            if student_id:
                Student.objects.filter(id=student_id).update(is_active=True)
        
        elif action == 'delete':
            student_id = request.POST.get('student_id')
            if student_id:
                Student.objects.filter(id=student_id).delete()
        
        return redirect('attendance:students_manage')
    
    active_students = Student.objects.filter(is_active=True)
    inactive_students = Student.objects.filter(is_active=False)
    
    return render(request, 'attendance/students_manage.html', {
        'active_students': active_students,
        'inactive_students': inactive_students,
    })
