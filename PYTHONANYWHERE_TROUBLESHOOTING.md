# 🆘 حل مشاكل PythonAnywhere

## 📋 المشكلة: Unhandled Exception

---

## ✅ الخطوات بالترتيب

### 1️⃣ التحقق من Error Log

في PythonAnywhere:
1. اذهب إلى **Web**
2. انزل لقسم **Log files**
3. اضغط على **error log**
4. ابحث عن السطر الأخير الذي يحتوي على `Error` أو `Exception`

**الأخطاء الشائعة:**

#### أ) ImportError: No module named 'flask'
```bash
# الحل: تثبيت المكتبات
cd ~/halaqat-management-system
pip3 install --user -r requirements.txt
```

#### ب) OperationalError: no such table
```bash
# الحل: تهيئة قاعدة البيانات
cd ~/halaqat-management-system
python3 setup.py
```

#### ج) ModuleNotFoundError: No module named 'app'
```bash
# الحل: مشكلة في WSGI configuration
# تأكد من المسار الصحيح
```

---

### 2️⃣ التحقق من WSGI Configuration

في **Web** → **Code** → **WSGI configuration file**:

```python
import sys
import os

# المسار يجب أن يكون صحيحاً
project_home = '/home/halaqat/halaqat-management-system'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# تحميل التطبيق
from app import app as application
```

**⚠️ مهم:**
- تأكد أن `halaqat` هو اسم حسابك الصحيح
- تأكد أن `halaqat-management-system` هو اسم المجلد الصحيح

---

### 3️⃣ التحقق من تثبيت المكتبات

```bash
# في PythonAnywhere Console
cd ~/halaqat-management-system

# تثبيت جميع المكتبات
pip3 install --user -r requirements.txt

# التحقق من التثبيت
pip3 list | grep -i flask
pip3 list | grep -i sqlalchemy
pip3 list | grep -i arabic
```

**يجب أن ترى:**
```
Flask                    2.3.3
Flask-Login              0.6.2
Flask-SQLAlchemy         3.0.5
arabic-reshaper          3.0.0
python-bidi              0.4.2
...
```

---

### 4️⃣ التحقق من قاعدة البيانات

```bash
# في PythonAnywhere Console
cd ~/halaqat-management-system

# تشغيل setup
python3 setup.py

# يجب أن ترى:
# تم إنشاء قاعدة البيانات بنجاح
# تم إضافة البيانات الأساسية
```

---

### 5️⃣ التحقق من Static Files

في **Web** → **Static files**:

```
URL: /static/
Directory: /home/halaqat/halaqat-management-system/static
```

**⚠️ تأكد:**
- لا توجد مسافات زائدة
- المسار يبدأ بـ `/home/`
- اسم المجلد صحيح

---

### 6️⃣ التحقق من الصلاحيات

```bash
# في PythonAnywhere Console
cd ~/halaqat-management-system

# التحقق من وجود الملفات
ls -la

# يجب أن ترى:
# app.py
# config.py
# models.py
# requirements.txt
# ...
```

---

## 🔧 الأخطاء الشائعة وحلولها

### خطأ 1: ModuleNotFoundError: No module named 'flask'
```bash
pip3 install --user Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Flask-Login==0.6.2
```

### خطأ 2: ModuleNotFoundError: No module named 'arabic_reshaper'
```bash
pip3 install --user arabic-reshaper==3.0.0 python-bidi==0.4.2
```

### خطأ 3: ImportError: cannot import name 'app' from 'app'
**المشكلة:** مسار خاطئ في WSGI
**الحل:** تحقق من المسار في WSGI configuration

### خطأ 4: OperationalError: no such table: user
**المشكلة:** قاعدة البيانات غير مهيأة
**الحل:**
```bash
cd ~/halaqat-management-system
rm halaqat.db  # احذف القديمة
python3 setup.py  # أنشئ جديدة
```

### خطأ 5: 403 Forbidden
**المشكلة:** مشكلة في Static files
**الحل:** تحقق من إعدادات Static files

---

## 🎯 خطة الحل السريعة

### نفذ هذه الأوامر بالترتيب:

```bash
# 1. اذهب للمجلد
cd ~/halaqat-management-system

# 2. تثبيت المكتبات
pip3 install --user -r requirements.txt

# 3. تهيئة قاعدة البيانات
python3 setup.py

# 4. التحقق من الملفات
ls -la

# 5. التحقق من app.py
python3 -c "from app import app; print('✅ App loaded successfully!')"
```

**إذا نجحت جميع الخطوات:**
1. اذهب إلى **Web**
2. اضغط **Reload halaqat.pythonanywhere.com**
3. افتح الموقع

---

## 📝 WSGI Configuration الصحيح

انسخ هذا بالضبط في WSGI configuration file:

```python
import sys
import os

# ⚠️ غيّر 'halaqat' إلى اسم حسابك إذا كان مختلفاً
project_home = '/home/halaqat/halaqat-management-system'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# تحميل التطبيق
from app import app as application

# لضمان عمل Flask
application.secret_key = os.environ.get("SECRET_KEY") or "fallback-secret-key"
```

---

## 🔍 التحقق النهائي

### في PythonAnywhere Console:

```bash
# اختبار استيراد التطبيق
cd ~/halaqat-management-system
python3 << EOF
import sys
sys.path.insert(0, '/home/halaqat/halaqat-management-system')
from app import app
print("✅ التطبيق تم تحميله بنجاح!")
print(f"✅ Flask version: {app.__module__}")
EOF
```

**إذا ظهر خطأ:**
- انسخ الخطأ الكامل
- ابحث عنه في Error log
- اتبع الحل المناسب أعلاه

---

## 📞 إذا لم يعمل

أرسل لي:
1. محتوى Error log (آخر 20 سطر)
2. نتيجة `pip3 list | grep -i flask`
3. نتيجة `ls -la ~/halaqat-management-system`

---

## ✅ علامات النجاح

عند نجاح النشر، يجب أن ترى:
```
✅ الموقع يفتح
✅ صفحة تسجيل الدخول تظهر
✅ الصور والـ CSS تعمل
✅ يمكن تسجيل الدخول
```

---

**بالتوفيق! 🚀**
