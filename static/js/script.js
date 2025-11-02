// تفعيل tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// دالة لتأكيد الحذف
function confirmDelete(message) {
    return confirm(message || 'هل أنت متأكد من الحذف؟');
}

// دالة لتأكيد الإجراء
function confirmAction(message) {
    return confirm(message || 'هل أنت متأكد من هذا الإجراء؟');
}

// دالة لطباعة الصفحة
function printPage() {
    window.print();
}

// دالة لتنسيق التاريخ
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('ar-SA', options);
}

// دالة لعرض loader
function showLoader() {
    const loader = document.createElement('div');
    loader.className = 'loader';
    loader.id = 'globalLoader';
    document.body.appendChild(loader);
}

function hideLoader() {
    const loader = document.getElementById('globalLoader');
    if (loader) {
        loader.remove();
    }
}

// PWA - تسجيل Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/sw.js')
            .then(function(registration) {
                console.log('Service Worker registered successfully');
            })
            .catch(function(error) {
                console.log('Service Worker registration failed:', error);
            });
    });
}

// PWA - زر التثبيت
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    // عرض زر التثبيت
    const installButton = document.getElementById('installButton');
    if (installButton) {
        installButton.style.display = 'block';
        
        installButton.addEventListener('click', () => {
            installButton.style.display = 'none';
            deferredPrompt.prompt();
            
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the install prompt');
                }
                deferredPrompt = null;
            });
        });
    }
});

// دالة لاختيار جميع checkboxes
function toggleAllCheckboxes(source) {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="employee_ids"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = source.checked;
    });
}

// دالة للبحث في الجداول
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        let found = false;
        
        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            if (cell) {
                const textValue = cell.textContent || cell.innerText;
                if (textValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        
        row.style.display = found ? '' : 'none';
    }
}

// دالة لتحديث الإحصائيات بشكل ديناميكي
function updateDashboardStats() {
    // يمكن استخدامها لتحديث الإحصائيات عبر AJAX
    // مثال:
    // fetch('/api/stats')
    //     .then(response => response.json())
    //     .then(data => {
    //         document.getElementById('totalEmployees').textContent = data.total_employees;
    //     });
}

// دالة لعرض التنبيهات
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// دالة للتحقق من صحة النموذج
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// دالة للتحقق من رقم الهوية
function validateNationalId(id) {
    return /^\d{10}$/.test(id);
}

// دالة لتنسيق الأرقام
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// دالة لحساب الفرق بين تاريخين
function getDaysDifference(date1, date2) {
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    const timeDiff = Math.abs(d2.getTime() - d1.getTime());
    return Math.ceil(timeDiff / (1000 * 3600 * 24));
}

// دالة لتحديث عدد الأيام في طلب الإجازة
function updateLeaveDays() {
    const startDate = document.getElementById('start_date');
    const endDate = document.getElementById('end_date');
    const daysDisplay = document.getElementById('days_count');
    
    if (startDate && endDate && startDate.value && endDate.value) {
        const days = getDaysDifference(startDate.value, endDate.value) + 1;
        if (daysDisplay) {
            daysDisplay.textContent = days + ' يوم';
        }
    }
}

// Event listeners للتواريخ
document.addEventListener('DOMContentLoaded', function() {
    const startDate = document.getElementById('start_date');
    const endDate = document.getElementById('end_date');
    
    if (startDate && endDate) {
        startDate.addEventListener('change', updateLeaveDays);
        endDate.addEventListener('change', updateLeaveDays);
    }
});
