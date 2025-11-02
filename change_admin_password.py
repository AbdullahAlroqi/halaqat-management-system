#!/usr/bin/env python3
"""
سكريبت لتغيير كلمة سر مدير النظام الأساسي
"""

from app import app, db
from models import User

# كلمة السر الجديدة (غيّر هنا)
NEW_PASSWORD = "Abdullah@1234"  # ⬅️ غيّر هذه الكلمة

with app.app_context():
    try:
        # البحث عن المدير
        admin = User.query.filter_by(national_id='1000000000').first()
        
        if admin:
            # تغيير كلمة السر
            admin.set_password(NEW_PASSWORD)
            db.session.commit()
            
            print("✅ تم تغيير كلمة السر بنجاح!")
            print(f"   رقم الهوية: {admin.national_id}")
            print(f"   الاسم: {admin.name}")
            print(f"   كلمة السر الجديدة: {NEW_PASSWORD}")
            print()
            print("💡 تسجيل الدخول:")
            print(f"   الهوية: {admin.national_id}")
            print(f"   كلمة السر: {NEW_PASSWORD}")
        else:
            print("❌ لم يتم العثور على مدير النظام")
            print("💡 تأكد من رقم الهوية في السكريبت")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ خطأ: {str(e)}")
        import traceback
        traceback.print_exc()
