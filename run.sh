#!/bin/bash

# تفعيل UTF-8
export LANG=en_US.UTF-8

echo "╔════════════════════════════════════════════════════════════╗"
echo "║       نظام إدارة معلمي الحلقات - مكة المكرمة             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "[1/4] التحقق من Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ خطأ: Python غير مثبت"
    exit 1
fi
python3 --version
echo "✅ Python مثبت بنجاح"
echo ""

echo "[2/4] التحقق من المكتبات المطلوبة..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "⚠️ المكتبات غير مثبتة. جاري التثبيت..."
    pip3 install -r requirements.txt
fi
echo "✅ جميع المكتبات متوفرة"
echo ""

echo "[3/4] إنشاء صور الشعار..."
python3 create_logo.py
echo ""

echo "[4/4] بدء تشغيل النظام..."
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  النظام يعمل الآن على: http://localhost:5000            ║"
echo "║                                                            ║"
echo "║  بيانات الدخول الافتراضية:                               ║"
echo "║  رقم الهوية: 1000000000                                   ║"
echo "║  كلمة المرور: admin123                                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "للإيقاف: اضغط Ctrl+C"
echo ""

python3 app.py
