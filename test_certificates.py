"""
سكريبت اختبار بسيط لنظام الشهادات
"""
from app import app
from models import db, Certificate, User, Role
from datetime import datetime, timedelta

def test_certificate_system():
    """اختبار نظام الشهادات"""
    with app.app_context():
        print("="*60)
        print("اختبار نظام إدارة الشهادات")
        print("="*60)
        
        # التحقق من وجود جدول الشهادات
        try:
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'certificates' in tables:
                print("✓ جدول الشهادات موجود")
                
                # عرض أعمدة الجدول
                columns = [col['name'] for col in inspector.get_columns('certificates')]
                print(f"\n✓ أعمدة الجدول ({len(columns)}):")
                for col in columns:
                    print(f"  - {col}")
                
                # عد الشهادات الموجودة
                cert_count = Certificate.query.count()
                print(f"\n✓ عدد الشهادات في قاعدة البيانات: {cert_count}")
                
                # عرض معلومات المشرفين الفرعيين
                sub_supervisors = User.query.filter_by(role=Role.SUB_SUPERVISOR).all()
                print(f"\n✓ عدد المشرفين الفرعيين: {len(sub_supervisors)}")
                for sup in sub_supervisors:
                    certs = Certificate.query.filter_by(created_by=sup.id).count()
                    print(f"  - {sup.name}: {certs} شهادة")
                
                print("\n" + "="*60)
                print("✓✓✓ نظام الشهادات جاهز للاستخدام!")
                print("="*60)
                
            else:
                print("✗ جدول الشهادات غير موجود!")
                print("\nالرجاء تشغيل:")
                print("  python update_db_certificates.py")
                
        except Exception as e:
            print(f"\n✗ خطأ أثناء الاختبار: {str(e)}")
            return False
        
        return True

if __name__ == '__main__':
    test_certificate_system()
