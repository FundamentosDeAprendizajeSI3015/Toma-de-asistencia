/**
 * Main JavaScript for Attendance App
 * Handles theme toggle, attendance saving, and UI interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    initThemeToggle();
    initAttendanceControls();
});

/* ========================================
   Theme Toggle
   ======================================== */

function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    
    // Load saved theme or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
}

/* ========================================
   Attendance Controls
   ======================================== */

function initAttendanceControls() {
    const saveBtn = document.getElementById('saveAttendance');
    const selectAllBtn = document.getElementById('selectAll');
    const deselectAllBtn = document.getElementById('deselectAll');
    const checkboxes = document.querySelectorAll('.student-checkbox');
    
    // Select All
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', function() {
            checkboxes.forEach(cb => cb.checked = true);
            updateStats();
        });
    }
    
    // Deselect All
    if (deselectAllBtn) {
        deselectAllBtn.addEventListener('click', function() {
            checkboxes.forEach(cb => cb.checked = false);
            updateStats();
        });
    }
    
    // Update stats on checkbox change
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateStats);
    });
    
    // Save Attendance
    if (saveBtn) {
        saveBtn.addEventListener('click', saveAttendance);
    }
}

function updateStats() {
    const checkboxes = document.querySelectorAll('.student-checkbox');
    const presentCount = document.querySelectorAll('.student-checkbox:checked').length;
    const totalStudents = typeof TOTAL_STUDENTS !== 'undefined' ? TOTAL_STUDENTS : checkboxes.length;
    const absentCount = totalStudents - presentCount;
    
    const presentCountEl = document.getElementById('presentCount');
    const absentCountEl = document.getElementById('absentCount');
    
    if (presentCountEl) presentCountEl.textContent = presentCount;
    if (absentCountEl) absentCountEl.textContent = absentCount;
}

async function saveAttendance() {
    const saveBtn = document.getElementById('saveAttendance');
    const btnText = saveBtn.querySelector('.btn-text');
    const btnLoading = saveBtn.querySelector('.btn-loading');
    
    // Collect attendance data
    const checkboxes = document.querySelectorAll('.student-checkbox');
    const attendanceData = {};
    
    checkboxes.forEach(checkbox => {
        const studentId = checkbox.getAttribute('data-student-id');
        attendanceData[studentId] = checkbox.checked;
    });
    
    // Show loading state
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    saveBtn.disabled = true;
    
    try {
        const response = await fetch('/save/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ attendance: attendanceData })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('✓ Asistencia guardada correctamente', 'success');
        } else {
            showToast('Error: ' + (result.error || 'No se pudo guardar'), 'error');
        }
    } catch (error) {
        console.error('Error saving attendance:', error);
        showToast('Error al guardar la asistencia', 'error');
    } finally {
        // Reset button state
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
        saveBtn.disabled = false;
    }
}

/* ========================================
   Toast Notifications
   ======================================== */

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    const toastMessage = toast.querySelector('.toast-message');
    toastMessage.textContent = message;
    
    toast.className = 'toast ' + type;
    toast.classList.add('show');
    
    // Auto hide after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
