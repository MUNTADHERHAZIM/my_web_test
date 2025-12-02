// إصلاح مشاكل عناصر span و iframe في CKEditor
(function() {
    'use strict';

    // انتظار تحميل CKEditor
    function waitForCKEditor(callback) {
        if (typeof CKEDITOR !== 'undefined') {
            callback();
        } else {
            setTimeout(function() {
                waitForCKEditor(callback);
            }, 100);
        }
    }

    waitForCKEditor(function() {
        // إعداد معالج الأحداث عند إنشاء محرر جديد
        CKEDITOR.on('instanceReady', function(event) {
            var editor = event.editor;
            
            // إصلاح مشكلة عناصر span
            editor.on('paste', function(evt) {
                var data = evt.data;
                if (data && data.dataValue) {
                    // السماح بعناصر span مع جميع الخصائص
                    data.dataValue = data.dataValue.replace(/<span([^>]*)>/gi, '<span$1>');
                }
            });

            // إصلاح مشكلة عناصر iframe
            editor.on('paste', function(evt) {
                var data = evt.data;
                if (data && data.dataValue) {
                    // السماح بعناصر iframe مع جميع الخصائص
                    data.dataValue = data.dataValue.replace(/<iframe([^>]*)>/gi, '<iframe$1>');
                }
            });

            // إضافة دعم إضافي لعناصر span في شريط الأدوات
            if (editor.ui.addButton) {
                editor.ui.addButton('SpanElement', {
                    label: 'إدراج عنصر Span',
                    command: 'insertSpan',
                    toolbar: 'insert'
                });

                editor.addCommand('insertSpan', {
                    exec: function(editor) {
                        var selection = editor.getSelection();
                        var selectedText = selection.getSelectedText();
                        
                        if (selectedText) {
                            var spanElement = new CKEDITOR.dom.element('span');
                            spanElement.setText(selectedText);
                            spanElement.setAttribute('class', 'custom-span');
                            
                            editor.insertElement(spanElement);
                        } else {
                            var spanHtml = '<span class="custom-span">نص داخل span</span>';
                            editor.insertHtml(spanHtml);
                        }
                    }
                });
            }

            // إضافة دعم محسن لعناصر iframe
            if (editor.ui.addButton) {
                editor.ui.addButton('IframeElement', {
                    label: 'إدراج إطار مضمن (iframe)',
                    command: 'insertIframe',
                    toolbar: 'insert'
                });

                editor.addCommand('insertIframe', {
                    exec: function(editor) {
                        var url = prompt('أدخل رابط الإطار المضمن:', 'https://example.com');
                        if (url) {
                            var iframeHtml = '<iframe src="' + url + '" width="100%" height="400" frameborder="0" allowfullscreen></iframe>';
                            editor.insertHtml(iframeHtml);
                        }
                    }
                });
            }

            // تحسين معالجة البيانات المدخلة
            editor.on('setData', function(evt) {
                var data = evt.data;
                if (data && data.dataValue) {
                    // التأكد من عدم إزالة عناصر span و iframe
                    data.dataValue = data.dataValue.replace(/&lt;span/gi, '<span');
                    data.dataValue = data.dataValue.replace(/&lt;\/span&gt;/gi, '</span>');
                    data.dataValue = data.dataValue.replace(/&lt;iframe/gi, '<iframe');
                    data.dataValue = data.dataValue.replace(/&lt;\/iframe&gt;/gi, '</iframe>');
                }
            });

            // تحسين معالجة البيانات المخرجة
            editor.on('getData', function(evt) {
                var data = evt.data;
                if (data && data.dataValue) {
                    // التأكد من الحفاظ على عناصر span و iframe
                    data.dataValue = data.dataValue.replace(/<span([^>]*)>/gi, '<span$1>');
                    data.dataValue = data.dataValue.replace(/<iframe([^>]*)>/gi, '<iframe$1>');
                }
            });

            // إضافة أنماط CSS مخصصة للعناصر
            if (editor.addContentsCss) {
                var customCSS = `
                    .custom-span {
                        background-color: #f0f8ff;
                        padding: 2px 4px;
                        border-radius: 3px;
                        border: 1px solid #ddd;
                    }
                    iframe {
                        max-width: 100%;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }
                `;
                
                // إضافة الأنماط إلى محتوى المحرر
                var head = editor.document.getHead();
                var style = new CKEDITOR.dom.element('style');
                style.setAttribute('type', 'text/css');
                style.appendText(customCSS);
                head.append(style);
            }

            console.log('تم تطبيق إصلاحات عناصر span و iframe بنجاح');
        });

        // إعداد فلتر البيانات العام
        CKEDITOR.on('instanceCreated', function(event) {
            var editor = event.editor;
            
            editor.on('configLoaded', function() {
                // إضافة قواعد فلترة مخصصة
                editor.config.allowedContent = true;
                editor.config.extraAllowedContent = 'iframe[*]; span[*]{*}; div[*]{*}';
                
                // تعطيل الفلترة التلقائية للعناصر
                editor.config.removeFormatAttributes = '';
                editor.config.removeFormatTags = '';
            });
        });
    });
})();