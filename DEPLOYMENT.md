# 🚀 دليل النشر - نظام إدارة معلمي الحلقات

## 📋 المحتويات
1. [النشر على GitHub](#النشر-على-github)
2. [النشر على PythonAnywhere](#النشر-على-pythonanywhere)
3. [الإعدادات المطلوبة](#الإعدادات-المطلوبة)

---

## 📦 النشر على GitHub

### الخطوات:

#### 1. إنشاء Repository جديد على GitHub
```bash
1. اذهب إلى https://github.com
2. اضغط على "New Repository"
3. اسم المشروع: halaqat-management-system
4. الوصف: نظام إدارة معلمي الحلقات - مكة المكرمة
5. اختر: Public أو Private
6. لا تختر README (لأنه موجود مسبقاً)
7. اضغط "Create Repository"
```

#### 2. ربط المشروع بـ GitHub
```bash
# افتح Terminal في مجلد المشروع

# 1. تهيئة Git (إذا لم يكن مهيأً)
git init

# 2. إضافة جميع الملفات
git add .

# 3. عمل Commit
git commit -m "Initial commit: نظام إدارة معلمي الحلقات"

# 4. ربط المشروع بـ GitHub (استبدل USERNAME باسمك)
git remote add origin https://github.com/USERNAME/halaqat-management-system.git

# 5. رفع المشروع
git push -u origin main
```

#### 3. إضافة ملف .gitkeep للمجلدات الفارغة
```bash
# في مجلد uploads
echo "" > uploads/.gitkeep

# في مجلد static/images
echo "" > static/images/.gitkeep
```

---

## 🌐 النشر على PythonAnywhere

### الخطوات:

#### 1. إنشاء حساب
```
1. اذهب إلى https://www.pythonanywhere.com
2. اضغط "Start running Python online"
3. اختر الخطة المجانية "Beginner"
4. سجل حسابك
```

#### 2. رفع الملفات

**الطريقة 1: من GitHub (الأسرع)**
```bash
# في PythonAnywhere Console
cd ~
git clone https://github.com/USERNAME/halaqat-management-system.git
cd halaqat-management-system
```

**الطريقة 2: رفع مباشر**
```
1. اذهب إلى "Files"
2. ارفع ملف ZIP للمشروع
3. فك الضغط
```

#### 3. تثبيت المكتبات
```bash
# في PythonAnywhere Console
cd ~/halaqat-management-system
pip3 install --user -r requirements.txt
```

#### 4. إنشاء Web App

```
1. اذهب إلى "Web"
2. اضغط "Add a new web app"
3. اختر "Manual configuration"
4. اختر Python 3.10
5. اضغط "Next"
```

#### 5. إعداد WSGI

```python
# في "Web" → "Code" → "WSGI configuration file"
# احذف كل المحتوى واستبدله بـ:

import sys
import os

# إضافة مسار المشروع
project_home = '/home/USERNAME/halaqat-management-system'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# تحميل التطبيق
from app import app as application
```

**استبدل USERNAME باسم حسابك في PythonAnywhere**

#### 6. إعداد Static Files
```
في "Web" → "Static files":

URL: /static/
Directory: /home/USERNAME/halaqat-management-system/static
```

#### 7. تهيئة قاعدة البيانات
```bash
# في PythonAnywhere Console
cd ~/halaqat-management-system
python3 setup.py
```

#### 8. إعادة تشغيل التطبيق
```
في "Web" اضغط الزر الأخضر الكبير "Reload"
```

#### 9. الوصول للموقع
```
https://USERNAME.pythonanywhere.com
```

---

## ⚙️ الإعدادات المطلوبة

### 1. المتغيرات البيئية (config.py)

قبل النشر، تأكد من تعديل:

```python
# config.py

class Config:
    # مفتاح سري قوي
    SECRET_KEY = 'أدخل-مفتاح-سري-قوي-هنا'  # ⚠️ غيّر هذا!
    
    # قاعدة البيانات
    SQLALCHEMY_DATABASE_URI = 'sqlite:///halaqat.db'
    
    # التطوير/الإنتاج
    DEBUG = False  # ⚠️ False في الإنتاج!
```

### 2. إنشاء مفتاح سري قوي

```python
# في Python Console
import secrets
print(secrets.token_hex(32))
# انسخ المخرج واستخدمه كـ SECRET_KEY
```

### 3. حذف بيانات الاختبار

```bash
# قبل النشر
python3 delete_test_data.py

# أو من لوحة الإدارة:
# تسجيل الدخول → لوحة التحكم → "حذف بيانات الاختبار"
```

---

## 🔒 الأمان

### قبل النشر:
- ✅ تغيير `SECRET_KEY` في `config.py`
- ✅ تعيين `DEBUG = False`
- ✅ حذف بيانات الاختبار
- ✅ إنشاء حساب مدير جديد برقم هوية حقيقي
- ✅ التأكد من عدم وجود معلومات حساسة في الكود

### بعد النشر:
- 🔐 تغيير كلمة مرور المدير الافتراضية
- 🔐 إنشاء نسخة احتياطية دورية لقاعدة البيانات
- 🔐 مراقبة السجلات (Logs)

---

## 📝 بيانات الدخول الافتراضية

**⚠️ مدير النظام (للتجربة فقط):**
```
رقم الهوية: 1000000000
كلمة المرور: admin123
```

**🔴 مهم جداً:**
1. احذف هذا الحساب بعد إنشاء حساب مدير حقيقي
2. أو غيّر كلمة المرور فوراً
3. أو غيّر رقم الهوية

---

## 🆘 حل المشاكل الشائعة

### مشكلة: ModuleNotFoundError

```bash
# الحل: تثبيت المكتبات
pip3 install --user -r requirements.txt
```

### مشكلة: قاعدة البيانات فارغة

```bash
# الحل: تشغيل setup.py
python3 setup.py
```

### مشكلة: Static Files لا تظهر

```
تأكد من إعداد Static Files في PythonAnywhere:
URL: /static/
Directory: /home/USERNAME/halaqat-management-system/static
```

### مشكلة: 500 Internal Server Error

```
1. تحقق من WSGI configuration
2. تحقق من Error Log في PythonAnywhere
3. تأكد أن DEBUG = False
```

---

## 📞 الدعم

إذا واجهت أي مشاكل:
1. راجع Error Log في PythonAnywhere
2. تحقق من أن جميع المكتبات مثبتة
3. تأكد من صحة المسارات في WSGI

---

## 🎉 نجاح النشر!

بعد إتمام الخطوات، سيكون النظام متاحاً على:
- **GitHub:** `https://github.com/USERNAME/halaqat-management-system`
- **PythonAnywhere:** `https://USERNAME.pythonanywhere.com`

---

**تم بحمد الله! 🚀**
