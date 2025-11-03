@echo off
chcp 65001 > nul
title نظام إدارة معلمي الحلقات - مكة المكرمة

echo ╔════════════════════════════════════════════════════════════╗
echo ║       نظام إدارة معلمي الحلقات - مكة المكرمة             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [1/4] التحقق من Python...
python --version
if errorlevel 1 (
    echo ❌ خطأ: Python غير مثبت. الرجاء تثبيت Python 3.8 أو أحدث
    pause
    exit /b 1
)
echo ✅ Python مثبت بنجاح
echo.

echo [2/4] التحقق من المكتبات المطلوبة...
pip show Flask > nul 2>&1
if errorlevel 1 (
    echo ⚠️ المكتبات غير مثبتة. جاري التثبيت...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ خطأ في تثبيت المكتبات
        pause
        exit /b 1
    )
)
echo ✅ جميع المكتبات متوفرة
echo.

echo [3/4] إنشاء صور الشعار...
python create_logo.py
echo.

echo [4/4] بدء تشغيل النظام...
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  النظام يعمل الآن على: http://localhost:5000            ║
echo ║                                                            ║
echo ║  بيانات الدخول الافتراضية:                               ║
echo ║  رقم الهوية: 1000000000                                   ║
echo ║  كلمة المرور: admin123                                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo للإيقاف: اضغط Ctrl+C
echo.

python app.py

pause
