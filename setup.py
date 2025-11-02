"""
سكريبت إعداد النظام - يقوم بإنشاء المجلدات المطلوبة
"""
import os

def create_directory(path):
    """إنشاء مجلد إذا لم يكن موجوداً"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'✅ تم إنشاء المجلد: {path}')
    else:
        print(f'✓ المجلد موجود: {path}')

def main():
    print('╔════════════════════════════════════════════════════════════╗')
    print('║             إعداد نظام إدارة معلمي الحلقات               ║')
    print('╚════════════════════════════════════════════════════════════╝')
    print()
    
    # المجلدات المطلوبة
    directories = [
        'static',
        'static/css',
        'static/js',
        'static/images',
        'static/uploads',
        'static/uploads/attachments',
        'templates',
        'templates/employee',
        'templates/supervisor',
        'templates/admin',
        'uploads',
        'uploads/attachments',
    ]
    
    print('إنشاء المجلدات المطلوبة...')
    print()
    
    for directory in directories:
        create_directory(directory)
    
    # إنشاء ملفات .gitkeep للمجلدات الفارغة
    gitkeep_dirs = [
        'uploads',
        'uploads/attachments',
        'static/uploads',
        'static/uploads/attachments',
    ]
    
    print()
    print('إنشاء ملفات .gitkeep...')
    print()
    
    for directory in gitkeep_dirs:
        gitkeep_file = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_file):
            with open(gitkeep_file, 'w') as f:
                f.write('')
            print(f'✅ تم إنشاء: {gitkeep_file}')
    
    print()
    print('╔════════════════════════════════════════════════════════════╗')
    print('║                  ✅ تم الإعداد بنجاح                     ║')
    print('╚════════════════════════════════════════════════════════════╝')
    print()
    print('الخطوات التالية:')
    print('1. تثبيت المكتبات: pip install -r requirements.txt')
    print('2. إنشاء الشعار: python create_logo.py')
    print('3. تشغيل النظام: python app.py')
    print()
    print('أو استخدم: run.bat (Windows) أو ./run.sh (Linux/Mac)')

if __name__ == '__main__':
    main()
