/**
 * CKEditor File Manager
 * مدير الملفات المتقدم لـ CKEditor
 */

(function() {
    'use strict';

    // إعدادات الملفات المدعومة
    const SUPPORTED_FILES = {
        images: {
            extensions: ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp'],
            maxSize: 5 * 1024 * 1024, // 5MB
            icon: '🖼️'
        },
        videos: {
            extensions: ['mp4', 'webm', 'ogg', 'avi', 'mov', 'wmv'],
            maxSize: 50 * 1024 * 1024, // 50MB
            icon: '🎥'
        },
        audio: {
            extensions: ['mp3', 'wav', 'ogg', 'aac', 'm4a'],
            maxSize: 10 * 1024 * 1024, // 10MB
            icon: '🎵'
        },
        documents: {
            extensions: ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt'],
            maxSize: 10 * 1024 * 1024, // 10MB
            icon: '📄'
        },
        archives: {
            extensions: ['zip', 'rar', '7z', 'tar', 'gz'],
            maxSize: 20 * 1024 * 1024, // 20MB
            icon: '📦'
        }
    };

    // فئة مدير الملفات
    class CKEditorFileManager {
        constructor(editor) {
            this.editor = editor;
            this.uploadQueue = [];
            this.isUploading = false;
            this.init();
        }

        init() {
            this.setupDragAndDrop();
            this.setupPasteHandler();
            this.setupFileInput();
            this.setupProgressBar();
            this.setupMediaGallery();
        }

        // إعداد السحب والإفلات
        setupDragAndDrop() {
            const editable = this.editor.editable();
            
            editable.on('dragover', (evt) => {
                evt.data.preventDefault();
                editable.addClass('drag-over');
            });

            editable.on('dragleave', (evt) => {
                evt.data.preventDefault();
                editable.removeClass('drag-over');
            });

            editable.on('drop', (evt) => {
                evt.data.preventDefault();
                editable.removeClass('drag-over');
                
                const files = evt.data.$.dataTransfer.files;
                if (files.length > 0) {
                    this.handleFiles(Array.from(files));
                }
            });
        }

        // إعداد معالج اللصق
        setupPasteHandler() {
            this.editor.on('paste', (evt) => {
                const clipboardData = evt.data.dataTransfer;
                if (clipboardData && clipboardData.getFilesCount() > 0) {
                    evt.data.preventDefault();
                    
                    const files = [];
                    for (let i = 0; i < clipboardData.getFilesCount(); i++) {
                        files.push(clipboardData.getFile(i));
                    }
                    this.handleFiles(files);
                }
            });
        }

        // إعداد حقل اختيار الملفات
        setupFileInput() {
            // إنشاء حقل مخفي لاختيار الملفات
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.multiple = true;
            fileInput.accept = this.getAllowedExtensions();
            fileInput.style.display = 'none';
            document.body.appendChild(fileInput);

            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    this.handleFiles(Array.from(e.target.files));
                }
            });

            // إضافة أمر لفتح حوار اختيار الملفات
            this.editor.addCommand('selectFiles', {
                exec: () => {
                    fileInput.click();
                }
            });

            // إضافة زر في شريط الأدوات
            this.editor.ui.addButton('SelectFiles', {
                label: 'رفع ملفات',
                command: 'selectFiles',
                toolbar: 'insert',
                icon: 'data:image/svg+xml;base64,' + btoa(`
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
                        <path d="M12,11L16,15H13V19H11V15H8L12,11Z" />
                    </svg>
                `)
            });
        }

        // إعداد شريط التقدم
        setupProgressBar() {
            const progressContainer = document.createElement('div');
            progressContainer.id = 'upload-progress-container';
            progressContainer.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                width: 300px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                padding: 16px;
                z-index: 10000;
                display: none;
                border: 2px solid #4f46e5;
            `;
            
            progressContainer.innerHTML = `
                <div style="display: flex; align-items: center; margin-bottom: 12px;">
                    <span style="font-weight: 600; color: #2d3748;">جاري الرفع...</span>
                    <button id="cancel-upload" style="margin-right: auto; background: #e53e3e; color: white; border: none; border-radius: 4px; padding: 4px 8px; cursor: pointer;">إلغاء</button>
                </div>
                <div id="upload-progress-bar" style="width: 100%; height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden;">
                    <div id="upload-progress-fill" style="height: 100%; background: linear-gradient(90deg, #4f46e5, #7c3aed); width: 0%; transition: width 0.3s ease;"></div>
                </div>
                <div id="upload-status" style="margin-top: 8px; font-size: 14px; color: #718096;"></div>
            `;
            
            document.body.appendChild(progressContainer);
            
            // إعداد زر الإلغاء
            document.getElementById('cancel-upload').addEventListener('click', () => {
                this.cancelUpload();
            });
        }

        // إعداد معرض الوسائط
        setupMediaGallery() {
            // إضافة أمر لفتح معرض الوسائط
            this.editor.addCommand('openMediaGallery', {
                exec: () => {
                    this.openMediaGallery();
                }
            });

            // إضافة زر في شريط الأدوات
            this.editor.ui.addButton('MediaGallery', {
                label: 'معرض الوسائط',
                command: 'openMediaGallery',
                toolbar: 'insert',
                icon: 'data:image/svg+xml;base64,' + btoa(`
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M5,3A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3H5M5,5H19V19H5V5M13.96,12.71L11.21,15.46L9.25,13.5L6.5,16.25H17.5L13.96,12.71Z" />
                    </svg>
                `)
            });
        }

        // معالجة الملفات
        handleFiles(files) {
            const validFiles = [];
            const errors = [];

            files.forEach(file => {
                const validation = this.validateFile(file);
                if (validation.valid) {
                    validFiles.push(file);
                } else {
                    errors.push(`${file.name}: ${validation.error}`);
                }
            });

            if (errors.length > 0) {
                this.showNotification('تحذير', errors.join('\n'), 'warning');
            }

            if (validFiles.length > 0) {
                this.uploadFiles(validFiles);
            }
        }

        // التحقق من صحة الملف
        validateFile(file) {
            const extension = file.name.split('.').pop().toLowerCase();
            let fileType = null;
            let maxSize = 0;

            // تحديد نوع الملف
            for (const [type, config] of Object.entries(SUPPORTED_FILES)) {
                if (config.extensions.includes(extension)) {
                    fileType = type;
                    maxSize = config.maxSize;
                    break;
                }
            }

            if (!fileType) {
                return {
                    valid: false,
                    error: `نوع الملف غير مدعوم (.${extension})`
                };
            }

            if (file.size > maxSize) {
                return {
                    valid: false,
                    error: `حجم الملف كبير جداً (الحد الأقصى: ${this.formatFileSize(maxSize)})`
                };
            }

            return { valid: true, type: fileType };
        }

        // رفع الملفات
        async uploadFiles(files) {
            if (this.isUploading) {
                this.uploadQueue.push(...files);
                return;
            }

            this.isUploading = true;
            this.showProgressBar();

            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                try {
                    this.updateProgress((i / files.length) * 100, `رفع ${file.name}...`);
                    const result = await this.uploadSingleFile(file);
                    this.insertFileIntoEditor(result, file);
                } catch (error) {
                    console.error('خطأ في رفع الملف:', error);
                    this.showNotification('خطأ', `فشل في رفع ${file.name}`, 'error');
                }
            }

            this.updateProgress(100, 'تم الرفع بنجاح!');
            setTimeout(() => {
                this.hideProgressBar();
                this.isUploading = false;
                
                // معالجة الملفات في الطابور
                if (this.uploadQueue.length > 0) {
                    const queuedFiles = [...this.uploadQueue];
                    this.uploadQueue = [];
                    this.uploadFiles(queuedFiles);
                }
            }, 1500);
        }

        // رفع ملف واحد
        async uploadSingleFile(file) {
            const formData = new FormData();
            formData.append('upload', file);
            formData.append('csrfmiddlewaretoken', this.getCSRFToken());

            const response = await fetch('/blog/upload/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        }

        // إدراج الملف في المحرر
        insertFileIntoEditor(uploadResult, file) {
            const extension = file.name.split('.').pop().toLowerCase();
            const fileType = this.getFileType(extension);
            
            let html = '';
            
            switch (fileType) {
                case 'images':
                    html = `<img src="${uploadResult.url}" alt="${file.name}" style="max-width: 100%; height: auto;" />`;
                    break;
                    
                case 'videos':
                    html = `<video controls style="max-width: 100%; height: auto;">
                        <source src="${uploadResult.url}" type="${file.type}">
                        متصفحك لا يدعم تشغيل الفيديو.
                    </video>`;
                    break;
                    
                case 'audio':
                    html = `<audio controls style="width: 100%;">
                        <source src="${uploadResult.url}" type="${file.type}">
                        متصفحك لا يدعم تشغيل الصوت.
                    </audio>`;
                    break;
                    
                default:
                    const icon = SUPPORTED_FILES[fileType]?.icon || '📎';
                    html = `<a href="${uploadResult.url}" target="_blank" style="display: inline-block; padding: 8px 12px; background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 6px; text-decoration: none; color: #2d3748; margin: 4px;">
                        <span style="font-size: 18px; margin-left: 8px;">${icon}</span>
                        ${file.name}
                        <span style="font-size: 12px; color: #718096; margin-right: 8px;">(${this.formatFileSize(file.size)})</span>
                    </a>`;
            }
            
            this.editor.insertHtml(html);
        }

        // فتح معرض الوسائط
        openMediaGallery() {
            // إنشاء نافذة معرض الوسائط
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                z-index: 10001;
                display: flex;
                align-items: center;
                justify-content: center;
            `;
            
            modal.innerHTML = `
                <div style="background: white; border-radius: 12px; width: 90%; max-width: 800px; height: 80%; display: flex; flex-direction: column;">
                    <div style="padding: 20px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0; color: #2d3748;">معرض الوسائط</h3>
                        <button id="close-gallery" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #718096;">×</button>
                    </div>
                    <div style="flex: 1; padding: 20px; overflow-y: auto;">
                        <div id="media-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 16px;">
                            <div style="text-align: center; color: #718096; grid-column: 1 / -1;">جاري تحميل الوسائط...</div>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // إغلاق المعرض
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    document.body.removeChild(modal);
                }
            });
            
            document.getElementById('close-gallery').addEventListener('click', () => {
                document.body.removeChild(modal);
            });
            
            // تحميل الوسائط
            this.loadMediaGallery();
        }

        // تحميل معرض الوسائط
        async loadMediaGallery() {
            try {
                const response = await fetch('/blog/browse/', {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    this.renderMediaGallery(data.files || []);
                } else {
                    throw new Error('فشل في تحميل الوسائط');
                }
            } catch (error) {
                console.error('خطأ في تحميل المعرض:', error);
                document.getElementById('media-grid').innerHTML = '<div style="text-align: center; color: #e53e3e; grid-column: 1 / -1;">فشل في تحميل الوسائط</div>';
            }
        }

        // عرض معرض الوسائط
        renderMediaGallery(files) {
            const grid = document.getElementById('media-grid');
            
            if (files.length === 0) {
                grid.innerHTML = '<div style="text-align: center; color: #718096; grid-column: 1 / -1;">لا توجد ملفات</div>';
                return;
            }
            
            grid.innerHTML = files.map(file => {
                const isImage = file.type && file.type.startsWith('image/');
                return `
                    <div class="media-item" data-url="${file.url}" data-name="${file.name}" style="
                        border: 2px solid #e2e8f0;
                        border-radius: 8px;
                        padding: 8px;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        text-align: center;
                    " onmouseover="this.style.borderColor='#4f46e5'; this.style.transform='scale(1.05)'" onmouseout="this.style.borderColor='#e2e8f0'; this.style.transform='scale(1)'">
                        ${isImage ? 
                            `<img src="${file.url}" alt="${file.name}" style="width: 100%; height: 100px; object-fit: cover; border-radius: 4px;">` :
                            `<div style="height: 100px; display: flex; align-items: center; justify-content: center; background: #f7fafc; border-radius: 4px; font-size: 32px;">${this.getFileIcon(file.name)}</div>`
                        }
                        <div style="margin-top: 8px; font-size: 12px; color: #2d3748; word-break: break-all;">${file.name}</div>
                    </div>
                `;
            }).join('');
            
            // إضافة مستمعي الأحداث
            grid.querySelectorAll('.media-item').forEach(item => {
                item.addEventListener('click', () => {
                    const url = item.dataset.url;
                    const name = item.dataset.name;
                    const extension = name.split('.').pop().toLowerCase();
                    const fileType = this.getFileType(extension);
                    
                    let html = '';
                    switch (fileType) {
                        case 'images':
                            html = `<img src="${url}" alt="${name}" style="max-width: 100%; height: auto;" />`;
                            break;
                        case 'videos':
                            html = `<video controls style="max-width: 100%; height: auto;"><source src="${url}">متصفحك لا يدعم تشغيل الفيديو.</video>`;
                            break;
                        case 'audio':
                            html = `<audio controls style="width: 100%;"><source src="${url}">متصفحك لا يدعم تشغيل الصوت.</audio>`;
                            break;
                        default:
                            const icon = this.getFileIcon(name);
                            html = `<a href="${url}" target="_blank" style="display: inline-block; padding: 8px 12px; background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 6px; text-decoration: none; color: #2d3748; margin: 4px;"><span style="font-size: 18px; margin-left: 8px;">${icon}</span>${name}</a>`;
                    }
                    
                    this.editor.insertHtml(html);
                    document.querySelector('[id*="close-gallery"]').click();
                });
            });
        }

        // الحصول على نوع الملف
        getFileType(extension) {
            for (const [type, config] of Object.entries(SUPPORTED_FILES)) {
                if (config.extensions.includes(extension)) {
                    return type;
                }
            }
            return 'documents';
        }

        // الحصول على أيقونة الملف
        getFileIcon(filename) {
            const extension = filename.split('.').pop().toLowerCase();
            const fileType = this.getFileType(extension);
            return SUPPORTED_FILES[fileType]?.icon || '📎';
        }

        // الحصول على الامتدادات المسموحة
        getAllowedExtensions() {
            const extensions = [];
            Object.values(SUPPORTED_FILES).forEach(config => {
                extensions.push(...config.extensions.map(ext => `.${ext}`));
            });
            return extensions.join(',');
        }

        // تنسيق حجم الملف
        formatFileSize(bytes) {
            if (bytes === 0) return '0 بايت';
            const k = 1024;
            const sizes = ['بايت', 'كيلوبايت', 'ميجابايت', 'جيجابايت'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        // عرض شريط التقدم
        showProgressBar() {
            document.getElementById('upload-progress-container').style.display = 'block';
        }

        // إخفاء شريط التقدم
        hideProgressBar() {
            document.getElementById('upload-progress-container').style.display = 'none';
        }

        // تحديث التقدم
        updateProgress(percent, status) {
            document.getElementById('upload-progress-fill').style.width = percent + '%';
            document.getElementById('upload-status').textContent = status;
        }

        // إلغاء الرفع
        cancelUpload() {
            this.isUploading = false;
            this.uploadQueue = [];
            this.hideProgressBar();
            this.showNotification('تم الإلغاء', 'تم إلغاء عملية الرفع', 'info');
        }

        // عرض الإشعارات
        showNotification(title, message, type = 'info') {
            const colors = {
                info: '#4f46e5',
                success: '#10b981',
                warning: '#f59e0b',
                error: '#e53e3e'
            };

            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                left: 20px;
                background: white;
                border: 2px solid ${colors[type]};
                border-radius: 8px;
                padding: 16px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 10002;
                max-width: 300px;
                animation: slideIn 0.3s ease;
            `;

            notification.innerHTML = `
                <div style="font-weight: 600; color: ${colors[type]}; margin-bottom: 8px;">${title}</div>
                <div style="color: #2d3748; white-space: pre-line;">${message}</div>
            `;

            document.body.appendChild(notification);

            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => {
                    if (notification.parentNode) {
                        document.body.removeChild(notification);
                    }
                }, 300);
            }, 5000);
        }

        // الحصول على رمز CSRF
        getCSRFToken() {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'csrftoken') {
                    return value;
                }
            }
            return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
        }
    }

    // تهيئة مدير الملفات عند تحميل CKEditor
    if (typeof CKEDITOR !== 'undefined') {
        CKEDITOR.on('instanceReady', function(evt) {
            const editor = evt.editor;
            editor.fileManager = new CKEditorFileManager(editor);
            console.log('تم تهيئة مدير الملفات المتقدم');
        });
    }

    // إضافة أنماط CSS للحركات
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(-100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);

})();