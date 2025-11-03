#!/usr/bin/env python3
"""
سكريبت لتحديث قاعدة البيانات لإضافة حقول جدول الحلقات
"""

from app import app, db
from models import User
from sqlalchemy import text

with app.app_context():
    try:
        # التحقق من وجود الأعمدة الجديدة
        with db.engine.connect() as conn:
            # محاولة قراءة الأعمدة
            result = conn.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result]
            
            print("🔍 فحص الأعمدة الموجودة...")
            print(f"   الأعمدة الحالية: {columns}")
            print()
            
            # إضافة الأعمدة الجديدة إذا لم تكن موجودة
            new_columns = {
                'period': 'VARCHAR(50)',
                'work_time': 'VARCHAR(50)',
                'rest_days': 'VARCHAR(100)'
            }
            
            for column_name, column_type in new_columns.items():
                if column_name not in columns:
                    print(f"➕ إضافة عمود: {column_name}")
                    conn.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"))
                    conn.commit()
                    print(f"   ✅ تمت إضافة {column_name}")
                else:
                    print(f"   ✅ {column_name} موجود بالفعل")
            
            print()
            print("✅ تم تحديث قاعدة البيانات بنجاح!")
            print()
            print("📋 يمكنك الآن:")
            print("   1. رفع ملف Excel من: الإدارة → جدول الحلقات → رفع ملف Excel")
            print("   2. عرض جدول الحلقات من: الإدارة → جدول الحلقات")
            print()
            
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        import traceback
        traceback.print_exc()
