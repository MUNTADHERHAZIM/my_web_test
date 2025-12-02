from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import json
import mimetypes
from PIL import Image
import uuid
from datetime import datetime

# إعدادات الملفات المدعومة
SUPPORTED_FILES = {
    'images': {
        'extensions': ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'],
        'max_size': 5 * 1024 * 1024,  # 5MB
        'folder': 'uploads/images/'
    },
    'videos': {
        'extensions': ['mp4', 'webm', 'ogg', 'avi', 'mov', 'wmv'],
        'max_size': 50 * 1024 * 1024,  # 50MB
        'folder': 'uploads/videos/'
    },
    'audio': {
        'extensions': ['mp3', 'wav', 'ogg', 'aac', 'm4a'],
        'max_size': 10 * 1024 * 1024,  # 10MB
        'folder': 'uploads/audio/'
    },
    'documents': {
        'extensions': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt'],
        'max_size': 10 * 1024 * 1024,  # 10MB
        'folder': 'uploads/documents/'
    },
    'archives': {
        'extensions': ['zip', 'rar', '7z', 'tar', 'gz'],
        'max_size': 20 * 1024 * 1024,  # 20MB
        'folder': 'uploads/archives/'
    }
}

def get_file_type(filename):
    """تحديد نوع الملف بناءً على الامتداد"""
    extension = filename.split('.')[-1].lower()
    for file_type, config in SUPPORTED_FILES.items():
        if extension in config['extensions']:
            return file_type, config
    return None, None

def validate_file(file):
    """التحقق من صحة الملف"""
    file_type, config = get_file_type(file.name)
    
    if not file_type:
        return False, f"نوع الملف غير مدعوم (.{file.name.split('.')[-1]})"
    
    if file.size > config['max_size']:
        max_size_mb = config['max_size'] / (1024 * 1024)
        return False, f"حجم الملف كبير جداً (الحد الأقصى: {max_size_mb:.1f} ميجابايت)"
    
    return True, file_type

def compress_image(image_file, max_width=1920, max_height=1080, quality=85):
    """ضغط الصورة وتقليل حجمها"""
    try:
        with Image.open(image_file) as img:
            # تحويل RGBA إلى RGB إذا لزم الأمر
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # تغيير حجم الصورة إذا كانت كبيرة
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # حفظ الصورة المضغوطة
            from io import BytesIO
            output = BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            
            return ContentFile(output.read())
    except Exception as e:
        print(f"خطأ في ضغط الصورة: {e}")
        return image_file

def generate_unique_filename(original_filename):
    """إنشاء اسم ملف فريد"""
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}_{name}{ext}"

@login_required
@require_http_methods(["POST"])
def upload_file(request):
    """رفع ملف واحد"""
    try:
        if 'upload' not in request.FILES:
            return JsonResponse({
                'error': 'لم يتم العثور على ملف للرفع'
            }, status=400)
        
        uploaded_file = request.FILES['upload']
        
        # التحقق من صحة الملف
        is_valid, result = validate_file(uploaded_file)
        if not is_valid:
            return JsonResponse({
                'error': result
            }, status=400)
        
        file_type = result
        config = SUPPORTED_FILES[file_type]
        
        # إنشاء اسم ملف فريد
        unique_filename = generate_unique_filename(uploaded_file.name)
        file_path = os.path.join(config['folder'], unique_filename)
        
        # ضغط الصورة إذا كانت صورة
        if file_type == 'images':
            uploaded_file = compress_image(uploaded_file)
        
        # حفظ الملف
        saved_path = default_storage.save(file_path, uploaded_file)
        file_url = default_storage.url(saved_path)
        
        # إرجاع معلومات الملف
        return JsonResponse({
            'url': file_url,
            'filename': unique_filename,
            'original_name': uploaded_file.name,
            'size': uploaded_file.size,
            'type': file_type,
            'uploaded': True
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'خطأ في رفع الملف: {str(e)}'
        }, status=500)

@login_required
@require_http_methods(["GET"])
def browse_files(request):
    """تصفح الملفات المرفوعة"""
    try:
        files = []
        
        # تصفح جميع مجلدات الملفات
        for file_type, config in SUPPORTED_FILES.items():
            folder_path = config['folder']
            
            try:
                # الحصول على قائمة الملفات في المجلد
                if default_storage.exists(folder_path):
                    folder_files = default_storage.listdir(folder_path)[1]  # [1] للملفات، [0] للمجلدات
                    
                    for filename in folder_files:
                        file_path = os.path.join(folder_path, filename)
                        if default_storage.exists(file_path):
                            file_url = default_storage.url(file_path)
                            file_size = default_storage.size(file_path)
                            
                            # تحديد نوع MIME
                            mime_type, _ = mimetypes.guess_type(filename)
                            
                            files.append({
                                'name': filename,
                                'url': file_url,
                                'size': file_size,
                                'type': mime_type,
                                'category': file_type,
                                'modified': default_storage.get_modified_time(file_path).isoformat()
                            })
            except Exception as e:
                print(f"خطأ في تصفح مجلد {folder_path}: {e}")
                continue
        
        # ترتيب الملفات حسب تاريخ التعديل (الأحدث أولاً)
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return JsonResponse({
            'files': files,
            'total': len(files)
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'خطأ في تصفح الملفات: {str(e)}',
            'files': []
        }, status=500)

@login_required
@require_http_methods(["POST"])
def delete_file(request):
    """حذف ملف"""
    try:
        data = json.loads(request.body)
        file_url = data.get('url')
        
        if not file_url:
            return JsonResponse({
                'error': 'لم يتم تحديد الملف للحذف'
            }, status=400)
        
        # استخراج مسار الملف من الرابط
        file_path = file_url.replace(settings.MEDIA_URL, '')
        
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
            return JsonResponse({
                'success': True,
                'message': 'تم حذف الملف بنجاح'
            })
        else:
            return JsonResponse({
                'error': 'الملف غير موجود'
            }, status=404)
            
    except Exception as e:
        return JsonResponse({
            'error': f'خطأ في حذف الملف: {str(e)}'
        }, status=500)

@login_required
@require_http_methods(["GET"])
def get_file_info(request):
    """الحصول على معلومات ملف"""
    try:
        file_url = request.GET.get('url')
        
        if not file_url:
            return JsonResponse({
                'error': 'لم يتم تحديد الملف'
            }, status=400)
        
        # استخراج مسار الملف من الرابط
        file_path = file_url.replace(settings.MEDIA_URL, '')
        
        if not default_storage.exists(file_path):
            return JsonResponse({
                'error': 'الملف غير موجود'
            }, status=404)
        
        filename = os.path.basename(file_path)
        file_size = default_storage.size(file_path)
        file_modified = default_storage.get_modified_time(file_path)
        mime_type, _ = mimetypes.guess_type(filename)
        file_type, _ = get_file_type(filename)
        
        return JsonResponse({
            'name': filename,
            'url': file_url,
            'size': file_size,
            'type': mime_type,
            'category': file_type,
            'modified': file_modified.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'خطأ في الحصول على معلومات الملف: {str(e)}'
        }, status=500)