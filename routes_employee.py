from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, Role, LeaveRequest, LeaveType, Schedule, Attendance
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

# لوحة تحكم الموظف
@employee_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != Role.EMPLOYEE:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    # إحصائيات
    total_leaves = LeaveRequest.query.filter_by(employee_id=current_user.id).count()
    pending_leaves = LeaveRequest.query.filter_by(
        employee_id=current_user.id,
        status='قيد الانتظار'
    ).count()
    
    # الحضور لهذا الشهر
    today = datetime.now().date()
    first_day = today.replace(day=1)
    attendance_count = Attendance.query.filter(
        Attendance.employee_id == current_user.id,
        Attendance.date >= first_day,
        Attendance.status == 'حاضر'
    ).count()
    
    absence_count = Attendance.query.filter(
        Attendance.employee_id == current_user.id,
        Attendance.date >= first_day,
        Attendance.status == 'غائب'
    ).count()
    
    return render_template('employee/dashboard.html',
                         total_leaves=total_leaves,
                         pending_leaves=pending_leaves,
                         attendance_count=attendance_count,
                         absence_count=absence_count)

# الاستعلام عن البيانات برقم الهوية
@employee_bp.route('/inquiry', methods=['GET', 'POST'])
def inquiry():
    if request.method == 'POST':
        national_id = request.form.get('national_id')
        user = User.query.filter_by(national_id=national_id, role=Role.EMPLOYEE).first()
        
        if not user:
            flash('لم يتم العثور على الموظف', 'warning')
            return redirect(url_for('employee.inquiry'))
        
        # جلب البيانات
        leaves = LeaveRequest.query.filter_by(employee_id=user.id).order_by(LeaveRequest.created_at.desc()).all()
        schedules = Schedule.query.filter_by(employee_id=user.id).all()
        attendance = Attendance.query.filter_by(employee_id=user.id).order_by(Attendance.date.desc()).limit(30).all()
        
        return render_template('employee/inquiry_results.html',
                             user=user,
                             leaves=leaves,
                             schedules=schedules,
                             attendance=attendance)
    
    return render_template('employee/inquiry.html')

# طلب إجازة (بدون تسجيل دخول)
@employee_bp.route('/leave-request', methods=['GET', 'POST'])
def leave_request():
    leave_types = LeaveType.query.filter_by(is_active=True).all()
    
    # التحقق من رقم الهوية في حالة POST
    if request.method == 'POST':
        national_id = request.form.get('national_id')
        if not national_id:
            flash('الرجاء إدخال رقم الهوية', 'danger')
            return redirect(url_for('employee.leave_request'))
        
        user = User.query.filter_by(national_id=national_id, role=Role.EMPLOYEE).first()
        if not user:
            flash('رقم الهوية غير صحيح', 'danger')
            return redirect(url_for('employee.leave_request'))
    
        leave_type_id = request.form.get('leave_type_id')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        reason = request.form.get('reason')
        
        # حساب عدد الأيام
        days_count = (end_date - start_date).days + 1
        
        leave_type = LeaveType.query.get(leave_type_id)
        
        # التحقق من الحد الأقصى
        current_year_leaves = LeaveRequest.query.filter(
            LeaveRequest.employee_id == user.id,
            LeaveRequest.leave_type_id == leave_type_id,
            LeaveRequest.status == 'مقبول',
            db.extract('year', LeaveRequest.start_date) == datetime.now().year
        ).all()
        
        total_days = sum([lr.days_count for lr in current_year_leaves])
        
        if total_days + days_count > leave_type.max_days:
            flash(f'تجاوزت الحد المسموح للإجازات ({leave_type.max_days} يوم). الرجاء التواصل مع الإدارة', 'danger')
            return redirect(url_for('employee.leave_request'))
        
        # إنشاء الطلب
        leave_req = LeaveRequest(
            employee_id=user.id,
            leave_type_id=leave_type_id,
            start_date=start_date,
            end_date=end_date,
            days_count=days_count,
            reason=reason
        )
        
        # رفع المرفق إذا كان مطلوباً
        if leave_type.requires_attachment and 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename:
                filename = secure_filename(f"{user.national_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                upload_folder = os.path.join('static', 'uploads', 'attachments')
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                leave_req.attachment_path = file_path
        
        db.session.add(leave_req)
        db.session.commit()
        
        flash('تم تقديم طلب الإجازة بنجاح', 'success')
        return render_template('employee/leave_request_success.html', user=user)
    
    return render_template('employee/leave_request.html', leave_types=leave_types)

# إجازاتي
@employee_bp.route('/my-leaves')
@login_required
def my_leaves():
    if current_user.role != Role.EMPLOYEE:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    leaves = LeaveRequest.query.filter_by(employee_id=current_user.id).order_by(LeaveRequest.created_at.desc()).all()
    return render_template('employee/my_leaves.html', leaves=leaves)

# جدولي
@employee_bp.route('/my-schedule')
@login_required
def my_schedule():
    if current_user.role != Role.EMPLOYEE:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    schedules = Schedule.query.filter_by(employee_id=current_user.id).all()
    return render_template('employee/my_schedule.html', schedules=schedules)

# حضوري وغيابي
@employee_bp.route('/my-attendance')
@login_required
def my_attendance():
    if current_user.role != Role.EMPLOYEE:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    # Get date range from query parameters
    month = request.args.get('month', datetime.now().month)
    year = request.args.get('year', datetime.now().year)
    
    attendance = Attendance.query.filter(
        Attendance.employee_id == current_user.id,
        db.extract('month', Attendance.date) == month,
        db.extract('year', Attendance.date) == year
    ).order_by(Attendance.date.desc()).all()
    
    return render_template('employee/my_attendance.html', attendance=attendance)
