// CKEditor Upload Fix

// Enhanced image upload functionality
CKEDITOR.on('instanceReady', function(ev) {
    var editor = ev.editor;
    
    // Configure upload settings
    editor.config.filebrowserUploadUrl = '/blog/upload/';
    editor.config.filebrowserImageUploadUrl = '/blog/upload/';
    editor.config.uploadUrl = '/blog/upload/';
    
    // Add upload event handlers
    editor.on('fileUploadRequest', function(evt) {
        var fileLoader = evt.data.fileLoader;
        var formData = new FormData();
        var xhr = fileLoader.xhr;
        
        // Add CSRF token
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            formData.append('csrfmiddlewaretoken', csrfToken.value);
        }
        
        // Add the file
        formData.append('upload', fileLoader.file, fileLoader.fileName);
        
        // Configure XHR
        xhr.open('POST', '/blog/upload/', true);
        xhr.responseType = 'json';
        
        // Handle upload progress
        xhr.upload.addEventListener('progress', function(e) {
            if (e.lengthComputable) {
                fileLoader.update(e.loaded, e.total);
            }
        });
        
        // Handle upload completion
        xhr.addEventListener('load', function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                var response = xhr.response;
                if (response && response.url) {
                    fileLoader.responseData = {
                        url: response.url
                    };
                    fileLoader.fire('uploaded', response);
                } else {
                    fileLoader.fire('error', 'Upload failed: Invalid response');
                }
            } else {
                fileLoader.fire('error', 'Upload failed: ' + xhr.status);
            }
        });
        
        // Handle upload errors
        xhr.addEventListener('error', function() {
            fileLoader.fire('error', 'Upload failed: Network error');
        });
        
        // Send the request
        xhr.send(formData);
        
        // Prevent default upload behavior
        evt.stop();
    });
    
    // Handle paste events for images
    editor.on('paste', function(evt) {
        var data = evt.data;
        var dataTransfer = data.dataTransfer;
        
        if (dataTransfer && dataTransfer.getFilesCount && dataTransfer.getFilesCount() > 0) {
            var files = dataTransfer.getFiles();
            
            for (var i = 0; i < files.length; i++) {
                var file = files[i];
                
                if (file.type && file.type.indexOf('image/') === 0) {
                    // Create file loader
                    var fileLoader = editor.uploadRepository.create(file);
                    
                    // Start upload
                    fileLoader.loadAndUpload('/blog/upload/');
                    
                    // Insert placeholder
                    var img = editor.document.createElement('img');
                    img.setAttribute('src', 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7');
                    img.setAttribute('data-cke-upload-id', fileLoader.id);
                    img.setAttribute('alt', 'Uploading...');
                    
                    editor.insertElement(img);
                    
                    // Handle upload completion
                    fileLoader.on('uploaded', function(evt) {
                        var response = evt.sender.responseData;
                        if (response && response.url) {
                            var uploadedImg = editor.document.findOne('img[data-cke-upload-id="' + fileLoader.id + '"]');
                            if (uploadedImg) {
                                uploadedImg.setAttribute('src', response.url);
                                uploadedImg.removeAttribute('data-cke-upload-id');
                                uploadedImg.setAttribute('alt', '');
                            }
                        }
                    });
                    
                    // Handle upload errors
                    fileLoader.on('error', function() {
                        var failedImg = editor.document.findOne('img[data-cke-upload-id="' + fileLoader.id + '"]');
                        if (failedImg) {
                            failedImg.remove();
                        }
                        
                        // Show error message
                        editor.showNotification('فشل في رفع الصورة. يرجى المحاولة مرة أخرى.', 'warning', 3000);
                    });
                }
            }
        }
    });
    
    // Enhance image dialog
    CKEDITOR.on('dialogDefinition', function(ev) {
        var dialogName = ev.data.name;
        var dialogDefinition = ev.data.definition;
        
        if (dialogName === 'image') {
            // Get the upload tab
            var uploadTab = dialogDefinition.getContents('Upload');
            
            if (uploadTab) {
                // Enhance upload field
                var uploadField = uploadTab.get('upload');
                
                if (uploadField) {
                    // Add drag and drop support
                    uploadField.onShow = function() {
                        var input = this.getInputElement().$;
                        var container = input.parentNode;
                        
                        // Style the container
                        container.style.border = '2px dashed #ccc';
                        container.style.borderRadius = '8px';
                        container.style.padding = '20px';
                        container.style.textAlign = 'center';
                        container.style.backgroundColor = '#f9f9f9';
                        container.style.transition = 'all 0.3s ease';
                        
                        // Add drag and drop events
                        container.addEventListener('dragover', function(e) {
                            e.preventDefault();
                            container.style.borderColor = '#007cba';
                            container.style.backgroundColor = '#f0f8ff';
                        });
                        
                        container.addEventListener('dragleave', function(e) {
                            e.preventDefault();
                            container.style.borderColor = '#ccc';
                            container.style.backgroundColor = '#f9f9f9';
                        });
                        
                        container.addEventListener('drop', function(e) {
                            e.preventDefault();
                            container.style.borderColor = '#ccc';
                            container.style.backgroundColor = '#f9f9f9';
                            
                            var files = e.dataTransfer.files;
                            if (files.length > 0) {
                                input.files = files;
                                input.dispatchEvent(new Event('change'));
                            }
                        });
                        
                        // Add helper text
                        if (!container.querySelector('.upload-helper')) {
                            var helper = document.createElement('div');
                            helper.className = 'upload-helper';
                            helper.innerHTML = '<p style="margin: 10px 0; color: #666; font-size: 14px;">اسحب الصورة هنا أو انقر للاختيار</p><p style="margin: 0; color: #999; font-size: 12px;">الحد الأقصى: 5MB | الأنواع المدعومة: JPG, PNG, GIF, WebP</p>';
                            container.appendChild(helper);
                        }
                    };
                }
            }
        }
    });
});

// Add CSS for upload enhancements
if (!document.getElementById('ckeditor-upload-styles')) {
    var style = document.createElement('style');
    style.id = 'ckeditor-upload-styles';
    style.textContent = `
        .cke_dialog_contents .cke_dialog_ui_fileButton {
            position: relative;
            overflow: hidden;
        }
        
        .cke_dialog_contents .cke_dialog_ui_fileButton input[type="file"] {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            cursor: pointer;
        }
        
        .upload-helper {
            pointer-events: none;
        }
        
        .cke_notification {
            direction: rtl;
            text-align: right;
        }
    `;
    document.head.appendChild(style);
}

console.log('CKEditor upload enhancements loaded');