"""
سكريبت ترحيل قاعدة البيانات - إضافة الحقول الجديدة
"""
import sqlite3
import os

def migrate_database():
    """تحديث قاعدة البيانات بإضافة الأعمدة الجديدة"""
    
    db_path = 'instance/halaqat.db'
    
    if not os.path.exists(db_path):
        print("⚠️ قاعدة البيانات غير موجودة. سيتم إنشاؤها عند تشغيل التطبيق.")
        return True
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("="*60)
        print("جاري تحديث قاعدة البيانات...")
        print("="*60)
        
        # التحقق من وجود عمود leave_balance
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'leave_balance' not in columns:
            print("\n✓ إضافة عمود leave_balance إلى جدول users...")
            cursor.execute("ALTER TABLE users ADD COLUMN leave_balance INTEGER DEFAULT 0")
            conn.commit()
            print("✓ تم إضافة عمود leave_balance بنجاح")
        else:
            print("\n✓ عمود leave_balance موجود مسبقاً")
        
        # التحقق من وجود جدول certificates
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='certificates'")
        if not cursor.fetchone():
            print("\n✓ سيتم إنشاء جدول certificates عند تشغيل التطبيق")
        else:
            print("\n✓ جدول certificates موجود مسبقاً")
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ تم تحديث قاعدة البيانات بنجاح!")
        print("="*60)
        print("\nيمكنك الآن تشغيل التطبيق:")
        print("  python app.py")
        print("\nأو على Windows:")
        print("  run.bat")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ أثناء التحديث: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    success = migrate_database()
    sys.exit(0 if success else 1)
