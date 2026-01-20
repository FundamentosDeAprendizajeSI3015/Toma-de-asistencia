from django.db import migrations


def create_competencies(apps, schema_editor):
    """Crear las 10 competencias predefinidas."""
    Competency = apps.get_model('attendance', 'Competency')
    
    competencies = [
        (1, 'Estadística', 'Conocimientos fundamentales de estadística descriptiva e inferencial'),
        (2, 'Regresión Logística', 'Comprensión y aplicación de modelos de regresión logística'),
        (3, 'Regresión Lineal', 'Comprensión y aplicación de modelos de regresión lineal'),
        (4, 'Máquina de Soporte Vectorial', 'Conocimiento de SVM para clasificación y regresión'),
        (5, 'Clustering', 'Técnicas de agrupamiento y análisis de clusters'),
        (6, 'TSNE', 'Reducción de dimensionalidad con t-SNE'),
        (7, 'VHTSNE', 'Variantes y optimizaciones de t-SNE'),
        (8, 'UMAP', 'Reducción de dimensionalidad con UMAP'),
        (9, 'Kernels', 'Comprensión de funciones kernel y su aplicación'),
        (10, 'DBSCAN', 'Clustering basado en densidad con DBSCAN'),
    ]
    
    for order, name, description in competencies:
        Competency.objects.create(
            name=name,
            description=description,
            order=order
        )


def remove_competencies(apps, schema_editor):
    """Eliminar las competencias."""
    Competency = apps.get_model('attendance', 'Competency')
    Competency.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_competency_studentcompetency'),
    ]

    operations = [
        migrations.RunPython(create_competencies, remove_competencies),
    ]
