// CKEditor Enhancements

// Wait for CKEditor to be ready
CKEDITOR.on('instanceReady', function(ev) {
    var editor = ev.editor;
    
    // Enhanced RTL support
    editor.on('contentDom', function() {
        var editable = editor.editable();
        
        // Set initial RTL direction
        editable.setAttribute('dir', 'rtl');
        editable.setStyle('text-align', 'right');
        editable.setStyle('direction', 'rtl');
        
        // Add RTL class to editor body
        var body = editable.$;
        if (body) {
            body.classList.add('cke_contents_rtl');
            body.style.direction = 'rtl';
            body.style.textAlign = 'right';
        }
        
        // Dynamic direction detection
        editable.attachListener(editable, 'keyup', function() {
            var content = editable.getText();
            var arabicRegex = /[\u0600-\u06FF]/;
            var englishRegex = /[a-zA-Z]/;
            
            if (arabicRegex.test(content) || content.trim() === '') {
                editable.setAttribute('dir', 'rtl');
                editable.setStyle('text-align', 'right');
                editable.setStyle('direction', 'rtl');
                if (body) {
                    body.style.direction = 'rtl';
                    body.style.textAlign = 'right';
                }
            } else if (englishRegex.test(content) && !arabicRegex.test(content)) {
                editable.setAttribute('dir', 'ltr');
                editable.setStyle('text-align', 'left');
                editable.setStyle('direction', 'ltr');
                if (body) {
                    body.style.direction = 'ltr';
                    body.style.textAlign = 'left';
                }
            }
        });
        
        // Handle paste events to maintain direction
        editable.attachListener(editable, 'paste', function() {
            setTimeout(function() {
                var content = editable.getText();
                var arabicRegex = /[\u0600-\u06FF]/;
                
                if (arabicRegex.test(content)) {
                    editable.setAttribute('dir', 'rtl');
                    editable.setStyle('text-align', 'right');
                    editable.setStyle('direction', 'rtl');
                }
            }, 100);
        });
    });
    
    // Set editor UI direction
    var editorElement = editor.element.$;
    if (editorElement) {
        editorElement.style.direction = 'rtl';
    }
    
    // Enhance code snippets after content is loaded
    editor.on('contentDom', function() {
        enhanceCodeSnippets(editor);
    });
    
    // Re-enhance code snippets when content changes
    editor.on('change', function() {
        setTimeout(function() {
            enhanceCodeSnippets(editor);
        }, 100);
    });
});

// Function to enhance code snippets
function enhanceCodeSnippets(editor) {
    var editable = editor.editable();
    if (!editable) return;
    
    var codeSnippets = editable.find('.cke_codesnippet');
    
    codeSnippets.forEach(function(snippet) {
        if (snippet.hasClass('enhanced')) return;
        
        snippet.addClass('enhanced');
        
        // Get language from data attribute
        var lang = snippet.getAttribute('data-cke-codesnippet-lang') || 'text';
        
        // Create language label
        var langLabel = new CKEDITOR.dom.element('span');
        langLabel.addClass('lang-label');
        langLabel.setText(getLanguageDisplayName(lang));
        langLabel.setStyles({
            'position': 'absolute',
            'top': '0',
            'right': '0',
            'background': 'rgba(0, 0, 0, 0.8)',
            'color': '#fff',
            'padding': '4px 8px',
            'font-size': '12px',
            'font-family': 'Courier New, monospace',
            'text-transform': 'uppercase',
            'border-bottom-left-radius': '4px',
            'z-index': '10'
        });
        
        // Create copy button
        var copyBtn = new CKEDITOR.dom.element('button');
        copyBtn.addClass('copy-btn');
        copyBtn.setText('نسخ');
        copyBtn.setStyles({
            'position': 'absolute',
            'top': '8px',
            'left': '8px',
            'background': '#007cba',
            'color': 'white',
            'border': 'none',
            'padding': '4px 8px',
            'border-radius': '4px',
            'font-size': '11px',
            'cursor': 'pointer',
            'opacity': '0',
            'transition': 'opacity 0.3s ease',
            'z-index': '10'
        });
        
        // Add hover effects
        snippet.on('mouseenter', function() {
            copyBtn.setStyle('opacity', '1');
        });
        
        snippet.on('mouseleave', function() {
            copyBtn.setStyle('opacity', '0');
        });
        
        // Add copy functionality
        copyBtn.on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            var codeText = snippet.getText();
            
            // Try to copy to clipboard
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(codeText).then(function() {
                    showCopySuccess(copyBtn);
                }).catch(function() {
                    fallbackCopyTextToClipboard(codeText, copyBtn);
                });
            } else {
                fallbackCopyTextToClipboard(codeText, copyBtn);
            }
        });
        
        // Make snippet container relative for absolute positioning
        snippet.setStyle('position', 'relative');
        
        // Append elements
        snippet.append(langLabel);
        snippet.append(copyBtn);
    });
}

// Get display name for programming language
function getLanguageDisplayName(lang) {
    var languages = {
        'python': 'Python',
        'javascript': 'JavaScript',
        'html': 'HTML',
        'css': 'CSS',
        'php': 'PHP',
        'java': 'Java',
        'cpp': 'C++',
        'csharp': 'C#',
        'sql': 'SQL',
        'bash': 'Bash',
        'json': 'JSON',
        'xml': 'XML',
        'text': 'نص'
    };
    
    return languages[lang] || lang.toUpperCase();
}

// Fallback copy function for older browsers
function fallbackCopyTextToClipboard(text, button) {
    var textArea = document.createElement('textarea');
    textArea.value = text;
    
    // Avoid scrolling to bottom
    textArea.style.top = '0';
    textArea.style.left = '0';
    textArea.style.position = 'fixed';
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        var successful = document.execCommand('copy');
        if (successful) {
            showCopySuccess(button);
        }
    } catch (err) {
        console.error('فشل في نسخ النص: ', err);
    }
    
    document.body.removeChild(textArea);
}

// Show copy success message
function showCopySuccess(button) {
    var originalText = button.getText();
    button.setText('تم النسخ!');
    button.setStyle('background', '#48bb78');
    
    setTimeout(function() {
        button.setText(originalText);
        button.setStyle('background', '#007cba');
    }, 2000);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        initializeCKEditorEnhancements();
    });
} else {
    initializeCKEditorEnhancements();
}

function initializeCKEditorEnhancements() {
    // Additional initialization if needed
    console.log('CKEditor enhancements loaded');
}