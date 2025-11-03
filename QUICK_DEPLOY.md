# ⚡ دليل النشر السريع

## 🔥 خطوات سريعة للنشر

---

## 1️⃣ GitHub (5 دقائق)

### أ) على GitHub.com:
1. اذهب إلى https://github.com
2. اضغط **"New Repository"** (أخضر في الأعلى)
3. Repository name: `halaqat-system`
4. Description: `نظام إدارة معلمي الحلقات - مكة المكرمة`
5. اختر **Public** (أو Private حسب رغبتك)
6. **لا تختر** "Initialize with README" (لأنه موجود)
7. اضغط **"Create repository"**

### ب) في Terminal/PowerShell (في مجلد المشروع):

```bash
# 1. تهيئة Git
git init

# 2. إضافة الملفات
git add .

# 3. Commit
git commit -m "Initial commit: نظام إدارة معلمي الحلقات"

# 4. تحديد branch (استبدل main بـ master إذا لزم الأمر)
git branch -M main

# 5. ربط بـ GitHub (استبدل YOUR_USERNAME باسمك)
git remote add origin https://github.com/YOUR_USERNAME/halaqat-system.git

# 6. رفع المشروع
git push -u origin main
```

### ج) إذا طلب منك اسم مستخدم وكلمة مرور:
- **Username:** اسمك في GitHub
- **Password:** استخدم **Personal Access Token** (ليس كلمة المرور العادية)

#### كيف تحصل على Token:
1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. اختر: `repo` (كامل)
5. انسخ الـ Token واستخدمه بدلاً من كلمة المرور

---

## 2️⃣ PythonAnywhere (15 دقيقة)

### أ) إنشاء حساب:
1. https://www.pythonanywhere.com
2. اضغط **"Pricing & signup"**
3. اختر **"Create a Beginner account"** (مجاني)
4. سجل حسابك

### ب) استنساخ المشروع:

```bash
# في PythonAnywhere → Consoles → Bash
cd ~
git clone https://github.com/YOUR_USERNAME/halaqat-system.git
cd halaqat-system
```

### ج) تثبيت المكتبات:

```bash
pip3 install --user -r requirements.txt
```

⏰ **قد يستغرق 2-3 دقائق**

### د) تهيئة قاعدة البيانات:

```bash
python3 setup.py
```

### هـ) إنشاء Web App:

1. اذهب إلى تبويب **"Web"**
2. اضغط **"Add a new web app"**
3. اضغط **"Next"**
4. اختر **"Manual configuration"**
5. اختر **Python 3.10**
6. اضغط **"Next"**

### و) إعداد WSGI:

1. في صفحة Web → قسم "Code"
2. اضغط على **"WSGI configuration file"** (مثل: `/var/www/username_pythonanywhere_com_wsgi.py`)
3. **احذف كل المحتوى**
4. الصق هذا الكود:

```python
import sys
import os

# استبدل YOUR_USERNAME باسمك
project_home = '/home/YOUR_USERNAME/halaqat-system'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
```

5. احفظ (Ctrl+S)

### ز) إعداد Static Files:

في صفحة **Web** → قسم **"Static files"**:

اضغط **"Enter URL"** و **"Enter path"**:

```
URL: /static/
Directory: /home/YOUR_USERNAME/halaqat-system/static
```

استبدل `YOUR_USERNAME` باسم حسابك!

### ح) إعادة التشغيل:

1. في صفحة **Web**
2. اضغط الزر الأخضر الكبير **"Reload YOUR_USERNAME.pythonanywhere.com"**

### ط) افتح الموقع:

```
https://YOUR_USERNAME.pythonanywhere.com
```

---

## ✅ قائمة التحقق السريعة

قبل النشر:
- [ ] حذفت بيانات الاختبار (`python delete_test_data.py`)
- [ ] شغلت `python prepare_for_deployment.py`
- [ ] غيّرت `SECRET_KEY` في `config.py`
- [ ] `DEBUG = False` في `config.py`

بعد النشر على PythonAnywhere:
- [ ] دخلت على الموقع
- [ ] سجلت دخول كمدير
- [ ] غيّرت كلمة مرور المدير
- [ ] اختبرت الميزات الأساسية

---

## 🆘 حل المشاكل السريع

### ❌ خطأ: ModuleNotFoundError

```bash
# في PythonAnywhere Console
cd ~/halaqat-system
pip3 install --user -r requirements.txt
```

### ❌ خطأ: 500 Internal Server Error

```bash
# تحقق من Error Log في PythonAnywhere → Web → Log files
```

### ❌ الصور/CSS لا تظهر

```
تأكد من Static Files في Web:
URL: /static/
Directory: /home/YOUR_USERNAME/halaqat-system/static
```

### ❌ قاعدة البيانات فارغة

```bash
cd ~/halaqat-system
python3 setup.py
```

---

## 🎉 انتهيت!

الموقع الآن متاح على:
- **GitHub:** `https://github.com/YOUR_USERNAME/halaqat-system`
- **Live:** `https://YOUR_USERNAME.pythonanywhere.com`

---

**بالتوفيق! 🚀**
