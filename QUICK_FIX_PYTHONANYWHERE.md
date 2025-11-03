# ⚡ حل سريع لـ PythonAnywhere

## 🔥 نفذ هذه الأوامر بالترتيب

### في PythonAnywhere Console:

```bash
# 1. اذهب للمجلد
cd ~/halaqat-management-system

# 2. شغّل التشخيص
python3 diagnose.py

# 3. ثبّت المكتبات
pip3 install --user -r requirements.txt

# 4. هيّء قاعدة البيانات
python3 setup.py

# 5. اختبر التطبيق
python3 -c "from app import app; print('✅ Success!')"
```

---

## ⚙️ WSGI Configuration

في **Web** → **Code** → **WSGI configuration file**:

**احذف كل شيء** والصق هذا:

```python
import sys
import os

project_home = '/home/halaqat/halaqat-management-system'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
```

**⚠️ مهم:** غيّر `halaqat` إلى اسم حسابك إذا كان مختلفاً!

---

## 📁 Static Files

في **Web** → **Static files**:

```
URL: /static/
Directory: /home/halaqat/halaqat-management-system/static
```

---

## 🔄 إعادة التحميل

1. اذهب إلى **Web**
2. اضغط الزر الأخضر الكبير **"Reload halaqat.pythonanywhere.com"**
3. انتظر 10 ثواني
4. افتح: `https://halaqat.pythonanywhere.com`

---

## ✅ إذا عمل

يجب أن ترى:
- صفحة تسجيل الدخول
- الشعار والألوان
- يمكنك الدخول بـ: `1000000000` / `admin123`

---

## ❌ إذا لم يعمل

### افتح Error Log:

1. **Web** → **Log files** → **error log**
2. انظر آخر سطر
3. ابحث عن:

#### "No module named 'flask'"
```bash
pip3 install --user Flask Flask-SQLAlchemy Flask-Login
```

#### "No module named 'arabic_reshaper'"
```bash
pip3 install --user arabic-reshaper python-bidi
```

#### "no such table: user"
```bash
cd ~/halaqat-management-system
python3 setup.py
```

#### "ModuleNotFoundError: No module named 'app'"
- تحقق من WSGI configuration
- تأكد من المسار صحيح

---

## 📞 ما زلت عالق؟

أرسل لي:
1. آخر 20 سطر من **error log**
2. نتيجة: `pip3 list | grep Flask`
3. نتيجة: `ls -la ~/halaqat-management-system/`

---

**بالتوفيق! 🚀**
