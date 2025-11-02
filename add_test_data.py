"""
سكريبت إضافة بيانات تجريبية للنظام
"""
from app import app, db
from models import User, Role, Gender, ShiftTime, Status, LeaveType, LeaveRequest, Schedule, Attendance, SystemSettings
from datetime import datetime, timedelta
import random

def add_test_data():
    """إضافة بيانات تجريبية شاملة"""
    
    with app.app_context():
        print('╔════════════════════════════════════════════════════════════╗')
        print('║           إضافة بيانات تجريبية للنظام                    ║')
        print('╚════════════════════════════════════════════════════════════╝')
        print()
        
        # 1. إضافة مشرفين رئيسيين
        print('[1/7] إضافة المشرفين الرئيسيين...')
        supervisors = []
        
        supervisor_data = [
            {'id': '2000000001', 'name': 'أحمد محمد السالم', 'gender': Gender.MALE, 'dept': 'القرآن الكريم', 'shift': '8:00 ص - 12:00 م'},
            {'id': '2000000002', 'name': 'فاطمة عبدالله الزهراني', 'gender': Gender.FEMALE, 'dept': 'القرآن الكريم', 'shift': '9:00 ص - 1:00 م'},
            {'id': '2000000003', 'name': 'عبدالرحمن سعيد القحطاني', 'gender': Gender.MALE, 'dept': 'التجويد', 'shift': '4:00 م - 8:00 م'},
            {'id': '2000000004', 'name': 'خديجة حسن الغامدي', 'gender': Gender.FEMALE, 'dept': 'التجويد', 'shift': '5:00 م - 9:00 م'},
        ]
        
        for sup_data in supervisor_data:
            sup = User.query.filter_by(national_id=sup_data['id']).first()
            if not sup:
                sup = User(
                    national_id=sup_data['id'],
                    name=sup_data['name'],
                    role=Role.MAIN_SUPERVISOR,
                    gender=sup_data['gender'],
                    department=sup_data['dept'],
                    shift_time=sup_data['shift'],
                    is_active=True
                )
                sup.set_password('123456')
                db.session.add(sup)
                supervisors.append(sup)
                print(f'  ✅ تم إضافة: {sup.name}')
            else:
                supervisors.append(sup)
                print(f'  ✓ موجود مسبقاً: {sup.name}')
        
        db.session.commit()
        print(f'✅ تم إضافة {len(supervisors)} مشرف رئيسي\n')
        
        # 2. إضافة مشرفين فرعيين
        print('[2/7] إضافة المشرفين الفرعيين...')
        sub_supervisors = []
        
        sub_supervisor_data = [
            {'id': '3000000001', 'name': 'محمد علي الشهري', 'gender': Gender.MALE, 'dept': 'القرآن الكريم'},
            {'id': '3000000002', 'name': 'عائشة سالم البقمي', 'gender': Gender.FEMALE, 'dept': 'القرآن الكريم'},
        ]
        
        for sub_data in sub_supervisor_data:
            sub = User.query.filter_by(national_id=sub_data['id']).first()
            if not sub:
                sub = User(
                    national_id=sub_data['id'],
                    name=sub_data['name'],
                    role=Role.SUB_SUPERVISOR,
                    gender=sub_data['gender'],
                    department=sub_data['dept'],
                    is_active=True
                )
                sub.set_password('123456')
                db.session.add(sub)
                sub_supervisors.append(sub)
                print(f'  ✅ تم إضافة: {sub.name}')
            else:
                sub_supervisors.append(sub)
                print(f'  ✓ موجود مسبقاً: {sub.name}')
        
        db.session.commit()
        print(f'✅ تم إضافة {len(sub_supervisors)} مشرف فرعي\n')
        
        # 3. إضافة موظفين
        print('[3/7] إضافة الموظفين...')
        employees = []
        
        male_names = [
            'عبدالله محمد الأحمدي', 'يوسف أحمد الغامدي', 'خالد سعيد القرشي',
            'عمر فهد الحربي', 'سلمان عبدالله الدوسري', 'طارق حسن العمري',
            'إبراهيم علي الزهراني', 'ماجد فيصل السلمي', 'ناصر راشد الشهري',
            'فهد عبدالعزيز القحطاني', 'سعود محمد الشمراني', 'تركي ناصر العتيبي'
        ]
        
        female_names = [
            'نورة عبدالله السعيد', 'سارة محمد الحارثي', 'هند أحمد البقمي',
            'ريم سعيد الثقفي', 'منى فهد الزهراني', 'لينا حسن الغامدي',
            'أسماء علي القحطاني', 'شيماء عبدالرحمن السلمي', 'دعاء محمود الشهري',
            'جواهر فيصل الدوسري', 'عهود ناصر الحربي', 'بدور سلطان العمري'
        ]
        
        departments = ['القرآن الكريم', 'التجويد', 'التفسير', 'الحديث']
        
        # إضافة موظفين ذكور
        for i, name in enumerate(male_names):
            emp_id = f'4000{i+1:06d}'
            emp = User.query.filter_by(national_id=emp_id).first()
            if not emp:
                emp = User(
                    national_id=emp_id,
                    name=name,
                    role=Role.EMPLOYEE,
                    gender=Gender.MALE,
                    department=random.choice(departments),
                    is_active=True,
                    supervisor_id=supervisors[i % 2].id  # توزيع على المشرفين الذكور
                )
                emp.set_password(emp_id)
                db.session.add(emp)
                employees.append(emp)
                print(f'  ✅ تم إضافة: {name}')
        
        # إضافة موظفات إناث
        for i, name in enumerate(female_names):
            emp_id = f'5000{i+1:06d}'
            emp = User.query.filter_by(national_id=emp_id).first()
            if not emp:
                emp = User(
                    national_id=emp_id,
                    name=name,
                    role=Role.EMPLOYEE,
                    gender=Gender.FEMALE,
                    department=random.choice(departments),
                    is_active=True,
                    supervisor_id=supervisors[2 + (i % 2)].id  # توزيع على المشرفات الإناث
                )
                emp.set_password(emp_id)
                db.session.add(emp)
                employees.append(emp)
                print(f'  ✅ تم إضافة: {name}')
        
        db.session.commit()
        print(f'✅ تم إضافة {len(employees)} موظف\n')
        
        # 4. إضافة الجداول
        print('[4/7] إضافة الجداول الأسبوعية...')
        days = ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة']
        schedule_count = 0
        
        for emp in employees:
            # حذف الجداول القديمة
            Schedule.query.filter_by(employee_id=emp.id).delete()
            
            # أيام العمل (6 أيام، يوم راحة)
            rest_day = random.choice(days)
            shift_times = ['8:00 ص - 12:00 م', '12:00 م - 4:00 م', '4:00 م - 8:00 م', '5:00 م - 9:00 م']
            shift = random.choice(shift_times)
            
            for day in days:
                schedule = Schedule(
                    employee_id=emp.id,
                    day_of_week=day,
                    shift_time=shift,
                    is_rest_day=(day == rest_day),
                    start_date=datetime.now().date(),
                    created_by=emp.supervisor_id
                )
                db.session.add(schedule)
                schedule_count += 1
        
        db.session.commit()
        print(f'✅ تم إضافة {schedule_count} سجل جدول\n')
        
        # 5. إضافة طلبات الإجازات
        print('[5/7] إضافة طلبات الإجازات...')
        leave_types = LeaveType.query.all()
        leave_count = 0
        
        for emp in employees[:8]:  # أول 8 موظفين
            # طلب إجازة مقبول
            start_date = datetime.now().date() - timedelta(days=random.randint(5, 15))
            end_date = start_date + timedelta(days=random.randint(2, 5))
            days_count = (end_date - start_date).days + 1
            
            leave_req = LeaveRequest(
                employee_id=emp.id,
                leave_type_id=random.choice(leave_types).id,
                start_date=start_date,
                end_date=end_date,
                days_count=days_count,
                reason='إجازة تجريبية - مقبولة',
                status=Status.APPROVED,
                reviewed_by=emp.supervisor_id,
                reviewed_at=datetime.utcnow(),
                review_notes='تم الموافقة على الطلب'
            )
            db.session.add(leave_req)
            leave_count += 1
        
        for emp in employees[8:12]:  # التالية 4 موظفين
            # طلب إجازة قيد الانتظار
            start_date = datetime.now().date() + timedelta(days=random.randint(5, 15))
            end_date = start_date + timedelta(days=random.randint(2, 4))
            days_count = (end_date - start_date).days + 1
            
            leave_req = LeaveRequest(
                employee_id=emp.id,
                leave_type_id=random.choice(leave_types).id,
                start_date=start_date,
                end_date=end_date,
                days_count=days_count,
                reason='إجازة تجريبية - قيد الانتظار',
                status=Status.PENDING
            )
            db.session.add(leave_req)
            leave_count += 1
        
        for emp in employees[12:15]:  # التالية 3 موظفين
            # طلب إجازة مرفوض
            start_date = datetime.now().date() - timedelta(days=random.randint(20, 30))
            end_date = start_date + timedelta(days=random.randint(2, 3))
            days_count = (end_date - start_date).days + 1
            
            leave_req = LeaveRequest(
                employee_id=emp.id,
                leave_type_id=random.choice(leave_types).id,
                start_date=start_date,
                end_date=end_date,
                days_count=days_count,
                reason='إجازة تجريبية - مرفوضة',
                status=Status.REJECTED,
                reviewed_by=emp.supervisor_id,
                reviewed_at=datetime.utcnow(),
                review_notes='تم رفض الطلب لعدم توفر بديل'
            )
            db.session.add(leave_req)
            leave_count += 1
        
        db.session.commit()
        print(f'✅ تم إضافة {leave_count} طلب إجازة\n')
        
        # 6. إضافة سجلات الحضور والغياب
        print('[6/7] إضافة سجلات الحضور والغياب...')
        attendance_count = 0
        
        # آخر 30 يوم
        for day_offset in range(30):
            date = datetime.now().date() - timedelta(days=day_offset)
            
            # تخطي الجمعة
            if date.strftime('%A') == 'Friday':
                continue
            
            for emp in employees:
                # 85% حضور، 10% غياب، 5% إجازة
                rand = random.random()
                if rand < 0.85:
                    status = 'حاضر'
                elif rand < 0.95:
                    status = 'غائب'
                else:
                    status = 'إجازة'
                
                attendance = Attendance(
                    employee_id=emp.id,
                    date=date,
                    status=status,
                    notes='سجل تجريبي' if status == 'غائب' else None,
                    recorded_by=emp.supervisor_id
                )
                db.session.add(attendance)
                attendance_count += 1
        
        db.session.commit()
        print(f'✅ تم إضافة {attendance_count} سجل حضور\n')
        
        # 7. ملخص البيانات
        print('[7/7] ملخص البيانات المضافة:')
        print('─' * 60)
        print(f'  • المشرفون الرئيسيون: {len(supervisors)}')
        print(f'  • المشرفون الفرعيون: {len(sub_supervisors)}')
        print(f'  • الموظفون: {len(employees)}')
        print(f'  • الجداول: {schedule_count}')
        print(f'  • طلبات الإجازات: {leave_count}')
        print(f'  • سجلات الحضور: {attendance_count}')
        print('─' * 60)
        print()
        
        print('╔════════════════════════════════════════════════════════════╗')
        print('║              ✅ تم إضافة البيانات بنجاح                  ║')
        print('╚════════════════════════════════════════════════════════════╝')
        print()
        
        print('📌 بيانات تسجيل الدخول للاختبار:')
        print('─' * 60)
        print('  🔑 مدير النظام:')
        print('     رقم الهوية: 1000000000')
        print('     كلمة المرور: admin123')
        print()
        print('  👨‍💼 مشرف رئيسي (ذكور):')
        print('     رقم الهوية: 2000000001')
        print('     كلمة المرور: 123456')
        print()
        print('  👩‍💼 مشرفة رئيسية (إناث):')
        print('     رقم الهوية: 2000000002')
        print('     كلمة المرور: 123456')
        print()
        print('  👤 موظف (ذكر):')
        print('     رقم الهوية: 4000000001')
        print('     كلمة المرور: 4000000001')
        print()
        print('  👤 موظفة (أنثى):')
        print('     رقم الهوية: 5000000001')
        print('     كلمة المرور: 5000000001')
        print('─' * 60)

if __name__ == '__main__':
    add_test_data()
