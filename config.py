import os
from datetime import timedelta

class Config:
    # مسار المشروع
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # المفتاح السري
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'halaqat-makkah-secret-key-2024'
    
    # إعدادات قاعدة البيانات
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'halaqat.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات الجلسة
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # مجلد رفع الملفات
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'pdf', 'jpg', 'jpeg', 'png'}
    
    # إعدادات النظام الافتراضية
    SYSTEM_NAME = 'نظام إدارة معلمي الحلقات - مكة المكرمة'
    PRIMARY_COLOR = '#0d7377'  # لون أخضر مائل للأزرق
    SECONDARY_COLOR = '#14FFEC'  # لون فيروزي
    ACCENT_COLOR = '#323232'  # رمادي غامق
    
    # مدة حذف المرفقات (بالأيام)
    ATTACHMENT_RETENTION_DAYS = 60
    
    # أنواع الإجازات الافتراضية
    DEFAULT_LEAVE_TYPES = [
        {'name': 'إجازة مرضية', 'max_days': 10, 'requires_attachment': True},
        {'name': 'إجازة طارئة', 'max_days': 3, 'requires_attachment': False},
        {'name': 'إجازة سنوية', 'max_days': 21, 'requires_attachment': False},
        {'name': 'إجازة اضطرارية', 'max_days': 5, 'requires_attachment': True},
    ]
    
    # إنشاء المجلدات المطلوبة
    @staticmethod
    def init_app(app):
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(os.path.join(Config.BASE_DIR, 'static', 'uploads'), exist_ok=True)
