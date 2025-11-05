"""
سكريبت تحديث قاعدة البيانات لإضافة جدول الشهادات
"""
from app import app
from models import db, Certificate
import sys

def update_database():
    """تحديث قاعدة البيانات بإضافة جدول الشهادات"""
    try:
        with app.app_context():
            print("جاري تحديث قاعدة البيانات...")
            
            # إنشاء جدول الشهادات
            db.create_all()
            
            print("✓ تم إنشاء جدول الشهادات بنجاح")
            print("\nالجداول المتاحة الآن:")
            
            # عرض جميع الجداول
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            for i, table in enumerate(tables, 1):
                print(f"  {i}. {table}")
            
            print("\n" + "="*50)
            print("تم تحديث قاعدة البيانات بنجاح!")
            print("="*50)
            
            return True
            
    except Exception as e:
        print(f"\n❌ خطأ أثناء تحديث قاعدة البيانات: {str(e)}")
        return False

if __name__ == '__main__':
    success = update_database()
    sys.exit(0 if success else 1)
