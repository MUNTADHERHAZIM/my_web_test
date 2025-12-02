// Language Switcher JavaScript

// Function to get CSRF token from cookies or meta tag
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to get CSRF token
function getCSRFToken() {
    return getCookie('csrftoken') || document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
}

// Function to set language
function setLanguage(languageCode) {
    const csrfToken = getCSRFToken();
    
    if (!csrfToken) {
        console.error('CSRF token not found');
        return;
    }
    
    // Show loading indicator
    showLoadingIndicator();
    
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/i18n/setlang/';
    form.style.display = 'none';
    
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    
    const languageInput = document.createElement('input');
    languageInput.type = 'hidden';
    languageInput.name = 'language';
    languageInput.value = languageCode;
    
    const nextInput = document.createElement('input');
    nextInput.type = 'hidden';
    nextInput.name = 'next';
    nextInput.value = window.location.pathname + window.location.search;
    
    form.appendChild(csrfInput);
    form.appendChild(languageInput);
    form.appendChild(nextInput);
    
    document.body.appendChild(form);
    form.submit();
}

// Function to show loading indicator
function showLoadingIndicator() {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'language-loading';
    loadingDiv.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 9999; display: flex; align-items: center; justify-content: center;">
            <div style="background: white; padding: 20px; border-radius: 8px; text-align: center;">
                <div style="width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 10px;"></div>
                <p style="margin: 0; color: #333;">تغيير اللغة... / Changing language...</p>
            </div>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    `;
    document.body.appendChild(loadingDiv);
}

// Function to update page direction and font based on language
function updatePageDirection(languageCode) {
    const html = document.documentElement;
    const body = document.body;
    
    if (languageCode === 'ar') {
        html.setAttribute('dir', 'rtl');
        html.setAttribute('lang', 'ar');
        body.classList.remove('font-english');
        body.classList.add('font-arabic');
        
        // Update text alignment for main content areas
        updateTextAlignment('rtl');
    } else {
        html.setAttribute('dir', 'ltr');
        html.setAttribute('lang', 'en');
        body.classList.remove('font-arabic');
        body.classList.add('font-english');
        
        // Update text alignment for main content areas
        updateTextAlignment('ltr');
    }
}

// Function to update text alignment
function updateTextAlignment(direction) {
    const contentElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, .card-text, .blog-content, .comment-content');
    
    contentElements.forEach(element => {
        if (direction === 'rtl') {
            element.style.textAlign = 'right';
            element.style.direction = 'rtl';
        } else {
            element.style.textAlign = 'left';
            element.style.direction = 'ltr';
        }
    });
}

// Function to handle language menu toggle
function toggleLanguageMenu() {
    const menu = document.getElementById('language-menu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
}

// Function to close language menu when clicking outside
function closeLanguageMenuOnOutsideClick(event) {
    const menu = document.getElementById('language-menu');
    const button = document.querySelector('[onclick="toggleLanguageMenu()"]');
    
    if (menu && !menu.contains(event.target) && !button.contains(event.target)) {
        menu.classList.add('hidden');
    }
}

// Initialize language switcher when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Language switcher script loaded');
    
    // Language toggle functionality
    const languageToggle = document.getElementById('language-toggle');
    const languageMenu = document.getElementById('language-menu');
    
    console.log('Language toggle element:', languageToggle);
    console.log('Language menu element:', languageMenu);
    
    if (languageToggle && languageMenu) {
        console.log('Both elements found, adding event listeners');
        languageToggle.addEventListener('click', function(e) {
            console.log('Language toggle clicked!');
            e.preventDefault();
            e.stopPropagation();
            if (languageMenu.style.display === 'none' || languageMenu.style.display === '') {
                console.log('Showing menu');
                languageMenu.style.display = 'block';
                languageMenu.style.opacity = '1';
            } else {
                console.log('Hiding menu');
                languageMenu.style.display = 'none';
                languageMenu.style.opacity = '0';
            }
        });
        
        // Close language menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!languageToggle.contains(event.target) && !languageMenu.contains(event.target)) {
                languageMenu.style.display = 'none';
                languageMenu.style.opacity = '0';
            }
        });
    }
    
    // Add event listeners to language toggle links
    const languageLinks = document.querySelectorAll('[data-language]');
    
    languageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const languageCode = this.getAttribute('data-language');
            setLanguage(languageCode);
        });
    });
    
    // Add click outside listener for language menu
    document.addEventListener('click', closeLanguageMenuOnOutsideClick);
    
    // Apply current language direction on page load
    const currentLang = document.documentElement.getAttribute('lang');
    if (currentLang) {
        updatePageDirection(currentLang);
    }
});

// Make functions globally available
window.setLanguage = setLanguage;
window.toggleLanguageMenu = toggleLanguageMenu;
window.updatePageDirection = updatePageDirection;