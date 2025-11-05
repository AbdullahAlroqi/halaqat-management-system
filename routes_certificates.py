from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Certificate, User, Role
from datetime import datetime

cert_bp = Blueprint('certificates', __name__, url_prefix='/certificates')

# إدارة الشهادات للمشرف الفرعي
@cert_bp.route('/manage')
@login_required
def manage_certificates():
    if current_user.role != Role.SUB_SUPERVISOR:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    # جلب الشهادات التي أنشأها المشرف الحالي
    certificates = Certificate.query.filter_by(created_by=current_user.id).order_by(Certificate.created_at.desc()).all()
    return render_template('supervisor/manage_certificates.html', certificates=certificates)

# إضافة شهادة جديدة
@cert_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_certificate():
    if current_user.role != Role.SUB_SUPERVISOR:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            expected_date = datetime.strptime(request.form.get('expected_completion_date'), '%Y-%m-%d').date()
            
            certificate = Certificate(
                student_name=request.form.get('student_name'),
                nationality=request.form.get('nationality'),
                phone=request.form.get('phone'),
                expected_completion_date=expected_date,
                narration_type=request.form.get('narration_type'),
                halaqah=request.form.get('halaqah'),
                completion_type=request.form.get('completion_type'),
                teacher_name=request.form.get('teacher_name'),
                notes=request.form.get('notes'),
                created_by=current_user.id
            )
            
            db.session.add(certificate)
            db.session.commit()
            
            flash('تمت إضافة الشهادة بنجاح', 'success')
            return redirect(url_for('certificates.manage_certificates'))
            
        except Exception as e:
            db.session.rollback()
            flash('حدث خطأ أثناء إضافة الشهادة', 'danger')
    
    return render_template('supervisor/add_certificate.html')

# تعديل شهادة
@cert_bp.route('/edit/<int:cert_id>', methods=['GET', 'POST'])
@login_required
def edit_certificate(cert_id):
    certificate = Certificate.query.get_or_404(cert_id)
    
    # التحقق من الصلاحيات
    if current_user.role != Role.SUB_SUPERVISOR or certificate.created_by != current_user.id:
        flash('ليس لديك صلاحية لتعديل هذه الشهادة', 'danger')
        return redirect(url_for('index'))
    
    # التحقق من أن وقت التعديل لم يتجاوز 24 ساعة
    time_since_creation = datetime.utcnow() - certificate.created_at
    if time_since_creation.total_seconds() > 24 * 60 * 60:  # 24 ساعة بالثواني
        flash('لا يمكن التعديل بعد مرور 24 ساعة على إنشاء الشهادة', 'danger')
        return redirect(url_for('certificates.manage_certificates'))
    
    if request.method == 'POST':
        try:
            certificate.student_name = request.form.get('student_name', certificate.student_name)
            certificate.nationality = request.form.get('nationality', certificate.nationality)
            certificate.phone = request.form.get('phone', certificate.phone)
            certificate.expected_completion_date = datetime.strptime(
                request.form.get('expected_completion_date'), '%Y-%m-%d'
            ).date()
            certificate.narration_type = request.form.get('narration_type', certificate.narration_type)
            certificate.halaqah = request.form.get('halaqah', certificate.halaqah)
            certificate.completion_type = request.form.get('completion_type', certificate.completion_type)
            certificate.teacher_name = request.form.get('teacher_name', certificate.teacher_name)
            certificate.notes = request.form.get('notes', certificate.notes)
            certificate.updated_by = current_user.id
            
            db.session.commit()
            flash('تم تحديث الشهادة بنجاح', 'success')
            return redirect(url_for('certificates.manage_certificates'))
            
        except Exception as e:
            db.session.rollback()
            flash('حدث خطأ أثناء تحديث الشهادة', 'danger')
    
    # تحويل التاريخ إلى تنسيق YYYY-MM-DD لعرضه في حقل التاريخ
    formatted_date = certificate.expected_completion_date.strftime('%Y-%m-%d')
    return render_template('supervisor/edit_certificate.html', 
                         certificate=certificate,
                         formatted_date=formatted_date)

# حذف شهادة (للمشرف الفرعي)
@cert_bp.route('/delete/<int:cert_id>', methods=['POST'])
@login_required
def delete_certificate(cert_id):
    certificate = Certificate.query.get_or_404(cert_id)
    
    # التحقق من الصلاحيات
    if current_user.role != Role.SUB_SUPERVISOR or certificate.created_by != current_user.id:
        return jsonify({'success': False, 'message': 'ليس لديك صلاحية لحذف هذه الشهادة'}), 403
    
    # التحقق من أن وقت الحذف لم يتجاوز 24 ساعة
    time_since_creation = datetime.utcnow() - certificate.created_at
    if time_since_creation.total_seconds() > 24 * 60 * 60:  # 24 ساعة بالثواني
        return jsonify({'success': False, 'message': 'لا يمكن الحذف بعد مرور 24 ساعة على إنشاء الشهادة'}), 403
    
    try:
        db.session.delete(certificate)
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم حذف الشهادة بنجاح'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء حذف الشهادة'}), 500

# إدارة الشهادات للمدير
@cert_bp.route('/admin/manage')
@login_required
def admin_manage():
    if current_user.role not in [Role.MAIN_ADMIN, Role.SUB_ADMIN]:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    # جلب جميع الشهادات مرتبة حسب تاريخ الإنشاء
    certificates = Certificate.query.order_by(Certificate.created_at.desc()).all()
    return render_template('admin/manage_certificates.html', certificates=certificates)

# تحديث حالة الشهادة (للمدير)
@cert_bp.route('/admin/update_status/<int:cert_id>', methods=['POST'])
@login_required
def update_certificate_status(cert_id):
    if current_user.role not in [Role.MAIN_ADMIN, Role.SUB_ADMIN]:
        return jsonify({'success': False, 'message': 'غير مصرح'}), 403
    
    certificate = Certificate.query.get_or_404(cert_id)
    new_status = request.json.get('status')
    
    if new_status not in ['جاري العمل', 'تمت']:
        return jsonify({'success': False, 'message': 'حالة غير صالحة'}), 400
    
    try:
        certificate.status = new_status
        certificate.updated_by = current_user.id
        certificate.updated_at = datetime.utcnow()
        
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'تم تحديث الحالة بنجاح',
            'new_status': new_status
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء تحديث الحالة'}), 500

# حذف شهادة (للمدير)
@cert_bp.route('/admin/delete/<int:cert_id>', methods=['POST'])
@login_required
def admin_delete_certificate(cert_id):
    if current_user.role not in [Role.MAIN_ADMIN, Role.SUB_ADMIN]:
        return jsonify({'success': False, 'message': 'غير مصرح'}), 403
    
    certificate = Certificate.query.get_or_404(cert_id)
    
    try:
        db.session.delete(certificate)
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم حذف الشهادة بنجاح'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء حذف الشهادة'}), 500

# إضافة شهادة للمدير
@cert_bp.route('/admin/add', methods=['GET', 'POST'])
@login_required
def admin_add_certificate():
    if current_user.role not in [Role.MAIN_ADMIN, Role.SUB_ADMIN]:
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            expected_date = datetime.strptime(request.form.get('expected_completion_date'), '%Y-%m-%d').date()
            
            certificate = Certificate(
                student_name=request.form.get('student_name'),
                nationality=request.form.get('nationality'),
                phone=request.form.get('phone'),
                expected_completion_date=expected_date,
                narration_type=request.form.get('narration_type'),
                halaqah=request.form.get('halaqah'),
                completion_type=request.form.get('completion_type'),
                teacher_name=request.form.get('teacher_name'),
                notes=request.form.get('notes'),
                created_by=current_user.id
            )
            
            db.session.add(certificate)
            db.session.commit()
            
            flash('تمت إضافة الشهادة بنجاح', 'success')
            return redirect(url_for('certificates.admin_manage'))
            
        except Exception as e:
            db.session.rollback()
            flash('حدث خطأ أثناء إضافة الشهادة', 'danger')
    
    return render_template('admin/add_certificate.html')
