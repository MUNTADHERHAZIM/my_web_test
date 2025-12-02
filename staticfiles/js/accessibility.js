// Accessibility Enhancements for Muntazir Portfolio
// WCAG 2.1 AA Compliance JavaScript

(function() {
    'use strict';

    // Accessibility manager class
    class AccessibilityManager {
        constructor() {
            this.isKeyboardUser = false;
            this.focusableElements = 'a[href], button, input, textarea, select, details, [tabindex]:not([tabindex="-1"])';
            this.init();
        }

        init() {
            this.detectKeyboardUser();
            this.enhanceFocusManagement();
            this.addSkipLinks();
            this.enhanceFormAccessibility();
            this.improveNavigationAccessibility();
            this.addARIALabels();
            this.handleModalAccessibility();
            this.enhanceTableAccessibility();
            this.addLiveRegions();
            this.handleReducedMotion();
            this.improveColorContrast();
        }

        // Detect keyboard users
        detectKeyboardUser() {
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    this.isKeyboardUser = true;
                    document.body.classList.add('keyboard-navigation');
                }
            });

            document.addEventListener('mousedown', () => {
                this.isKeyboardUser = false;
                document.body.classList.remove('keyboard-navigation');
            });
        }

        // Enhanced focus management
        enhanceFocusManagement() {
            // Focus trap for modals
            this.setupFocusTrap();
            
            // Focus restoration
            this.setupFocusRestoration();
            
            // Skip to main content
            this.setupSkipToMain();
        }

        setupFocusTrap() {
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    const modal = document.querySelector('.modal[aria-hidden="false"]');
                    if (modal) {
                        this.trapFocus(e, modal);
                    }
                }
            });
        }

        trapFocus(e, container) {
            const focusableElements = container.querySelectorAll(this.focusableElements);
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];

            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        }

        setupFocusRestoration() {
            let lastFocusedElement = null;

            document.addEventListener('focusin', (e) => {
                if (!e.target.closest('.modal')) {
                    lastFocusedElement = e.target;
                }
            });

            // Restore focus when modal closes
            document.addEventListener('modalClosed', () => {
                if (lastFocusedElement) {
                    lastFocusedElement.focus();
                }
            });
        }

        setupSkipToMain() {
            const skipLink = document.querySelector('.skip-link');
            if (skipLink) {
                skipLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    const mainContent = document.querySelector('main, #main, .main-content');
                    if (mainContent) {
                        mainContent.focus();
                        mainContent.scrollIntoView({ behavior: 'smooth' });
                    }
                });
            }
        }

        // Add skip links if they don't exist
        addSkipLinks() {
            if (!document.querySelector('.skip-link')) {
                const skipLink = document.createElement('a');
                skipLink.href = '#main';
                skipLink.className = 'skip-link';
                skipLink.textContent = 'Skip to main content';
                skipLink.setAttribute('aria-label', 'Skip to main content');
                document.body.insertBefore(skipLink, document.body.firstChild);
            }
        }

        // Enhanced form accessibility
        enhanceFormAccessibility() {
            const forms = document.querySelectorAll('form');
            
            forms.forEach(form => {
                this.addFormValidation(form);
                this.enhanceFormLabels(form);
                this.addFormInstructions(form);
            });
        }

        addFormValidation(form) {
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                // Add ARIA attributes
                if (input.hasAttribute('required')) {
                    input.setAttribute('aria-required', 'true');
                }

                // Real-time validation
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });

                input.addEventListener('input', () => {
                    if (input.getAttribute('aria-invalid') === 'true') {
                        this.validateField(input);
                    }
                });
            });

            // Form submission validation
            form.addEventListener('submit', (e) => {
                let isValid = true;
                inputs.forEach(input => {
                    if (!this.validateField(input)) {
                        isValid = false;
                    }
                });

                if (!isValid) {
                    e.preventDefault();
                    const firstInvalid = form.querySelector('[aria-invalid="true"]');
                    if (firstInvalid) {
                        firstInvalid.focus();
                        this.announceToScreenReader('Please correct the errors in the form');
                    }
                }
            });
        }

        validateField(input) {
            const isValid = input.checkValidity();
            const errorId = input.id + '-error';
            let errorElement = document.getElementById(errorId);

            if (!isValid) {
                input.setAttribute('aria-invalid', 'true');
                
                if (!errorElement) {
                    errorElement = document.createElement('div');
                    errorElement.id = errorId;
                    errorElement.className = 'form-error';
                    errorElement.setAttribute('role', 'alert');
                    input.parentNode.appendChild(errorElement);
                }
                
                errorElement.textContent = input.validationMessage;
                input.setAttribute('aria-describedby', errorId);
            } else {
                input.setAttribute('aria-invalid', 'false');
                if (errorElement) {
                    errorElement.remove();
                    input.removeAttribute('aria-describedby');
                }
            }

            return isValid;
        }

        enhanceFormLabels(form) {
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                if (!input.getAttribute('aria-label') && !input.getAttribute('aria-labelledby')) {
                    const label = form.querySelector(`label[for="${input.id}"]`);
                    if (!label && input.id) {
                        // Create label if it doesn't exist
                        const newLabel = document.createElement('label');
                        newLabel.setAttribute('for', input.id);
                        newLabel.textContent = input.placeholder || input.name || 'Input field';
                        newLabel.className = 'sr-only';
                        input.parentNode.insertBefore(newLabel, input);
                    }
                }
            });
        }

        addFormInstructions(form) {
            const requiredFields = form.querySelectorAll('[required]');
            if (requiredFields.length > 0) {
                let instructionsElement = form.querySelector('.form-instructions');
                if (!instructionsElement) {
                    instructionsElement = document.createElement('div');
                    instructionsElement.className = 'form-instructions';
                    instructionsElement.textContent = 'Fields marked with * are required';
                    instructionsElement.setAttribute('aria-live', 'polite');
                    form.insertBefore(instructionsElement, form.firstChild);
                }
            }
        }

        // Improve navigation accessibility
        improveNavigationAccessibility() {
            const navElements = document.querySelectorAll('nav');
            
            navElements.forEach(nav => {
                if (!nav.getAttribute('aria-label') && !nav.getAttribute('aria-labelledby')) {
                    nav.setAttribute('aria-label', 'Navigation');
                }

                // Add current page indicator
                const currentLink = nav.querySelector('a[href="' + window.location.pathname + '"]');
                if (currentLink) {
                    currentLink.setAttribute('aria-current', 'page');
                }
            });

            // Mobile menu accessibility
            const mobileMenuButton = document.querySelector('.mobile-menu-button');
            const mobileMenu = document.querySelector('.mobile-menu');
            
            if (mobileMenuButton && mobileMenu) {
                mobileMenuButton.setAttribute('aria-expanded', 'false');
                mobileMenuButton.setAttribute('aria-controls', mobileMenu.id || 'mobile-menu');
                
                mobileMenuButton.addEventListener('click', () => {
                    const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
                    mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
                    mobileMenu.setAttribute('aria-hidden', isExpanded);
                });
            }
        }

        // Add ARIA labels and descriptions
        addARIALabels() {
            // Images without alt text
            const images = document.querySelectorAll('img:not([alt])');
            images.forEach(img => {
                img.setAttribute('alt', '');
                img.setAttribute('role', 'presentation');
            });

            // Buttons without accessible names
            const buttons = document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])');
            buttons.forEach(button => {
                if (!button.textContent.trim()) {
                    const icon = button.querySelector('i, svg');
                    if (icon) {
                        button.setAttribute('aria-label', 'Button');
                    }
                }
            });

            // Links without accessible names
            const links = document.querySelectorAll('a:not([aria-label]):not([aria-labelledby])');
            links.forEach(link => {
                if (!link.textContent.trim()) {
                    link.setAttribute('aria-label', 'Link');
                }
            });
        }

        // Modal accessibility
        handleModalAccessibility() {
            const modals = document.querySelectorAll('.modal');
            
            modals.forEach(modal => {
                modal.setAttribute('role', 'dialog');
                modal.setAttribute('aria-modal', 'true');
                modal.setAttribute('aria-hidden', 'true');
                
                const closeButton = modal.querySelector('.modal-close');
                if (closeButton) {
                    closeButton.setAttribute('aria-label', 'Close modal');
                    
                    closeButton.addEventListener('click', () => {
                        this.closeModal(modal);
                    });
                }

                // Close on Escape key
                modal.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape') {
                        this.closeModal(modal);
                    }
                });
            });
        }

        closeModal(modal) {
            modal.setAttribute('aria-hidden', 'true');
            modal.style.display = 'none';
            document.dispatchEvent(new CustomEvent('modalClosed'));
        }

        // Table accessibility
        enhanceTableAccessibility() {
            const tables = document.querySelectorAll('table');
            
            tables.forEach(table => {
                // Add table role if not present
                if (!table.getAttribute('role')) {
                    table.setAttribute('role', 'table');
                }

                // Add caption if not present
                if (!table.querySelector('caption')) {
                    const caption = document.createElement('caption');
                    caption.textContent = 'Data table';
                    caption.className = 'sr-only';
                    table.insertBefore(caption, table.firstChild);
                }

                // Add scope to headers
                const headers = table.querySelectorAll('th');
                headers.forEach(header => {
                    if (!header.getAttribute('scope')) {
                        const isColumnHeader = header.parentNode.parentNode.tagName.toLowerCase() === 'thead';
                        header.setAttribute('scope', isColumnHeader ? 'col' : 'row');
                    }
                });
            });
        }

        // Add live regions for dynamic content
        addLiveRegions() {
            if (!document.querySelector('[aria-live]')) {
                const liveRegion = document.createElement('div');
                liveRegion.setAttribute('aria-live', 'polite');
                liveRegion.setAttribute('aria-atomic', 'true');
                liveRegion.className = 'sr-only';
                liveRegion.id = 'live-region';
                document.body.appendChild(liveRegion);
            }
        }

        // Announce messages to screen readers
        announceToScreenReader(message) {
            const liveRegion = document.getElementById('live-region');
            if (liveRegion) {
                liveRegion.textContent = message;
                setTimeout(() => {
                    liveRegion.textContent = '';
                }, 1000);
            }
        }

        // Handle reduced motion preferences
        handleReducedMotion() {
            const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
            
            if (prefersReducedMotion.matches) {
                document.body.classList.add('reduced-motion');
                
                // Disable auto-playing animations
                const animations = document.querySelectorAll('[data-animation]');
                animations.forEach(element => {
                    element.style.animation = 'none';
                });
            }
        }

        // Improve color contrast
        improveColorContrast() {
            const prefersHighContrast = window.matchMedia('(prefers-contrast: high)');
            
            if (prefersHighContrast.matches) {
                document.body.classList.add('high-contrast');
            }
        }

        // Keyboard shortcuts
        setupKeyboardShortcuts() {
            document.addEventListener('keydown', (e) => {
                // Alt + 1: Skip to main content
                if (e.altKey && e.key === '1') {
                    e.preventDefault();
                    const main = document.querySelector('main, #main, .main-content');
                    if (main) {
                        main.focus();
                        main.scrollIntoView({ behavior: 'smooth' });
                    }
                }

                // Alt + 2: Skip to navigation
                if (e.altKey && e.key === '2') {
                    e.preventDefault();
                    const nav = document.querySelector('nav');
                    if (nav) {
                        const firstLink = nav.querySelector('a');
                        if (firstLink) {
                            firstLink.focus();
                        }
                    }
                }

                // Alt + 3: Skip to search
                if (e.altKey && e.key === '3') {
                    e.preventDefault();
                    const search = document.querySelector('input[type="search"], .search-input');
                    if (search) {
                        search.focus();
                    }
                }
            });
        }

        // Voice control support
        setupVoiceControl() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = document.documentElement.lang || 'en-US';

                // Add voice command indicators
                const voiceElements = document.querySelectorAll('[data-voice-command]');
                voiceElements.forEach(element => {
                    element.addEventListener('click', () => {
                        const command = element.getAttribute('data-voice-command');
                        this.announceToScreenReader(`Voice command: ${command}`);
                    });
                });
            }
        }
    }

    // Initialize accessibility manager when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            new AccessibilityManager();
        });
    } else {
        new AccessibilityManager();
    }

    // Export for manual initialization if needed
    window.AccessibilityManager = AccessibilityManager;

})();

// Additional utility functions
window.AccessibilityUtils = {
    // Focus management
    focusElement: function(selector) {
        const element = document.querySelector(selector);
        if (element) {
            element.focus();
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    },

    // Announce to screen readers
    announce: function(message, priority = 'polite') {
        const liveRegion = document.getElementById('live-region');
        if (liveRegion) {
            liveRegion.setAttribute('aria-live', priority);
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    },

    // Check if element is focusable
    isFocusable: function(element) {
        const focusableElements = 'a[href], button, input, textarea, select, details, [tabindex]:not([tabindex="-1"])';
        return element.matches(focusableElements) && !element.disabled && !element.hidden;
    },

    // Get all focusable elements in container
    getFocusableElements: function(container = document) {
        const focusableElements = 'a[href], button, input, textarea, select, details, [tabindex]:not([tabindex="-1"])';
        return Array.from(container.querySelectorAll(focusableElements))
            .filter(element => !element.disabled && !element.hidden);
    },

    // Set focus trap
    setFocusTrap: function(container) {
        const focusableElements = this.getFocusableElements(container);
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        container.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        e.preventDefault();
                        lastElement.focus();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        e.preventDefault();
                        firstElement.focus();
                    }
                }
            }
        });
    }
};

console.log('Accessibility enhancements loaded');