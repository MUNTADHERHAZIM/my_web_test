// CKEditor URL Image Upload Support

// Add URL image upload functionality
CKEDITOR.on('instanceReady', function(ev) {
    var editor = ev.editor;
    
    // Add custom command for URL image upload
    editor.addCommand('insertImageFromUrl', {
        exec: function(editor) {
            var url = prompt('أدخل رابط الصورة:', 'https://');
            if (url && url.trim() !== '' && url !== 'https://') {
                // Validate URL format
                var urlPattern = /^(https?:\/\/)([\da-z\.-]+)\.([a-z\.]{2,6})([\/ \w \.-]*)*\/?$/;
                if (urlPattern.test(url)) {
                    // Ask for image alt text
                    var altText = prompt('أدخل عنوان الصورة (وصف مختصر):', '');
                    if (altText === null) {
                        return; // User cancelled
                    }
                    
                    // Use default alt text if empty
                    if (!altText || altText.trim() === '') {
                        altText = 'صورة من رابط';
                    }
                    
                    // Create image element
                    var img = editor.document.createElement('img');
                    img.setAttribute('src', url);
                    img.setAttribute('alt', altText.trim());
                    img.setAttribute('style', 'max-width: 100%; height: auto;');
                    
                    // Insert image
                    editor.insertElement(img);
                    
                    // Show success notification
                    editor.showNotification('تم إدراج الصورة بنجاح', 'success', 3000);
                } else {
                    editor.showNotification('رابط الصورة غير صحيح', 'warning', 5000);
                }
            }
        }
    });
    
    // Add button to toolbar
    editor.ui.addButton('InsertImageFromUrl', {
        label: 'إدراج صورة من رابط',
        command: 'insertImageFromUrl',
        toolbar: 'insert',
        icon: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTIgMTJMMTQgMTJMMTQgNEwyIDRMMiAxMloiIHN0cm9rZT0iIzMzMzMzMyIgc3Ryb2tlLXdpZHRoPSIxLjUiIGZpbGw9Im5vbmUiLz4KPGNpcmNsZSBjeD0iNSIgY3k9IjciIHI9IjEuNSIgZmlsbD0iIzMzMzMzMyIvPgo8cGF0aCBkPSJNMTAgMTBMMTIgOEwxNCA5TDE0IDEyTDEwIDEyTDEwIDEwWiIgZmlsbD0iIzMzMzMzMyIvPgo8L3N2Zz4K'
    });
    
    // Enhanced drag and drop functionality
    editor.on('contentDom', function() {
        var editable = editor.editable();
        
        // Add drag over styling
        editable.on('dragover', function(evt) {
            evt.data.preventDefault();
            editable.addClass('cke_drag_over');
        });
        
        editable.on('dragleave', function(evt) {
            editable.removeClass('cke_drag_over');
        });
        
        // Handle file drop
        editable.on('drop', function(evt) {
            evt.data.preventDefault();
            editable.removeClass('cke_drag_over');
            
            var files = evt.data.$.dataTransfer.files;
            if (files.length > 0) {
                for (var i = 0; i < files.length; i++) {
                    var file = files[i];
                    if (file.type.indexOf('image/') === 0) {
                        uploadImageFile(editor, file);
                    }
                }
            }
        });
    });
    
    // Function to upload image file
    function uploadImageFile(editor, file) {
        var formData = new FormData();
        formData.append('upload', file);
        
        // Add CSRF token
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            formData.append('csrfmiddlewaretoken', csrfToken.value);
        }
        
        // Show uploading notification
        var notification = editor.showNotification('جاري رفع الصورة...', 'info');
        
        // Create XMLHttpRequest
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/blog/upload/', true);
        
        xhr.onload = function() {
            notification.hide();
            
            if (xhr.status === 200) {
                try {
                    var response = JSON.parse(xhr.responseText);
                    if (response.url) {
                        // Ask for image alt text
                        var altText = prompt('أدخل عنوان الصورة (وصف مختصر):', response.original_name || '');
                        if (altText === null) {
                            altText = response.original_name || 'صورة مرفوعة';
                        }
                        
                        // Use default alt text if empty
                        if (!altText || altText.trim() === '') {
                            altText = response.original_name || 'صورة مرفوعة';
                        }
                        
                        // Create and insert image
                        var img = editor.document.createElement('img');
                        img.setAttribute('src', response.url);
                        img.setAttribute('alt', altText.trim());
                        img.setAttribute('style', 'max-width: 100%; height: auto;');
                        
                        editor.insertElement(img);
                        editor.showNotification('تم رفع الصورة بنجاح', 'success', 3000);
                    } else {
                        editor.showNotification('خطأ في رفع الصورة: ' + (response.error || 'خطأ غير معروف'), 'warning', 5000);
                    }
                } catch (e) {
                    editor.showNotification('خطأ في معالجة استجابة الخادم', 'warning', 5000);
                }
            } else {
                editor.showNotification('خطأ في رفع الصورة: ' + xhr.status, 'warning', 5000);
            }
        };
        
        xhr.onerror = function() {
            notification.hide();
            editor.showNotification('خطأ في الشبكة أثناء رفع الصورة', 'warning', 5000);
        };
        
        xhr.send(formData);
    }
});

// Add custom styles for drag and drop
if (!document.getElementById('ckeditor-url-upload-styles')) {
    var style = document.createElement('style');
    style.id = 'ckeditor-url-upload-styles';
    style.textContent = `
        .cke_drag_over {
            border: 2px dashed #007cba !important;
            background-color: rgba(0, 124, 186, 0.1) !important;
        }
        
        .cke_notification {
            direction: rtl;
            text-align: right;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .cke_button__insertimagefromurl_icon {
            background-size: 16px 16px !important;
        }
    `;
    document.head.appendChild(style);
}

console.log('CKEditor URL upload support loaded');