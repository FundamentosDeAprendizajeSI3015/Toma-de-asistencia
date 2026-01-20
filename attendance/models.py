from django.db import models
import unicodedata


def normalize_text(text):
    """Normaliza texto quitando acentos para ordenamiento."""
    if not text:
        return ''
    # Descomponer caracteres acentuados y filtrar las marcas de acento
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn').lower()


class Student(models.Model):
    """Modelo para representar un estudiante."""
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    github_username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Usuario GitHub")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    # Campo para ordenamiento sin acentos (se genera automáticamente)
    last_name_normalized = models.CharField(max_length=100, blank=True, editable=False)

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['last_name_normalized', 'first_name']

    def save(self, *args, **kwargs):
        """Al guardar, normaliza el apellido para ordenamiento correcto."""
        self.last_name_normalized = normalize_text(self.last_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def attendance_count(self):
        """Número de clases a las que asistió."""
        return self.attendance_records.filter(is_present=True).count()

    @property
    def absence_count(self):
        """Número de clases a las que faltó."""
        return self.attendance_records.filter(is_present=False).count()

    @property
    def attendance_percentage(self):
        """Porcentaje de asistencia."""
        total = self.attendance_records.count()
        if total == 0:
            return 0
        return round((self.attendance_count / total) * 100, 1)

    @property
    def competencies_achieved(self):
        """Número de competencias logradas."""
        return self.student_competencies.filter(is_achieved=True).count()

    @property
    def competencies_total(self):
        """Total de competencias evaluadas."""
        return self.student_competencies.count()


class Competency(models.Model):
    """Modelo para representar una competencia/habilidad a evaluar."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    order = models.IntegerField(default=0, verbose_name="Orden")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Competencia"
        verbose_name_plural = "Competencias"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class StudentCompetency(models.Model):
    """Modelo para registrar si un estudiante ha logrado una competencia."""
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='student_competencies',
        verbose_name="Estudiante"
    )
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE,
        related_name='student_competencies',
        verbose_name="Competencia"
    )
    is_achieved = models.BooleanField(default=False, verbose_name="Lograda")
    notes = models.TextField(blank=True, verbose_name="Notas")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Competencia del Estudiante"
        verbose_name_plural = "Competencias de Estudiantes"
        unique_together = ['student', 'competency']

    def __str__(self):
        status = "✓" if self.is_achieved else "✗"
        return f"{self.student} - {self.competency} - {status}"


class AttendanceSession(models.Model):
    """Modelo para representar una sesión de asistencia (por fecha)."""
    date = models.DateField(unique=True, verbose_name="Fecha")
    description = models.CharField(max_length=255, blank=True, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sesión de Asistencia"
        verbose_name_plural = "Sesiones de Asistencia"
        ordering = ['-date']

    def __str__(self):
        return f"Sesión del {self.date.strftime('%d/%m/%Y')}"

    @property
    def present_count(self):
        return self.records.filter(is_present=True).count()

    @property
    def absent_count(self):
        return self.records.filter(is_present=False).count()


class AttendanceRecord(models.Model):
    """Modelo para registrar la asistencia de un estudiante en una sesión."""
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name="Estudiante"
    )
    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name='records',
        verbose_name="Sesión"
    )
    is_present = models.BooleanField(default=False, verbose_name="Presente")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro de Asistencia"
        verbose_name_plural = "Registros de Asistencia"
        unique_together = ['student', 'session']

    def __str__(self):
        status = "Presente" if self.is_present else "Ausente"
        return f"{self.student} - {self.session.date} - {status}"

