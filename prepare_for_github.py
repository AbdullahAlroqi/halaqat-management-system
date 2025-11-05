"""
سكريبت تجهيز المشروع للرفع على GitHub
ينظف الملفات الحساسة ويجهز المشروع
"""
import os
import shutil

def clean_project():
    """تنظيف المشروع قبل الرفع"""
    
    print("="*60)
    print("تجهيز المشروع للرفع على GitHub...")
    print("="*60)
    
    # الملفات والمجلدات المراد حذفها
    items_to_remove = [
        'halaqat.db',
        'instance/',
        '__pycache__/',
        '*.pyc',
        '.pytest_cache/',
        '.coverage',
        'htmlcov/',
    ]
    
    removed_count = 0
    
    for item in items_to_remove:
        # حذف ملفات بنمط معين
        if '*' in item:
            import glob
            files = glob.glob(f"**/{item}", recursive=True)
            for file in files:
                try:
                    os.remove(file)
                    print(f"✓ حذف: {file}")
                    removed_count += 1
                except Exception as e:
                    pass
        else:
            # حذف ملف أو مجلد محدد
            if os.path.exists(item):
                try:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                    else:
                        os.remove(item)
                    print(f"✓ حذف: {item}")
                    removed_count += 1
                except Exception as e:
                    print(f"⚠ تعذر حذف {item}: {str(e)}")
    
    # التأكد من وجود .gitkeep في مجلدات uploads
    gitkeep_dirs = ['uploads', 'static/uploads']
    for dir_path in gitkeep_dirs:
        if os.path.exists(dir_path):
            gitkeep_file = os.path.join(dir_path, '.gitkeep')
            if not os.path.exists(gitkeep_file):
                with open(gitkeep_file, 'w') as f:
                    f.write('')
                print(f"✓ أنشئ: {gitkeep_file}")
    
    print("\n" + "="*60)
    print(f"✅ تم تنظيف {removed_count} عنصر")
    print("="*60)
    print("\nالخطوات التالية:")
    print("1. راجع ملف .gitignore")
    print("2. تأكد من تحديث README_GITHUB.md")
    print("3. استخدم الأوامر التالية لرفع المشروع:")
    print("\n   git init")
    print("   git add .")
    print('   git commit -m "Initial commit"')
    print("   git branch -M main")
    print("   git remote add origin YOUR_REPO_URL")
    print("   git push -u origin main")
    print("\n" + "="*60)

if __name__ == '__main__':
    clean_project()
