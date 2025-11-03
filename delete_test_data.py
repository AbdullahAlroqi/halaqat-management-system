"""
سكريبت حذف البيانات التجريبية من النظام
"""
from app import app, db
from models import User, Role, LeaveRequest, Schedule, Attendance

def delete_test_data():
    """حذف البيانات التجريبية"""
    
    with app.app_context():
        print('╔════════════════════════════════════════════════════════════╗')
        print('║              ⚠️ حذف البيانات التجريبية                  ║')
        print('╚════════════════════════════════════════════════════════════╝')
        print()
        
        confirm = input('⚠️  هل أنت متأكد من حذف جميع البيانات التجريبية؟ (yes/no): ')
        
        if confirm.lower() != 'yes':
            print('❌ تم إلغاء العملية')
            return
        
        print()
        print('جاري حذف البيانات...')
        print()
        
        # 1. حذف سجلات الحضور التجريبية
        print('[1/4] حذف سجلات الحضور...')
        attendance_count = Attendance.query.filter(Attendance.notes == 'سجل تجريبي').delete()
        # حذف جميع سجلات الحضور للموظفين التجريبيين
        test_employees = User.query.filter(
            User.national_id.like('4000%') | User.national_id.like('5000%')
        ).all()
        for emp in test_employees:
            Attendance.query.filter_by(employee_id=emp.id).delete()
        db.session.commit()
        print(f'  ✅ تم حذف سجلات الحضور')
        
        # 2. حذف طلبات الإجازات التجريبية
        print('[2/4] حذف طلبات الإجازات...')
        for emp in test_employees:
            LeaveRequest.query.filter_by(employee_id=emp.id).delete()
        db.session.commit()
        print(f'  ✅ تم حذف طلبات الإجازات')
        
        # 3. حذف الجداول التجريبية
        print('[3/4] حذف الجداول...')
        for emp in test_employees:
            Schedule.query.filter_by(employee_id=emp.id).delete()
        db.session.commit()
        print(f'  ✅ تم حذف الجداول')
        
        # 4. حذف المستخدمين التجريبيين
        print('[4/4] حذف المستخدمين...')
        
        # حذف الموظفين التجريبيين
        employees_deleted = User.query.filter(
            User.national_id.like('4000%') | User.national_id.like('5000%')
        ).delete(synchronize_session=False)
        
        # حذف المشرفين التجريبيين
        supervisors_deleted = User.query.filter(
            User.national_id.like('2000%') | User.national_id.like('3000%')
        ).delete(synchronize_session=False)
        
        db.session.commit()
        print(f'  ✅ تم حذف {employees_deleted} موظف')
        print(f'  ✅ تم حذف {supervisors_deleted} مشرف')
        
        print()
        print('╔════════════════════════════════════════════════════════════╗')
        print('║            ✅ تم حذف البيانات التجريبية بنجاح            ║')
        print('╚════════════════════════════════════════════════════════════╝')
        print()
        print('ℹ️  تم الاحتفاظ بـ:')
        print('  • مدير النظام الأساسي')
        print('  • أنواع الإجازات الافتراضية')
        print('  • إعدادات النظام')
        print()

if __name__ == '__main__':
    delete_test_data()
