#!/usr/bin/env python3
"""
سكريبت لإصلاح الإشعارات التي لها user_id = None
"""

from app import app, db
from models import Notification

with app.app_context():
    try:
        # حذف الإشعارات التي user_id فيها None
        deleted_count = Notification.query.filter_by(user_id=None).delete()
        
        db.session.commit()
        
        print(f"✅ تم حذف {deleted_count} إشعار غير صالح")
        print()
        
        # عرض عدد الإشعارات المتبقية
        remaining = Notification.query.count()
        print(f"📊 الإشعارات المتبقية: {remaining}")
        print()
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ خطأ: {str(e)}")
        import traceback
        traceback.print_exc()
