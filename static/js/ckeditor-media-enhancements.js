/**
 * CKEditor Media Enhancements
 * تحسينات متقدمة للوسائط في محرر CKEditor
 */

// إعدادات ضغط الصور
const IMAGE_COMPRESSION_SETTINGS = {
    maxWidth: 1200,
    maxHeight: 800,
    quality: 0.8,
    format: 'jpeg'
};

// أنواع الملفات المدعومة
const SUPPORTED_FILE_TYPES = {
    images: ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'],
    videos: ['mp4', 'webm', 'ogg', 'avi', 'mov'],
    documents: ['pdf', 'doc', 'docx', 'txt', 'rtf'],
    archives: ['zip', 'rar', '7z', 'tar']
};

// دالة ضغط الصور
function compressImage(file, callback) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = function() {
        // حساب الأبعاد الجديدة
        let { width, height } = img;
        const maxWidth = IMAGE_COMPRESSION_SETTINGS.maxWidth;
        const maxHeight = IMAGE_COMPRESSION_SETTINGS.maxHeight;
        
        if (width > maxWidth || height > maxHeight) {
            const ratio = Math.min(maxWidth / width, maxHeight / height);
            width *= ratio;
            height *= ratio;
        }
        
        canvas.width = width;
        canvas.height = height;
        
        // رسم الصورة المضغوطة
        ctx.drawImage(img, 0, 0, width, height);
        
        // تحويل إلى blob
        canvas.toBlob(callback, 'image/jpeg', IMAGE_COMPRESSION_SETTINGS.quality);
    };
    
    img.src = URL.createObjectURL(file);
}

// دالة إنشاء معاينة للملفات
function createFilePreview(file) {
    const preview = document.createElement('div');
    preview.className = 'file-preview';
    preview.style.cssText = `
        display: inline-block;
        margin: 10px;
        padding: 15px;
        border: 2px dashed #ddd;
        border-radius: 8px;
        text-align: center;
        background: #f9f9f9;
        position: relative;
        max-width: 200px;
    `;
    
    const fileName = document.createElement('div');
    fileName.textContent = file.name;
    fileName.style.cssText = 'font-size: 12px; margin-top: 5px; word-break: break-all;';
    
    const fileSize = document.createElement('div');
    fileSize.textContent = formatFileSize(file.size);
    fileSize.style.cssText = 'font-size: 10px; color: #666; margin-top: 2px;';
    
    // إنشاء معاينة حسب نوع الملف
    if (file.type.startsWith('image/')) {
        const img = document.createElement('img');
        img.style.cssText = 'max-width: 150px; max-height: 100px; border-radius: 4px;';
        img.src = URL.createObjectURL(file);
        preview.appendChild(img);
    } else if (file.type.startsWith('video/')) {
        const video = document.createElement('video');
        video.style.cssText = 'max-width: 150px; max-height: 100px; border-radius: 4px;';
        video.controls = true;
        video.src = URL.createObjectURL(file);
        preview.appendChild(video);
    } else {
        const icon = document.createElement('div');
        icon.innerHTML = getFileIcon(file.type);
        icon.style.cssText = 'font-size: 48px; color: #666;';
        preview.appendChild(icon);
    }
    
    preview.appendChild(fileName);
    preview.appendChild(fileSize);
    
    // زر الحذف
    const deleteBtn = document.createElement('button');
    deleteBtn.innerHTML = '×';
    deleteBtn.style.cssText = `
        position: absolute;
        top: -5px;
        right: -5px;
        background: #ff4444;
        color: white;
        border: none;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        cursor: pointer;
        font-size: 14px;
        line-height: 1;
    `;
    deleteBtn.onclick = () => preview.remove();
    preview.appendChild(deleteBtn);
    
    return preview;
}

// دالة تنسيق حجم الملف
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// دالة الحصول على أيقونة الملف
function getFileIcon(fileType) {
    if (fileType.includes('pdf')) return '📄';
    if (fileType.includes('word') || fileType.includes('document')) return '📝';
    if (fileType.includes('zip') || fileType.includes('archive')) return '📦';
    if (fileType.includes('video')) return '🎥';
    if (fileType.includes('audio')) return '🎵';
    return '📁';
}

// تحسين خاصية السحب والإفلات
function enhanceDragAndDrop(editor) {
    const editable = editor.editable();
    
    // منع السلوك الافتراضي
    editable.on('dragover', function(evt) {
        evt.data.preventDefault();
        editable.addClass('drag-over');
    });
    
    editable.on('dragleave', function(evt) {
        editable.removeClass('drag-over');
    });
    
    // معالجة إسقاط الملفات
    editable.on('drop', function(evt) {
        evt.data.preventDefault();
        editable.removeClass('drag-over');
        
        const files = evt.data.$.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files, editor);
        }
    });
}

// دالة معالجة رفع الملفات
function handleFileUpload(files, editor) {
    const previewContainer = document.getElementById('upload-preview') || createPreviewContainer();
    
    Array.from(files).forEach(file => {
        // إنشاء معاينة
        const preview = createFilePreview(file);
        previewContainer.appendChild(preview);
        
        // ضغط الصور قبل الرفع
        if (file.type.startsWith('image/') && file.size > 500000) { // أكبر من 500KB
            compressImage(file, function(compressedBlob) {
                uploadFile(compressedBlob, file.name, editor, preview);
            });
        } else {
            uploadFile(file, file.name, editor, preview);
        }
    });
}

// دالة إنشاء حاوية المعاينة
function createPreviewContainer() {
    const container = document.createElement('div');
    container.id = 'upload-preview';
    container.style.cssText = `
        margin: 10px 0;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background: #fafafa;
        min-height: 50px;
    `;
    
    const title = document.createElement('h4');
    title.textContent = 'معاينة الملفات المرفوعة';
    title.style.cssText = 'margin: 0 0 10px 0; font-size: 14px; color: #333;';
    container.appendChild(title);
    
    // إدراج الحاوية قبل المحرر
    const editorContainer = document.querySelector('.cke');
    if (editorContainer) {
        editorContainer.parentNode.insertBefore(container, editorContainer);
    }
    
    return container;
}

// دالة رفع الملف
function uploadFile(file, fileName, editor, previewElement) {
    const formData = new FormData();
    formData.append('upload', file, fileName);
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
    
    // شريط التقدم
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        width: 100%;
        height: 4px;
        background: #ddd;
        border-radius: 2px;
        margin-top: 5px;
        overflow: hidden;
    `;
    
    const progress = document.createElement('div');
    progress.style.cssText = `
        height: 100%;
        background: #4CAF50;
        width: 0%;
        transition: width 0.3s;
    `;
    progressBar.appendChild(progress);
    previewElement.appendChild(progressBar);
    
    // رفع الملف
    const xhr = new XMLHttpRequest();
    
    xhr.upload.onprogress = function(e) {
        if (e.lengthComputable) {
            const percentComplete = (e.loaded / e.total) * 100;
            progress.style.width = percentComplete + '%';
        }
    };
    
    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (response.url) {
                // إدراج الملف في المحرر
                insertMediaInEditor(response.url, file.type, fileName, editor);
                previewElement.style.borderColor = '#4CAF50';
                progress.style.background = '#4CAF50';
            }
        } else {
            previewElement.style.borderColor = '#ff4444';
            progress.style.background = '#ff4444';
        }
    };
    
    xhr.onerror = function() {
        previewElement.style.borderColor = '#ff4444';
        progress.style.background = '#ff4444';
    };
    
    xhr.open('POST', '/ckeditor/upload/');
    xhr.send(formData);
}

// دالة إدراج الوسائط في المحرر
function insertMediaInEditor(url, fileType, fileName, editor) {
    if (fileType.startsWith('image/')) {
        editor.insertHtml(`<img src="${url}" alt="${fileName}" style="max-width: 100%; height: auto;" />`);
    } else if (fileType.startsWith('video/')) {
        editor.insertHtml(`<video controls style="max-width: 100%; height: auto;"><source src="${url}" type="${fileType}">متصفحك لا يدعم تشغيل الفيديو.</video>`);
    } else {
        editor.insertHtml(`<a href="${url}" target="_blank">${fileName}</a>`);
    }
}

// تهيئة التحسينات عند تحميل المحرر
if (typeof CKEDITOR !== 'undefined') {
    CKEDITOR.on('instanceReady', function(evt) {
        const editor = evt.editor;
        
        // تفعيل السحب والإفلات
        enhanceDragAndDrop(editor);
        
        // إضافة أنماط CSS للمحرر
        const styles = `
            .drag-over {
                border: 2px dashed #4CAF50 !important;
                background-color: #f0f8f0 !important;
            }
            .cke_editable {
                transition: all 0.3s ease;
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
        
        console.log('CKEditor Media Enhancements loaded successfully');
    });
}