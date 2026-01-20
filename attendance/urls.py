from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Asistencia
    path('', views.index, name='index'),
    path('save/', views.save_attendance, name='save_attendance'),
    path('history/', views.history, name='history'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('session/<int:session_id>/edit/', views.edit_session, name='edit_session'),
    path('session/<int:session_id>/save/', views.save_session_attendance, name='save_session_attendance'),
    
    # Estudiantes
    path('students/', views.students_list, name='students_list'),
    path('students/manage/', views.students_manage, name='students_manage'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('student/<int:student_id>/competencies/save/', views.save_student_competencies, name='save_student_competencies'),
]
