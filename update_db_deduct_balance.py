"""
سكريبت تحديث قاعدة البيانات - إضافة حقل deduct_from_balance
"""
import sqlite3
import os

def update_database():
    """تحديث قاعدة البيانات"""
    
    db_path = 'halaqat.db'
    
    if not os.path.exists(db_path):
        print("⚠️ قاعدة البيانات غير موجودة!")
        print("الرجاء تشغيل التطبيق أولاً لإنشاء قاعدة البيانات.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("="*60)
        print("جاري تحديث قاعدة البيانات...")
        print("="*60)
        
        # التحقق من وجود عمود deduct_from_balance
        cursor.execute("PRAGMA table_info(leave_types)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'deduct_from_balance' not in columns:
            print("\n✓ إضافة عمود deduct_from_balance إلى جدول leave_types...")
            cursor.execute("ALTER TABLE leave_types ADD COLUMN deduct_from_balance BOOLEAN DEFAULT 1")
            
            # تحديث أنواع الإجازات الموجودة
            # الإجازات المرضية والوطنية لا تخصم
            print("✓ تحديث أنواع الإجازات الموجودة...")
            cursor.execute("UPDATE leave_types SET deduct_from_balance = 0 WHERE name IN ('إجازة مرضية', 'إجازة وطنية', 'الإجازات الوطنية', 'مرضية', 'وطنية')")
            
            conn.commit()
            print("✓ تم إضافة عمود deduct_from_balance بنجاح")
        else:
            print("\n✓ عمود deduct_from_balance موجود مسبقاً")
        
        conn.close()
        
        print("\n" + "="*60)
        print("✅ تم تحديث قاعدة البيانات بنجاح!")
        print("="*60)
        print("\nالآن:")
        print("  • الإجازات العادية تخصم من الرصيد تلقائياً")
        print("  • الإجازات المرضية والوطنية لا تخصم من الرصيد")
        print("  • يمكنك تخصيص ذلك من صفحة أنواع الإجازات")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ أثناء التحديث: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    success = update_database()
    sys.exit(0 if success else 1)
