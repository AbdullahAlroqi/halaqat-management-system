# 🚀 دليل النشر السريع

## 📦 الرفع على GitHub

### 1. تنظيف المشروع
```bash
python prepare_for_github.py
```

### 2. إنشاء مستودع على GitHub

1. اذهب إلى [github.com](https://github.com)
2. اضغط **New repository**
3. اختر اسم المستودع: `halaqat-management-system`
4. اختر **Public** أو **Private**
5. **لا تضف** README أو .gitignore (موجودان بالفعل)
6. اضغط **Create repository**

### 3. رفع المشروع

```bash
# في مجلد المشروع
git init
git add .
git commit -m "نظام إدارة معلمي الحلقات - النسخة 2.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/halaqat-management-system.git
git push -u origin main
```

### 4. التحديثات اللاحقة

```bash
git add .
git commit -m "وصف التحديث"
git push
```

---

## 🌐 النشر على PythonAnywhere

### خطوات سريعة:

#### 1. تسجيل وإعداد
- سجّل على [pythonanywhere.com](https://www.pythonanywhere.com)
- افتح **Bash Console**

#### 2. استنساخ المشروع
```bash
git clone https://github.com/YOUR_USERNAME/halaqat-management-system.git
cd halaqat-management-system
```

#### 3. إعداد البيئة
```bash
mkvirtualenv --python=/usr/bin/python3.10 halaqat-env
pip install -r requirements.txt
python setup.py
```

#### 4. إعداد Web App
- اذهب لتبويب **Web**
- **Add new web app** → **Manual configuration** → **Python 3.10**

#### 5. تكوين WSGI
في ملف WSGI:
```python
import sys
import os

project_home = '/home/YOUR_USERNAME/halaqat-management-system'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['SECRET_KEY'] = 'your-secret-key-here-change-this'
os.environ['FLASK_ENV'] = 'production'

from app import app as application
```

#### 6. البيئة الافتراضية
في **Virtualenv**: `/home/YOUR_USERNAME/.virtualenvs/halaqat-env`

#### 7. الملفات الثابتة
| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/halaqat-management-system/static/` |
| `/uploads/` | `/home/YOUR_USERNAME/halaqat-management-system/uploads/` |

#### 8. إعادة التحميل
اضغط **Reload** في تبويب Web

#### 9. الوصول
`https://YOUR_USERNAME.pythonanywhere.com`

---

## ✅ قائمة التحقق قبل النشر

### الأمان:
- [ ] تغيير SECRET_KEY في الإنتاج
- [ ] تغيير كلمة مرور المدير (1000000000 / admin123)
- [ ] مراجعة .gitignore
- [ ] إزالة أي بيانات تجريبية حساسة
- [ ] تعطيل DEBUG mode

### الملفات:
- [ ] تحديث README.md
- [ ] إضافة LICENSE
- [ ] إنشاء .env.example
- [ ] التأكد من requirements.txt محدث

### قاعدة البيانات:
- [ ] نسخة احتياطية من البيانات
- [ ] اختبار الترحيل على بيئة تجريبية
- [ ] التأكد من صلاحيات الملفات

### الاختبار:
- [ ] اختبار تسجيل الدخول
- [ ] اختبار جميع الأدوار (مدير، مشرف، موظف)
- [ ] اختبار رفع الملفات
- [ ] اختبار الشهادات
- [ ] اختبار رصيد الإجازات

---

## 🔄 سير العمل الموصى به

### التطوير المحلي:
```bash
git checkout -b feature/new-feature
# طور الميزة
git add .
git commit -m "إضافة ميزة جديدة"
git push origin feature/new-feature
```

### على GitHub:
- أنشئ Pull Request
- راجع التغييرات
- ادمج في main

### التحديث على PythonAnywhere:
```bash
cd ~/halaqat-management-system
git pull origin main
# إعادة تحميل من تبويب Web
```

---

## 📞 حل المشاكل

### GitHub

**مشكلة:** `permission denied`
```bash
# استخدم HTTPS أو أضف SSH key
git remote set-url origin https://github.com/YOUR_USERNAME/repo.git
```

**مشكلة:** ملفات كبيرة
```bash
# استخدم Git LFS
git lfs install
git lfs track "*.db"
```

### PythonAnywhere

**مشكلة:** خطأ 500
```bash
# راجع سجل الأخطاء
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

**مشكلة:** قاعدة البيانات
```bash
# تحقق من الصلاحيات
chmod 644 halaqat.db
```

---

## 📚 موارد إضافية

- [توثيق Git](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)

---

## 🎉 تهانينا!

مشروعك الآن على GitHub و PythonAnywhere!

**GitHub:** `https://github.com/YOUR_USERNAME/halaqat-management-system`  
**Live:** `https://YOUR_USERNAME.pythonanywhere.com`

---

**آخر تحديث:** 2025-01-06
