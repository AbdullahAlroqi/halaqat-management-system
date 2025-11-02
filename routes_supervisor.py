from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, Role, LeaveRequest, Schedule, Attendance, Notification
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

supervisor_bp = Blueprint('supervisor', __name__, url_prefix='/supervisor')

# لوحة تحكم المشرف
@supervisor_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role not in [Role.MAIN_SUPERVISOR, Role.SUB_SUPERVISOR]:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    # جلب الموظفين التابعين
    subordinates = User.query.filter_by(supervisor_id=current_user.id, role=Role.EMPLOYEE).all()
    
    # إحصائيات
    total_employees = len(subordinates)
    pending_leaves = LeaveRequest.query.join(User, LeaveRequest.employee_id == User.id).filter(
        User.supervisor_id == current_user.id,
        LeaveRequest.status == 'قيد الانتظار'
    ).count()
    
    # الحضور اليوم
    today = datetime.now().date()
    present_today = Attendance.query.join(User, Attendance.employee_id == User.id).filter(
        User.supervisor_id == current_user.id,
        Attendance.date == today,
        Attendance.status == 'حاضر'
    ).count()
    
    absent_today = Attendance.query.join(User, Attendance.employee_id == User.id).filter(
        User.supervisor_id == current_user.id,
        Attendance.date == today,
        Attendance.status == 'غائب'
    ).count()
    
    return render_template('supervisor/dashboard.html',
                         subordinates=subordinates,
                         total_employees=total_employees,
                         pending_leaves=pending_leaves,
                         present_today=present_today,
                         absent_today=absent_today)

# رفع الجداول
@supervisor_bp.route('/schedules', methods=['GET', 'POST'])
@login_required
def schedules():
    if current_user.role != Role.MAIN_SUPERVISOR:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    subordinates = User.query.filter_by(supervisor_id=current_user.id, role=Role.EMPLOYEE).all()
    
    if request.method == 'POST':
        # معالجة إضافة جداول متعددة
        employees_data = request.form.getlist('employee_id')
        
        for emp_id in employees_data:
            if not emp_id:
                continue
                
            employee_id = int(emp_id)
            days = request.form.getlist(f'days_{emp_id}')
            shift_start = request.form.get(f'shift_start_{emp_id}')
            shift_end = request.form.get(f'shift_end_{emp_id}')
            shift_time = f"{shift_start} - {shift_end}"
            start_date = datetime.strptime(request.form.get(f'start_date_{emp_id}'), '%Y-%m-%d').date()
            end_date_str = request.form.get(f'end_date_{emp_id}')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
            
            # حذف الجداول القديمة
            Schedule.query.filter_by(employee_id=employee_id).delete()
            
            # إضافة الأيام
            all_days = ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة']
            
            for day in all_days:
                schedule = Schedule(
                    employee_id=employee_id,
                    day_of_week=day,
                    shift_time=shift_time,
                    is_rest_day=(day not in days),
                    start_date=start_date,
                    end_date=end_date,
                    created_by=current_user.id
                )
                db.session.add(schedule)
        
        db.session.commit()
        flash('تم رفع الجداول بنجاح', 'success')
        return redirect(url_for('supervisor.schedules'))
    
    return render_template('supervisor/schedules.html', subordinates=subordinates)

# عرض جميع الجداول
@supervisor_bp.route('/view-schedules')
@login_required
def view_schedules():
    if current_user.role != Role.MAIN_SUPERVISOR:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    subordinates = User.query.filter_by(supervisor_id=current_user.id, role=Role.EMPLOYEE).all()
    
    # جلب جداول جميع الموظفين
    schedules_data = []
    for emp in subordinates:
        emp_schedules = Schedule.query.filter_by(employee_id=emp.id).all()
        if emp_schedules:
            schedules_data.append({
                'employee': emp,
                'schedules': emp_schedules
            })
    
    return render_template('supervisor/view_schedules.html', schedules_data=schedules_data)

# نسخ الجدول لشهر قادم
@supervisor_bp.route('/copy-schedule/<int:employee_id>', methods=['POST'])
@login_required
def copy_schedule(employee_id):
    if current_user.role != Role.MAIN_SUPERVISOR:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    # التحقق من أن الموظف تابع لهذا المشرف
    employee = User.query.get_or_404(employee_id)
    if employee.supervisor_id != current_user.id:
        flash('ليس لديك صلاحية لإدارة هذا الموظف', 'danger')
        return redirect(url_for('supervisor.view_schedules'))
    
    # جلب الجداول الحالية
    current_schedules = Schedule.query.filter_by(employee_id=employee_id).all()
    
    if not current_schedules:
        flash('لا يوجد جدول لنسخه', 'warning')
        return redirect(url_for('supervisor.view_schedules'))
    
    # نسخ الجداول للشهر القادم
    copied_count = 0
    for schedule in current_schedules:
        # حساب التاريخ للشهر القادم
        new_start_date = schedule.start_date + relativedelta(months=1) if schedule.start_date else None
        new_end_date = schedule.end_date + relativedelta(months=1) if schedule.end_date else None
        
        # إنشاء جدول جديد
        new_schedule = Schedule(
            employee_id=schedule.employee_id,
            day_of_week=schedule.day_of_week,
            shift_time=schedule.shift_time,
            is_rest_day=schedule.is_rest_day,
            start_date=new_start_date,
            end_date=new_end_date,
            created_by=current_user.id
        )
        db.session.add(new_schedule)
        copied_count += 1
    
    db.session.commit()
    flash(f'تم نسخ {copied_count} جدول للشهر القادم بنجاح', 'success')
    return redirect(url_for('supervisor.view_schedules'))

# طلبات الإجازات
@supervisor_bp.route('/leave-requests')
@login_required
def leave_requests():
    if current_user.role != Role.MAIN_SUPERVISOR:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    # جلب طلبات الإجازات للموظفين التابعين
    requests = LeaveRequest.query.join(User, LeaveRequest.employee_id == User.id).filter(
        User.supervisor_id == current_user.id
    ).order_by(LeaveRequest.created_at.desc()).all()
    
    return render_template('supervisor/leave_requests.html', requests=requests)

# الموافقة أو الرفض على الإجازة
@supervisor_bp.route('/leave-request/<int:request_id>/review', methods=['POST'])
@login_required
def review_leave_request(request_id):
    if current_user.role != Role.MAIN_SUPERVISOR:
        return jsonify({'success': False, 'message': 'ليس لديك صلاحية'}), 403
    
    leave_request = LeaveRequest.query.get_or_404(request_id)
    
    # التحقق من أن الموظف تابع لهذا المشرف
    if leave_request.employee.supervisor_id != current_user.id:
        return jsonify({'success': False, 'message': 'ليس لديك صلاحية على هذا الطلب'}), 403
    
    action = request.form.get('action')
    notes = request.form.get('notes', '')
    
    if action == 'approve':
        leave_request.status = 'مقبول'
        message = f'تم قبول طلب إجازتك من {leave_request.start_date} إلى {leave_request.end_date}'
    elif action == 'reject':
        leave_request.status = 'مرفوض'
        message = f'تم رفض طلب إجازتك من {leave_request.start_date} إلى {leave_request.end_date}'
    else:
        return jsonify({'success': False, 'message': 'إجراء غير صحيح'}), 400
    
    leave_request.reviewed_by = current_user.id
    leave_request.reviewed_at = datetime.utcnow()
    leave_request.review_notes = notes
    
    # إنشاء تنبيه للموظف
    notification = Notification(
        user_id=leave_request.employee_id,
        title='تحديث على طلب الإجازة',
        message=message,
        related_type='leave_request',
        related_id=leave_request.id
    )
    
    db.session.add(notification)
    db.session.commit()
    
    flash(f'تم {"قبول" if action == "approve" else "رفض"} الطلب بنجاح', 'success')
    return redirect(url_for('supervisor.leave_requests'))

# تسجيل الحضور والغياب
@supervisor_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    if current_user.role not in [Role.MAIN_SUPERVISOR, Role.SUB_SUPERVISOR]:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    subordinates = User.query.filter_by(supervisor_id=current_user.id, role=Role.EMPLOYEE).all()
    
    if request.method == 'POST':
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        
        for emp in subordinates:
            status = request.form.get(f'status_{emp.id}')
            notes = request.form.get(f'notes_{emp.id}', '')
            
            if not status:
                continue
            
            # التحقق من وجود سجل حضور لهذا اليوم
            existing = Attendance.query.filter_by(employee_id=emp.id, date=date).first()
            
            if existing:
                existing.status = status
                existing.notes = notes
                existing.recorded_by = current_user.id
            else:
                attendance_record = Attendance(
                    employee_id=emp.id,
                    date=date,
                    status=status,
                    notes=notes,
                    recorded_by=current_user.id
                )
                db.session.add(attendance_record)
        
        db.session.commit()
        flash('تم تسجيل الحضور والغياب بنجاح', 'success')
        return redirect(url_for('supervisor.attendance'))
    
    # جلب سجلات اليوم
    today = datetime.now().date()
    today_attendance = {}
    for emp in subordinates:
        record = Attendance.query.filter_by(employee_id=emp.id, date=today).first()
        today_attendance[emp.id] = record
    
    return render_template('supervisor/attendance.html', 
                         subordinates=subordinates,
                         today_attendance=today_attendance,
                         today=today)

# عرض سجل الحضور
@supervisor_bp.route('/attendance-records')
@login_required
def attendance_records():
    if current_user.role not in [Role.MAIN_SUPERVISOR, Role.SUB_SUPERVISOR]:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    # الحصول على معاملات البحث
    employee_id = request.args.get('employee_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # بناء الاستعلام
    query = Attendance.query.join(User, Attendance.employee_id == User.id).filter(User.supervisor_id == current_user.id)
    
    if employee_id:
        query = query.filter(Attendance.employee_id == employee_id)
    
    if start_date:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        query = query.filter(Attendance.date >= start)
    
    if end_date:
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        query = query.filter(Attendance.date <= end)
    
    records = query.order_by(Attendance.date.desc()).all()
    subordinates = User.query.filter_by(supervisor_id=current_user.id, role=Role.EMPLOYEE).all()
    
    return render_template('supervisor/attendance_records.html', 
                         records=records,
                         subordinates=subordinates)

# إضافة مشرف فرعي (للمشرف الرئيسي فقط)
@supervisor_bp.route('/add-sub-supervisor', methods=['GET', 'POST'])
@login_required
def add_sub_supervisor():
    if current_user.role != Role.MAIN_SUPERVISOR:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        national_id = request.form.get('national_id')
        name = request.form.get('name')
        password = request.form.get('password')
        gender = request.form.get('gender')
        department = request.form.get('department')
        shift_start = request.form.get('shift_start')
        shift_end = request.form.get('shift_end')
        shift_time = f"{shift_start} - {shift_end}" if shift_start and shift_end else None
        
        # التحقق من عدم وجود الهوية
        existing = User.query.filter_by(national_id=national_id).first()
        if existing:
            flash('رقم الهوية موجود مسبقاً', 'danger')
            return redirect(url_for('supervisor.add_sub_supervisor'))
        
        # إنشاء المشرف الفرعي
        sub_supervisor = User(
            national_id=national_id,
            name=name,
            role=Role.SUB_SUPERVISOR,
            gender=gender,
            department=department,
            shift_time=shift_time,
            supervisor_id=current_user.id  # ربطه بالمشرف الرئيسي
        )
        sub_supervisor.set_password(password)
        
        db.session.add(sub_supervisor)
        db.session.commit()
        
        flash('تم إضافة المشرف الفرعي بنجاح', 'success')
        return redirect(url_for('supervisor.sub_supervisors'))
    
    return render_template('supervisor/add_sub_supervisor.html')

# عرض المشرفين الفرعيين
@supervisor_bp.route('/sub-supervisors')
@login_required
def sub_supervisors():
    if current_user.role != Role.MAIN_SUPERVISOR:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    # جلب المشرفين الفرعيين التابعين للمشرف الرئيسي
    subs = User.query.filter_by(supervisor_id=current_user.id, role=Role.SUB_SUPERVISOR).all()
    
    return render_template('supervisor/sub_supervisors.html', supervisors=subs)

# إسناد المعلمين للمشرفين الفرعيين
@supervisor_bp.route('/assign-to-subs', methods=['GET', 'POST'])
@login_required
def assign_to_subs():
    if current_user.role != Role.MAIN_SUPERVISOR:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    # جلب المشرفين الفرعيين
    sub_supervisors = User.query.filter_by(supervisor_id=current_user.id, role=Role.SUB_SUPERVISOR).all()
    
    # جلب الموظفين التابعين للمشرف الرئيسي فقط
    employees = User.query.filter_by(supervisor_id=current_user.id, role=Role.EMPLOYEE).all()
    
    if request.method == 'POST':
        sub_supervisor_id = request.form.get('supervisor_id')
        employee_ids = request.form.getlist('employee_ids')
        
        if not sub_supervisor_id:
            flash('الرجاء اختيار المشرف الفرعي', 'danger')
            return redirect(url_for('supervisor.assign_to_subs'))
        
        # التحقق أن المشرف الفرعي تابع للمشرف الرئيسي
        sub_supervisor = User.query.get(sub_supervisor_id)
        if not sub_supervisor or sub_supervisor.supervisor_id != current_user.id:
            flash('المشرف الفرعي غير صحيح', 'danger')
            return redirect(url_for('supervisor.assign_to_subs'))
        
        # إسناد الموظفين
        for emp_id in employee_ids:
            employee = User.query.get(int(emp_id))
            if employee and employee.supervisor_id == current_user.id:
                employee.supervisor_id = int(sub_supervisor_id)
        
        db.session.commit()
        flash(f'تم إسناد {len(employee_ids)} موظف للمشرف الفرعي', 'success')
        return redirect(url_for('supervisor.assign_to_subs'))
    
    return render_template('supervisor/assign_to_subs.html', 
                          sub_supervisors=sub_supervisors,
                          employees=employees)
