from django.db import migrations


def replace_students(apps, schema_editor):
    """Eliminar estudiantes de prueba y añadir los estudiantes reales."""
    Student = apps.get_model('attendance', 'Student')
    
    # Eliminar todos los estudiantes existentes
    Student.objects.all().delete()
    
    # Lista de estudiantes reales
    students = [
        ('Jaider', 'España Paternina', 'jespnap@eafit.edu.co'),
        ('Esteban', 'Álvarez Zuluaga', 'ealvarezzz@eafit.edu.co'),
        ('Juan', 'Citelly Guzmán', 'jccitellyg@eafit.edu.co'),
        ('Miguel', 'Mercado Mercado', 'mamercado@eafit.edu.co'),
        ('Santiago', 'Manco Maya', 'smancom@eafit.edu.co'),
        ('Sebastián', 'Uribe Ruiz', 'sauriber2@eafit.edu.co'),
        ('Mateo', 'Pineda Álvarez', 'mpinedaa4@eafit.edu.co'),
        ('Agustín', 'Figueroa Sierra', 'afigueroas@eafit.edu.co'),
        ('Camilo', 'Salazar Acevedo', 'csalazara@eafit.edu.co'),
        ('Martín', 'Vanegas Ospina', 'mvanegaso1@eafit.edu.co'),
        ('Jean', 'Londoño Ocampo', 'jclondonoo@eafit.edu.co'),
        ('Nicolás', 'Ospina Torres', 'nospinat@eafit.edu.co'),
        ('Alejandro', 'Garcés Ramírez', 'agarcesr@eafit.edu.co'),
        ('Pablo', 'Cabrejos Munera', 'pcabrejosm@eafit.edu.co'),
        ('Luciana', 'Hoyos Pérez', 'lhoyosp1@eafit.edu.co'),
        ('María Alejandra', 'Ocampo Giraldo', 'maocampog1@eafit.edu.co'),
        ('Mariana', 'Valderrama Castañeda', 'mvalderrc1@eafit.edu.co'),
        ('Juan Esteban', 'Alzate Ospina', 'jealzateo@eafit.edu.co'),
        ('Juan', 'Lopera Soto', 'jmloperas@eafit.edu.co'),
        ('Luis', 'Nerio Pereira', 'laneriop@eafit.edu.co'),
        ('Isabella', 'Camacho Monsalve', 'icamachom1@eafit.edu.co'),
        ('Alejandro', 'Sepúlveda Posada', 'asepulvedp@eafit.edu.co'),
        ('Sebastián', 'Durán Fernández', 'sduranf@eafit.edu.co'),
        ('Paula', 'Llanos López', 'pillanosl@eafit.edu.co'),
        ('Lucas', 'Higuita Bedoya', 'lhiguitab@eafit.edu.co'),
        ('Santiago', 'Gómez Ospina', 'sgomezo14@eafit.edu.co'),
    ]
    
    for first_name, last_name, email in students:
        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True
        )


def reverse_students(apps, schema_editor):
    """Revertir la migración."""
    pass  # No revertible de manera simple


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_create_competencies'),
    ]

    operations = [
        migrations.RunPython(replace_students, reverse_students),
    ]
