from django.db import migrations


def create_sample_students(apps, schema_editor):
    """Crear estudiantes de ejemplo para demostración."""
    Student = apps.get_model('attendance', 'Student')
    
    sample_students = [
        ('María', 'García López', 'maria.garcia@ejemplo.com'),
        ('Carlos', 'Rodríguez Pérez', 'carlos.rodriguez@ejemplo.com'),
        ('Ana', 'Martínez Sánchez', 'ana.martinez@ejemplo.com'),
        ('Juan', 'López Fernández', 'juan.lopez@ejemplo.com'),
        ('Laura', 'Hernández García', 'laura.hernandez@ejemplo.com'),
        ('Pedro', 'González Martín', 'pedro.gonzalez@ejemplo.com'),
        ('Sofía', 'Díaz Ruiz', 'sofia.diaz@ejemplo.com'),
        ('Diego', 'Moreno Jiménez', 'diego.moreno@ejemplo.com'),
        ('Valentina', 'Álvarez Torres', 'valentina.alvarez@ejemplo.com'),
        ('Andrés', 'Romero Vargas', 'andres.romero@ejemplo.com'),
        ('Camila', 'Navarro Silva', 'camila.navarro@ejemplo.com'),
        ('Sebastián', 'Torres Mendoza', 'sebastian.torres@ejemplo.com'),
        ('Isabella', 'Ramírez Castro', 'isabella.ramirez@ejemplo.com'),
        ('Mateo', 'Flores Ortiz', 'mateo.flores@ejemplo.com'),
        ('Luciana', 'Acosta Ríos', 'luciana.acosta@ejemplo.com'),
    ]
    
    for first_name, last_name, email in sample_students:
        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True
        )


def remove_sample_students(apps, schema_editor):
    """Eliminar estudiantes de ejemplo."""
    Student = apps.get_model('attendance', 'Student')
    Student.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_students, remove_sample_students),
    ]
