from django.contrib import admin
from .models import Student, AttendanceSession, AttendanceRecord, Competency, StudentCompetency


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'github_username', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('first_name', 'last_name', 'email', 'github_username')
    ordering = ('last_name', 'first_name')


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'present_count', 'absent_count', 'created_at')
    list_filter = ('date',)
    ordering = ('-date',)


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'is_present', 'updated_at')
    list_filter = ('is_present', 'session__date')
    search_fields = ('student__first_name', 'student__last_name')


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'description')
    ordering = ('order',)


@admin.register(StudentCompetency)
class StudentCompetencyAdmin(admin.ModelAdmin):
    list_display = ('student', 'competency', 'is_achieved', 'updated_at')
    list_filter = ('is_achieved', 'competency')
    search_fields = ('student__first_name', 'student__last_name', 'competency__name')
