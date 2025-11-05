"""
سكريبت تحديث قاعدة البيانات الشامل
- إضافة جدول الشهادات
- إضافة حقل رصيد الإجازات
"""
from app import app
from models import db, Certificate, User
import sys

def update_database():
    """تحديث قاعدة البيانات"""
    try:
        with app.app_context():
            print("="*60)
            print("جاري تحديث قاعدة البيانات...")
            print("="*60)
            
            # إنشاء جميع الجداول
            db.create_all()
            
            print("\n✓ تم إنشاء/تحديث الجداول")
            
            # إضافة حقل leave_balance إلى المستخدمين الموجودين إذا لم يكن موجوداً
            try:
                users_updated = 0
                for user in User.query.all():
                    if not hasattr(user, 'leave_balance') or user.leave_balance is None:
                        user.leave_balance = 0
                        users_updated += 1
                
                if users_updated > 0:
                    db.session.commit()
                    print(f"✓ تم تحديث رصيد الإجازات لـ {users_updated} مستخدم")
                else:
                    print("✓ رصيد الإجازات محدث مسبقاً")
            except Exception as e:
                print(f"⚠ ملاحظة: {str(e)}")
            
            # عرض الجداول
            print("\n" + "="*60)
            print("الجداول المتاحة:")
            print("="*60)
            
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            for i, table in enumerate(tables, 1):
                print(f"  {i}. {table}")
            
            # إحصائيات
            print("\n" + "="*60)
            print("الإحصائيات:")
            print("="*60)
            
            total_users = User.query.count()
            total_certs = Certificate.query.count()
            
            print(f"  • إجمالي المستخدمين: {total_users}")
            print(f"  • إجمالي الشهادات: {total_certs}")
            
            print("\n" + "="*60)
            print("✅ تم تحديث قاعدة البيانات بنجاح!")
            print("="*60)
            print("\nالتحديثات المطبقة:")
            print("  ✓ إضافة جدول الشهادات (certificates)")
            print("  ✓ إضافة حقل رصيد الإجازات (leave_balance)")
            print("\n" + "="*60)
            
            return True
            
    except Exception as e:
        print(f"\n❌ خطأ أثناء تحديث قاعدة البيانات: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = update_database()
    
    if success:
        print("\n✅ يمكنك الآن تشغيل التطبيق!")
        print("   python app.py")
    else:
        print("\n❌ فشل التحديث. الرجاء مراجعة الأخطاء أعلاه.")
    
    sys.exit(0 if success else 1)
