#!/usr/bin/env python3
"""
سكريبت تشخيص سريع لـ PythonAnywhere
"""

import sys
import os

print("=" * 60)
print("🔍 تشخيص مشاكل PythonAnywhere")
print("=" * 60)
print()

# 1. التحقق من Python
print("[1/7] التحقق من إصدار Python...")
print(f"   ✅ Python: {sys.version}")
print()

# 2. التحقق من المسار الحالي
print("[2/7] التحقق من المسار...")
current_dir = os.getcwd()
print(f"   📁 المسار الحالي: {current_dir}")
print()

# 3. التحقق من الملفات الأساسية
print("[3/7] التحقق من الملفات الأساسية...")
required_files = ['app.py', 'config.py', 'models.py', 'requirements.txt', 'setup.py']
for file in required_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - مفقود!")
print()

# 4. التحقق من المكتبات
print("[4/7] التحقق من المكتبات المطلوبة...")
required_modules = {
    'flask': 'Flask',
    'flask_sqlalchemy': 'Flask-SQLAlchemy',
    'flask_login': 'Flask-Login',
    'arabic_reshaper': 'arabic-reshaper',
    'bidi': 'python-bidi'
}

missing_modules = []
for module, name in required_modules.items():
    try:
        __import__(module)
        print(f"   ✅ {name}")
    except ImportError:
        print(f"   ❌ {name} - غير مثبت!")
        missing_modules.append(name)
print()

# 5. التحقق من قاعدة البيانات
print("[5/7] التحقق من قاعدة البيانات...")
if os.path.exists('halaqat.db'):
    db_size = os.path.getsize('halaqat.db')
    if db_size > 1000:
        print(f"   ✅ halaqat.db موجودة ({db_size} bytes)")
    else:
        print(f"   ⚠️  halaqat.db موجودة لكنها صغيرة جداً ({db_size} bytes)")
        print(f"   💡 قد تحتاج لتشغيل: python3 setup.py")
else:
    print(f"   ❌ halaqat.db - مفقودة!")
    print(f"   💡 شغّل: python3 setup.py")
print()

# 6. محاولة استيراد التطبيق
print("[6/7] محاولة استيراد التطبيق...")
try:
    from app import app
    print("   ✅ تم استيراد التطبيق بنجاح!")
    print(f"   ✅ Flask app name: {app.name}")
except Exception as e:
    print(f"   ❌ فشل استيراد التطبيق!")
    print(f"   ❌ الخطأ: {str(e)}")
print()

# 7. التحقق من المجلدات
print("[7/7] التحقق من المجلدات...")
required_dirs = ['templates', 'static', 'uploads']
for dir_name in required_dirs:
    if os.path.exists(dir_name) and os.path.isdir(dir_name):
        files_count = len(os.listdir(dir_name))
        print(f"   ✅ {dir_name}/ ({files_count} items)")
    else:
        print(f"   ❌ {dir_name}/ - مفقود!")
print()

# النتيجة النهائية
print("=" * 60)
print("📊 ملخص التشخيص")
print("=" * 60)

issues = []

# جمع المشاكل
if not all(os.path.exists(f) for f in required_files):
    issues.append("⚠️  ملفات أساسية مفقودة")

if missing_modules:
    issues.append(f"⚠️  مكتبات غير مثبتة: {', '.join(missing_modules)}")

if not os.path.exists('halaqat.db'):
    issues.append("⚠️  قاعدة البيانات مفقودة")

if issues:
    print("\n❌ توجد مشاكل يجب حلها:\n")
    for issue in issues:
        print(f"  {issue}")
    print("\n💡 الحلول المقترحة:")
    print()
    if missing_modules:
        print("  1. تثبيت المكتبات:")
        print("     pip3 install --user -r requirements.txt")
        print()
    if not os.path.exists('halaqat.db'):
        print("  2. تهيئة قاعدة البيانات:")
        print("     python3 setup.py")
        print()
    print("  3. إعادة تحميل الموقع من لوحة Web")
    print()
else:
    print("\n✅ كل شيء يبدو جيداً!")
    print()
    print("💡 إذا كان الموقع لا يعمل:")
    print("  1. تحقق من WSGI configuration")
    print("  2. تحقق من Static files settings")
    print("  3. اضغط Reload في لوحة Web")
    print()

print("=" * 60)
print()
print("📖 للمزيد من المساعدة، راجع:")
print("   PYTHONANYWHERE_TROUBLESHOOTING.md")
print()
