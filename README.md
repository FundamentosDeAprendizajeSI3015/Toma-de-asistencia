# 📋 App Toma de Asistencia

Sistema de gestión de asistencia y evaluación de competencias para el curso **Fundamentos de Aprendizaje Automático** de EAFIT.

## ✨ Características

- ✅ Toma de asistencia diaria con checkboxes
- ✅ Historial de sesiones de asistencia
- ✅ Edición de asistencia (solo el mismo día)
- ✅ Listado de estudiantes con información de contacto
- ✅ Sistema de 10 competencias evaluables por estudiante
- ✅ Gestión de estudiantes (añadir/desactivar/eliminar)
- ✅ Tema oscuro/claro con persistencia
- ✅ Interfaz responsive y moderna

## 🛠️ Tecnologías

- **Backend:** Django 6.0
- **Base de datos:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript vanilla

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Figs0203/App-toma-de-asistencia.git
cd App-toma-de-asistencia
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

Esto creará la base de datos y cargará:
- Los 26 estudiantes del curso
- Las 10 competencias predefinidas

### 5. Ejecutar el servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en **http://127.0.0.1:8000/**

## 🔗 Rutas principales

| Ruta | Descripción |
|------|-------------|
| `/` | Tomar asistencia del día |
| `/history/` | Historial de sesiones |
| `/students/` | Listado de estudiantes |
| `/student/<id>/` | Detalle y competencias del estudiante |
| `/students/manage/` | Gestionar estudiantes |

## 🎯 Competencias evaluadas

1. Estadística
2. Regresión Logística
3. Regresión Lineal
4. Máquina de Soporte Vectorial (SVM)
5. Clustering
6. TSNE
7. VHTSNE
8. UMAP
9. Kernels
10. DBSCAN

## 📝 Uso opcional: Crear superusuario

Para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

Luego accede a **http://127.0.0.1:8000/admin/**

## 📄 Licencia

Este proyecto fue desarrollado para uso académico en EAFIT.
