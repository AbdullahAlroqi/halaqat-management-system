from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Role, LeaveRequest, LeaveType, Schedule, Attendance, SystemSettings, Notification, ActivityLog, AbsenceStatus
from routes_employee import employee_bp
from routes_supervisor import supervisor_bp
from routes_admin import admin_bp
from datetime import datetime, timedelta
import os
import openpyxl
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'الرجاء تسجيل الدخول للوصول إلى هذه الصفحة'

# تسجيل الـ Blueprints
app.register_blueprint(employee_bp)
app.register_blueprint(supervisor_bp)
app.register_blueprint(admin_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# جعل الإعدادات متاحة في جميع القوالب
@app.context_processor
def inject_settings():
    settings = SystemSettings.query.first()
    return dict(system_settings=settings)

# Decorators للتحقق من الأدوار
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# تهيئة قاعدة البيانات
def init_database():
    with app.app_context():
        db.create_all()
        
        # إنشاء مدير النظام الأساسي إذا لم يكن موجوداً
        admin = User.query.filter_by(role=Role.MAIN_ADMIN).first()
        if not admin:
            admin = User(
                national_id='1000000000',
                name='مدير النظام',
                role=Role.MAIN_ADMIN,
                gender='ذكر',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # إنشاء أنواع الإجازات الافتراضية
        if LeaveType.query.count() == 0:
            for lt in Config.DEFAULT_LEAVE_TYPES:
                leave_type = LeaveType(**lt)
                db.session.add(leave_type)
        
        # إنشاء إعدادات النظام
        if SystemSettings.query.count() == 0:
            settings = SystemSettings()
            db.session.add(settings)
        
        # إنشاء حالات الغياب الافتراضية
        if AbsenceStatus.query.count() == 0:
            default_statuses = [
                {'name': 'حاضر', 'color': '#28a745', 'is_counted_as_absent': False},
                {'name': 'غائب بعذر', 'color': '#ffc107', 'is_counted_as_absent': True},
                {'name': 'غائب بدون عذر', 'color': '#dc3545', 'is_counted_as_absent': True},
                {'name': 'إجازة', 'color': '#17a2b8', 'is_counted_as_absent': False},
                {'name': 'إجازة مرضية', 'color': '#6c757d', 'is_counted_as_absent': False},
            ]
            for status_data in default_statuses:
                status = AbsenceStatus(**status_data)
                db.session.add(status)
        
        db.session.commit()
        print('تم تهيئة قاعدة البيانات بنجاح')

# الصفحة الرئيسية
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == Role.EMPLOYEE:
            return redirect(url_for('employee.dashboard'))
        elif current_user.role in [Role.MAIN_SUPERVISOR, Role.SUB_SUPERVISOR]:
            return redirect(url_for('supervisor.dashboard'))
        else:
            return redirect(url_for('admin.dashboard'))
    return render_template('index.html')

# تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        national_id = request.form.get('national_id')
        password = request.form.get('password')
        
        user = User.query.filter_by(national_id=national_id, is_active=True).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash(f'مرحباً بك {user.name}', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('رقم الهوية أو كلمة المرور غير صحيحة', 'danger')
    
    return render_template('login.html')

# تسجيل الخروج
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
