# 🌐 دليل النشر على PythonAnywhere

دليل شامل لنشر نظام إدارة معلمي الحلقات على PythonAnywhere.

## 📋 المتطلبات

1. حساب على [PythonAnywhere](https://www.pythonanywhere.com)
   - حساب مجاني يكفي للبداية
   - للمشاريع الكبيرة، يُنصح بالحساب المدفوع

2. مشروع مرفوع على GitHub

## 🚀 خطوات النشر

### 1. إنشاء حساب والدخول

1. اذهب إلى [pythonanywhere.com](https://www.pythonanywhere.com)
2. سجّل حساب جديد أو سجّل دخول
3. اختر Python 3.10 أو أحدث

### 2. استنساخ المشروع من GitHub

افتح Bash Console من لوحة التحكم:

```bash
# استنساخ المشروع
git clone https://github.com/YOUR_USERNAME/halaqat-management-system.git
cd halaqat-management-system

# إنشاء بيئة افتراضية
mkvirtualenv --python=/usr/bin/python3.10 halaqat-env

# تثبيت المتطلبات
pip install -r requirements.txt
```

### 3. إعداد قاعدة البيانات

```bash
# تهيئة قاعدة البيانات
python setup.py

# أو إذا كانت لديك قاعدة بيانات موجودة
python migrate_db.py
```

### 4. إنشاء Web App

من لوحة التحكم:

1. اذهب إلى تبويب **Web**
2. اضغط **Add a new web app**
3. اختر **Manual configuration**
4. اختر **Python 3.10**

### 5. تكوين WSGI

اضغط على ملف WSGI configuration واستبدل المحتوى بـ:

```python
# +++++++++++ FLASK +++++++++++
import sys
import os

# إضافة مسار المشروع
project_home = '/home/YOUR_USERNAME/halaqat-management-system'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# إعداد متغيرات البيئة
os.environ['SECRET_KEY'] = 'your-super-secret-key-change-this-now-12345'
os.environ['FLASK_ENV'] = 'production'

# استيراد التطبيق
from app import app as application
```

> **⚠️ مهم:** غيّر `YOUR_USERNAME` و `SECRET_KEY`

### 6. إعداد البيئة الافتراضية

في صفحة Web configuration:

1. اذهب إلى قسم **Virtualenv**
2. أدخل: `/home/YOUR_USERNAME/.virtualenvs/halaqat-env`
3. احفظ

### 7. إعداد الملفات الثابتة

في قسم **Static files**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/halaqat-management-system/static/` |
| `/uploads/` | `/home/YOUR_USERNAME/halaqat-management-system/uploads/` |

### 8. الصلاحيات

```bash
# تأكد من صلاحيات المجلدات
cd ~/halaqat-management-system
chmod -R 755 static/
chmod -R 755 uploads/
chmod 644 halaqat.db  # إذا كانت قاعدة البيانات موجودة
```

### 9. إعادة تحميل التطبيق

1. اذهب إلى تبويب **Web**
2. اضغط الزر الأخضر **Reload YOUR_USERNAME.pythonanywhere.com**

### 10. اختبار التطبيق

افتح `https://YOUR_USERNAME.pythonanywhere.com` في المتصفح.

## 🔧 الإعدادات المتقدمة

### تعيين متغيرات البيئة

في ملف WSGI أضف:

```python
os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['SYSTEM_NAME'] = 'نظام إدارة الحلقات'
```

### استخدام MySQL بدلاً من SQLite

1. أنشئ قاعدة بيانات MySQL من لوحة التحكم
2. في ملف WSGI:

```python
os.environ['DATABASE_URL'] = 'mysql://username:password@username.mysql.pythonanywhere-services.com/dbname'
```

3. ثبّت mysqlclient:

```bash
pip install mysqlclient
```

### النسخ الاحتياطي التلقائي

أنشئ سكريبت `backup.py`:

```python
import shutil
from datetime import datetime

# نسخ قاعدة البيانات
backup_name = f"backups/halaqat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
shutil.copy('halaqat.db', backup_name)
```

ثم أضف Scheduled task من لوحة التحكم:

```bash
/home/YOUR_USERNAME/.virtualenvs/halaqat-env/bin/python /home/YOUR_USERNAME/halaqat-management-system/backup.py
```

## 🔄 التحديثات

لتحديث التطبيق بعد رفع تغييرات على GitHub:

```bash
# في Bash Console
cd ~/halaqat-management-system
git pull origin main

# إعادة تحميل التطبيق من تبويب Web
```

## 📊 المراقبة

### سجلات الأخطاء

- اذهب إلى **Web** → **Log files**
- راجع `error.log` و `server.log`

### حل المشاكل

#### خطأ 500 - Internal Server Error

```bash
# تحقق من سجل الأخطاء
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log

# تأكد من تثبيت المتطلبات
pip install -r requirements.txt --upgrade
```

#### خطأ في قاعدة البيانات

```bash
# تحقق من الصلاحيات
ls -la halaqat.db

# أعد إنشاء قاعدة البيانات
python setup.py
```

#### الملفات الثابتة لا تعمل

- تأكد من مسارات Static files صحيحة
- تحقق من الصلاحيات: `chmod -R 755 static/`

## 🔐 الأمان

### قائمة التحقق الأمني:

- ✅ تغيير SECRET_KEY
- ✅ تعطيل DEBUG mode
- ✅ استخدام HTTPS (مجاني على PythonAnywhere)
- ✅ تغيير كلمة مرور المدير الافتراضية
- ✅ نسخ احتياطي منتظم لقاعدة البيانات
- ✅ تحديد allowed hosts
- ✅ تشفير قاعدة البيانات (للبيانات الحساسة جداً)

### تأمين قاعدة البيانات

```bash
# إنشاء نسخة احتياطية
cp halaqat.db halaqat_backup_$(date +%Y%m%d).db

# تقييد الصلاحيات
chmod 600 halaqat.db
```

## 📈 الأداء

### تحسين الأداء:

1. **استخدام قاعدة MySQL** للمشاريع الكبيرة
2. **تفعيل Caching** في Flask
3. **ضغط الملفات الثابتة**
4. **استخدام CDN** للملفات الكبيرة

### حدود الحساب المجاني:

- حركة مرور: محدودة
- CPU: محدود
- قاعدة بيانات: SQLite فقط
- نطاق: `username.pythonanywhere.com`

للترقية: [خطط PythonAnywhere](https://www.pythonanywhere.com/pricing/)

## 🌐 النطاق المخصص

للاستخدام مع نطاقك الخاص:

1. ترقية إلى حساب مدفوع
2. في تبويب **Web** → **Setup your domain**
3. أضف سجلات DNS:
   - CNAME: `www` → `webapp-XXXX.pythonanywhere.com`
   - A: `@` → IP address المقدم

## 📞 الدعم

- [توثيق PythonAnywhere](https://help.pythonanywhere.com/)
- [منتدى PythonAnywhere](https://www.pythonanywhere.com/forums/)
- [دعم البريد الإلكتروني](mailto:support@pythonanywhere.com)

## ✅ قائمة التحقق النهائية

قبل الإطلاق:

- [ ] استنساخ المشروع من GitHub
- [ ] تثبيت المتطلبات في البيئة الافتراضية
- [ ] إعداد قاعدة البيانات
- [ ] تكوين WSGI بشكل صحيح
- [ ] إضافة مسارات Static files
- [ ] تغيير SECRET_KEY
- [ ] تغيير كلمة مرور المدير
- [ ] اختبار جميع الصفحات
- [ ] إعداد النسخ الاحتياطي
- [ ] مراجعة سجلات الأخطاء

## 🎉 تم النشر بنجاح!

يمكنك الآن الوصول إلى نظامك على:
`https://YOUR_USERNAME.pythonanywhere.com`

---

**آخر تحديث:** 2025-01-06
