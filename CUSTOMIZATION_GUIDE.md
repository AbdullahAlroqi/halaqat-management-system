# 🎨 دليل تخصيص النظام

## 1️⃣ تغيير كلمة سر مدير النظام

### الطريقة 1: باستخدام السكريبت

```bash
# 1. افتح ملف change_admin_password.py
# 2. غيّر السطر:
NEW_PASSWORD = "admin123"  # ⬅️ ضع كلمة السر الجديدة هنا

# 3. شغّل السكريبت:
python change_admin_password.py
```

### الطريقة 2: من داخل النظام

```python
from app import app, db
from models import User

with app.app_context():
    admin = User.query.filter_by(national_id='1000000000').first()
    admin.set_password('كلمة_السر_الجديدة')
    db.session.commit()
    print("✅ تم تغيير كلمة السر")
```

---

## 2️⃣ تغيير الأيقونة (Favicon)

### ✅ تم بالفعل! 

الأيقونة الآن تستخدم نفس الشعار:
- `static/images/logo-144.png` للأيقونة
- يظهر في تبويب المتصفح
- يظهر في المفضلة

### لتغيير الأيقونة:

1. ضع الصورة الجديدة في: `static/images/`
2. غيّر في `templates/base.html` السطر 19-20:
```html
<link rel="icon" type="image/png" href="{{ url_for('static', filename='images/اسم_الصورة.png') }}">
```

---

## 3️⃣ تغيير نص أسفل الموقع (Footer)

### ✅ تم تحديثه!

النص الحالي:
```
🕋 جمعية تحفيظ القرآن الكريم بمكة المكرمة
نظام إدارة معلمي الحلقات والمقرأة الإلكترونية
مكة المكرمة - 1446 هـ
```

### لتغييره:

افتح `templates/base.html` وعدّل الأسطر 230-238:
```html
<p class="mb-2">
    <i class="fas fa-kaaba ms-1"></i>
    <strong>اسم المؤسسة</strong>
</p>
<p class="mb-1 small">
    وصف النظام
</p>
<p class="mb-0 small text-muted">
    المدينة - التاريخ
</p>
```

---

## 4️⃣ تغيير اسم الموقع في المتصفح

في `templates/base.html` السطر 16:
```html
<title>{% block title %}نظام إدارة معلمي الحلقات - مكة المكرمة{% endblock %}</title>
```

غيّره إلى:
```html
<title>{% block title %}اسم الموقع الجديد{% endblock %}</title>
```

---

## 5️⃣ تغيير الشعار

### الشعار الرئيسي في الصفحة:

الشعار موجود في: `static/images/`

لتغييره:
1. استبدل الصورة في المجلد
2. أو غيّر المسار في `templates/base.html` السطر ~70-80 (في navbar)

---

## 🚀 تطبيق التغييرات

### على الجهاز المحلي:
```bash
python app.py
```

### على PythonAnywhere:
```bash
# 1. رفع على GitHub
git add .
git commit -m "Customize site: password, favicon, footer"
git push origin main

# 2. في PythonAnywhere Console:
cd ~/halaqat-management-system
git pull origin main

# 3. تغيير كلمة السر:
python3 change_admin_password.py

# 4. Reload الموقع من تبويب Web
```

---

## 📝 ملف change_admin_password.py

```python
from app import app, db
from models import User

NEW_PASSWORD = "كلمة_السر_الجديدة"  # ⬅️ غيّر هنا

with app.app_context():
    admin = User.query.filter_by(national_id='1000000000').first()
    if admin:
        admin.set_password(NEW_PASSWORD)
        db.session.commit()
        print(f"✅ تم تغيير كلمة السر إلى: {NEW_PASSWORD}")
    else:
        print("❌ لم يتم العثور على المدير")
```

---

## ✅ قائمة المراجعة

- [x] تغيير كلمة السر ← `change_admin_password.py`
- [x] إضافة الأيقونة ← `templates/base.html` (السطر 19-20)
- [x] تحديث الفوتر ← `templates/base.html` (السطر 230-238)
- [ ] اختبار على المتصفح
- [ ] رفع على PythonAnywhere

---

**جاهز للتطبيق! 🎉**
