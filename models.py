from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
<<<<<<< HEAD
import pytz

db = SQLAlchemy()

# التوقيت السعودي
SAUDI_TZ = pytz.timezone('Asia/Riyadh')

def get_saudi_time():
    """الحصول على الوقت الحالي بتوقيت السعودية"""
    return datetime.now(SAUDI_TZ)

=======

db = SQLAlchemy()

>>>>>>> 2af5888e290fafbfb39432b6ce530ed87f045bdf
# جدول الأدوار
class Role:
    EMPLOYEE = 'موظف'
    MAIN_SUPERVISOR = 'مشرف رئيسي'
    SUB_SUPERVISOR = 'مشرف فرعي'
    SUB_ADMIN = 'مدير نظام فرعي'
    MAIN_ADMIN = 'مدير النظام الأساسي'

# جدول الجنس
class Gender:
    MALE = 'ذكر'
    FEMALE = 'أنثى'

# أوقات الدوام (بالساعة)
class ShiftTime:
    # يمكن تخزين الوقت كنص مثل "4:00 م - 8:00 م"
    pass

# جدول الحالة
class Status:
    PENDING = 'قيد الانتظار'
    APPROVED = 'مقبول'
    REJECTED = 'مرفوض'

# نموذج المستخدم
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    national_id = db.Column(db.String(10), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    department = db.Column(db.String(100))
    shift_time = db.Column(db.String(50))  # مثل: "4:00 م - 8:00 م"
    
    # معلومات الجدول الدراسي
    period = db.Column(db.String(50))  # الفترة: الأولى، الثانية، الثالثة، الرابعة، السادسة
    work_time = db.Column(db.String(50))  # الوقت: 4م-8م، 10ص-2م، الخ
    rest_days = db.Column(db.String(100))  # أيام الراحة: الاثنين والثلاثاء، الجمعة والسبت، الخ
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقة مع المشرف
    supervisor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    supervisor = db.relationship('User', remote_side=[id], backref='subordinates')
    
    # العلاقات
    schedules = db.relationship('Schedule', backref='employee', lazy='dynamic', foreign_keys='Schedule.employee_id')
    leave_requests = db.relationship('LeaveRequest', backref='employee', lazy='dynamic', foreign_keys='LeaveRequest.employee_id')
    attendance_records = db.relationship('Attendance', backref='employee', lazy='dynamic', foreign_keys='Attendance.employee_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.name}>'

# نموذج الجدول الدراسي
class Schedule(db.Model):
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)  # السبت، الأحد، إلخ
    shift_time = db.Column(db.String(50), nullable=False)  # مثل: "4:00 م - 8:00 م"
    is_rest_day = db.Column(db.Boolean, default=False)  # يوم راحة
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    
    def __repr__(self):
        return f'<Schedule {self.employee_id} - {self.day_of_week}>'

# نموذج أنواع الإجازات
class LeaveType(db.Model):
    __tablename__ = 'leave_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    max_days = db.Column(db.Integer, nullable=False)
    requires_attachment = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    leave_requests = db.relationship('LeaveRequest', backref='leave_type', lazy='dynamic')
    
    def __repr__(self):
        return f'<LeaveType {self.name}>'

# نموذج طلبات الإجازات
class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_types.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days_count = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text)
    attachment_path = db.Column(db.String(500))
    status = db.Column(db.String(20), default=Status.PENDING)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviewed_at = db.Column(db.DateTime)
    review_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    
    def __repr__(self):
        return f'<LeaveRequest {self.employee_id} - {self.leave_type_id}>'

# نموذج الحضور والغياب
class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # حاضر / غائب / إجازة
<<<<<<< HEAD
    absence_status_id = db.Column(db.Integer, db.ForeignKey('absence_statuses.id'))  # الربط بحالة الغياب
=======
>>>>>>> 2af5888e290fafbfb39432b6ce530ed87f045bdf
    notes = db.Column(db.Text)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    recorder = db.relationship('User', foreign_keys=[recorded_by])
<<<<<<< HEAD
    absence_status = db.relationship('AbsenceStatus', backref='attendance_records')
=======
>>>>>>> 2af5888e290fafbfb39432b6ce530ed87f045bdf
    
    __table_args__ = (db.UniqueConstraint('employee_id', 'date', name='_employee_date_uc'),)
    
    def __repr__(self):
        return f'<Attendance {self.employee_id} - {self.date}>'

# نموذج إعدادات النظام
class SystemSettings(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(200), default='نظام إدارة معلمي الحلقات - مكة المكرمة')
    primary_color = db.Column(db.String(20), default='#0d7377')
    secondary_color = db.Column(db.String(20), default='#14FFEC')
    accent_color = db.Column(db.String(20), default='#323232')
    attachment_retention_days = db.Column(db.Integer, default=60)
    logo_path = db.Column(db.String(500))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemSettings {self.system_name}>'

# نموذج التنبيهات
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    related_type = db.Column(db.String(50))  # leave_request, schedule, etc.
    related_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='notifications')
    
    def __repr__(self):
        return f'<Notification {self.title}>'
<<<<<<< HEAD

# نموذج سجل النشاطات (Activity Logs)
class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # نوع العملية: إضافة، تعديل، حذف
    target_type = db.Column(db.String(50), nullable=False)  # نوع الهدف: موظف، مشرف، إجازة، إلخ
    target_id = db.Column(db.Integer)  # معرف الهدف
    details = db.Column(db.Text)  # تفاصيل العملية
    ip_address = db.Column(db.String(50))  # عنوان IP
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='activity_logs')
    
    def __repr__(self):
        return f'<ActivityLog {self.action} - {self.target_type}>'

# نموذج حالات الغياب
class AbsenceStatus(db.Model):
    __tablename__ = 'absence_statuses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # اسم الحالة: حاضر، غائب بعذر، غائب بدون عذر، إجازة، إلخ
    color = db.Column(db.String(20), default='#6c757d')  # اللون المميز للحالة
    is_counted_as_absent = db.Column(db.Boolean, default=True)  # هل يحتسب كغياب
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AbsenceStatus {self.name}>'
=======
>>>>>>> 2af5888e290fafbfb39432b6ce530ed87f045bdf
