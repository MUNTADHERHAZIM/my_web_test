// UI/UX Enhancements for Muntazir Portfolio
// Modern User Experience and Interaction Improvements

(function() {
    'use strict';

    // UI Enhancement Manager
    class UIEnhancementManager {
        constructor() {
            this.init();
        }

        init() {
            this.setupSmoothScrolling();
            this.setupParallaxEffects();
            this.setupIntersectionObserver();
            this.setupImageLazyLoading();
            this.setupFormEnhancements();
            this.setupNavigationEnhancements();
            this.setupCardHoverEffects();
            this.setupTypingAnimation();
            this.setupProgressBars();
            this.setupTooltips();
            this.setupModals();
            this.setupTabs();
            this.setupAccordions();
            this.setupScrollToTop();
            this.setupThemeToggle();
            this.setupSearchEnhancements();
            this.setupNotifications();
            this.setupKeyboardShortcuts();
            this.setupPerformanceOptimizations();
        }

        // Smooth Scrolling Enhancement
        setupSmoothScrolling() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', (e) => {
                    e.preventDefault();
                    const target = document.querySelector(anchor.getAttribute('href'));
                    if (target) {
                        const headerOffset = 80;
                        const elementPosition = target.getBoundingClientRect().top;
                        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                        window.scrollTo({
                            top: offsetPosition,
                            behavior: 'smooth'
                        });

                        // Update URL without jumping
                        history.pushState(null, null, anchor.getAttribute('href'));
                    }
                });
            });
        }

        // Parallax Effects
        setupParallaxEffects() {
            const parallaxElements = document.querySelectorAll('.parallax');
            
            if (parallaxElements.length > 0) {
                window.addEventListener('scroll', this.throttle(() => {
                    const scrolled = window.pageYOffset;
                    const rate = scrolled * -0.5;
                    
                    parallaxElements.forEach(element => {
                        element.style.transform = `translateY(${rate}px)`;
                    });
                }, 16));
            }
        }

        // Intersection Observer for Animations
        setupIntersectionObserver() {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-fade-in');
                        
                        // Add staggered animation for children
                        const children = entry.target.querySelectorAll('.stagger-child');
                        children.forEach((child, index) => {
                            setTimeout(() => {
                                child.classList.add('animate-slide-in-left');
                            }, index * 100);
                        });
                        
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            document.querySelectorAll('.animate-on-scroll').forEach(el => {
                observer.observe(el);
            });
        }

        // Enhanced Image Lazy Loading
        setupImageLazyLoading() {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        const src = img.getAttribute('data-src');
                        
                        if (src) {
                            img.src = src;
                            img.classList.add('loaded');
                            img.removeAttribute('data-src');
                        }
                        
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }

        // Form Enhancements
        setupFormEnhancements() {
            // Floating Labels
            document.querySelectorAll('.form-floating').forEach(container => {
                const input = container.querySelector('input, textarea');
                const label = container.querySelector('label');
                
                if (input && label) {
                    input.addEventListener('focus', () => {
                        label.classList.add('floating');
                    });
                    
                    input.addEventListener('blur', () => {
                        if (!input.value) {
                            label.classList.remove('floating');
                        }
                    });
                    
                    // Check initial state
                    if (input.value) {
                        label.classList.add('floating');
                    }
                }
            });

            // Real-time Validation
            document.querySelectorAll('input[type="email"]').forEach(input => {
                input.addEventListener('input', this.debounce(() => {
                    this.validateEmail(input);
                }, 300));
            });

            // Password Strength Indicator
            document.querySelectorAll('input[type="password"]').forEach(input => {
                const strengthIndicator = this.createPasswordStrengthIndicator();
                input.parentNode.appendChild(strengthIndicator);
                
                input.addEventListener('input', () => {
                    this.updatePasswordStrength(input.value, strengthIndicator);
                });
            });

            // Auto-resize Textareas
            document.querySelectorAll('textarea.auto-resize').forEach(textarea => {
                textarea.addEventListener('input', () => {
                    textarea.style.height = 'auto';
                    textarea.style.height = textarea.scrollHeight + 'px';
                });
            });
        }

        // Navigation Enhancements
        setupNavigationEnhancements() {
            // Active Navigation Highlighting
            const navLinks = document.querySelectorAll('.nav-link');
            const sections = document.querySelectorAll('section[id]');
            
            window.addEventListener('scroll', this.throttle(() => {
                let current = '';
                
                sections.forEach(section => {
                    const sectionTop = section.getBoundingClientRect().top;
                    if (sectionTop <= 100) {
                        current = section.getAttribute('id');
                    }
                });
                
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${current}`) {
                        link.classList.add('active');
                    }
                });
            }, 100));

            // Mobile Menu Enhancement
            const mobileMenuButton = document.querySelector('.mobile-menu-toggle');
            const mobileMenu = document.querySelector('.mobile-menu');
            
            if (mobileMenuButton && mobileMenu) {
                mobileMenuButton.addEventListener('click', () => {
                    mobileMenu.classList.toggle('active');
                    mobileMenuButton.classList.toggle('active');
                    document.body.classList.toggle('menu-open');
                });

                // Close menu when clicking outside
                document.addEventListener('click', (e) => {
                    if (!mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target)) {
                        mobileMenu.classList.remove('active');
                        mobileMenuButton.classList.remove('active');
                        document.body.classList.remove('menu-open');
                    }
                });
            }
        }

        // Card Hover Effects
        setupCardHoverEffects() {
            document.querySelectorAll('.card-hover').forEach(card => {
                card.addEventListener('mouseenter', () => {
                    card.style.transform = 'translateY(-8px) scale(1.02)';
                    card.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.1)';
                });
                
                card.addEventListener('mouseleave', () => {
                    card.style.transform = 'translateY(0) scale(1)';
                    card.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
                });
            });
        }

        // Typing Animation
        setupTypingAnimation() {
            const typingElements = document.querySelectorAll('.typing-text');
            
            typingElements.forEach(element => {
                const text = element.textContent;
                const speed = parseInt(element.getAttribute('data-speed')) || 100;
                
                element.textContent = '';
                element.style.borderRight = '2px solid currentColor';
                
                let i = 0;
                const typeWriter = () => {
                    if (i < text.length) {
                        element.textContent += text.charAt(i);
                        i++;
                        setTimeout(typeWriter, speed);
                    } else {
                        // Blinking cursor effect
                        setInterval(() => {
                            element.style.borderRight = element.style.borderRight === 'none' 
                                ? '2px solid currentColor' 
                                : 'none';
                        }, 500);
                    }
                };
                
                // Start typing when element is visible
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            setTimeout(typeWriter, 500);
                            observer.unobserve(entry.target);
                        }
                    });
                });
                
                observer.observe(element);
            });
        }

        // Progress Bars
        setupProgressBars() {
            const progressBars = document.querySelectorAll('.progress-bar');
            
            const progressObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const progressBar = entry.target;
                        const percentage = progressBar.getAttribute('data-percentage');
                        
                        progressBar.style.width = '0%';
                        setTimeout(() => {
                            progressBar.style.width = percentage + '%';
                        }, 200);
                        
                        progressObserver.unobserve(progressBar);
                    }
                });
            });
            
            progressBars.forEach(bar => {
                progressObserver.observe(bar);
            });
        }

        // Enhanced Tooltips
        setupTooltips() {
            document.querySelectorAll('[data-tooltip]').forEach(element => {
                element.addEventListener('mouseenter', (e) => {
                    this.showTooltip(e.target, e.target.getAttribute('data-tooltip'));
                });
                
                element.addEventListener('mouseleave', () => {
                    this.hideTooltip();
                });
            });
        }

        showTooltip(element, text) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip-popup';
            tooltip.textContent = text;
            
            document.body.appendChild(tooltip);
            
            const rect = element.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            
            setTimeout(() => tooltip.classList.add('visible'), 10);
        }

        hideTooltip() {
            const tooltip = document.querySelector('.tooltip-popup');
            if (tooltip) {
                tooltip.remove();
            }
        }

        // Modal Enhancements
        setupModals() {
            document.querySelectorAll('[data-modal]').forEach(trigger => {
                trigger.addEventListener('click', (e) => {
                    e.preventDefault();
                    const modalId = trigger.getAttribute('data-modal');
                    this.openModal(modalId);
                });
            });
            
            document.querySelectorAll('.modal-close').forEach(closeBtn => {
                closeBtn.addEventListener('click', () => {
                    this.closeModal();
                });
            });
            
            // Close modal on backdrop click
            document.addEventListener('click', (e) => {
                if (e.target.classList.contains('modal-backdrop')) {
                    this.closeModal();
                }
            });
            
            // Close modal on Escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.closeModal();
                }
            });
        }

        openModal(modalId) {
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('active');
                document.body.classList.add('modal-open');
                
                // Focus first focusable element
                const focusable = modal.querySelector('button, input, textarea, select, a[href]');
                if (focusable) {
                    focusable.focus();
                }
            }
        }

        closeModal() {
            const activeModal = document.querySelector('.modal.active');
            if (activeModal) {
                activeModal.classList.remove('active');
                document.body.classList.remove('modal-open');
            }
        }

        // Tab Enhancement
        setupTabs() {
            document.querySelectorAll('.tab-nav').forEach(tabNav => {
                const tabs = tabNav.querySelectorAll('.tab-button');
                const panels = document.querySelectorAll('.tab-panel');
                
                tabs.forEach(tab => {
                    tab.addEventListener('click', () => {
                        const target = tab.getAttribute('data-tab');
                        
                        // Remove active class from all tabs and panels
                        tabs.forEach(t => t.classList.remove('active'));
                        panels.forEach(p => p.classList.remove('active'));
                        
                        // Add active class to clicked tab and corresponding panel
                        tab.classList.add('active');
                        document.getElementById(target).classList.add('active');
                    });
                });
            });
        }

        // Accordion Enhancement
        setupAccordions() {
            document.querySelectorAll('.accordion-item').forEach(item => {
                const header = item.querySelector('.accordion-header');
                const content = item.querySelector('.accordion-content');
                
                header.addEventListener('click', () => {
                    const isActive = item.classList.contains('active');
                    
                    // Close all accordion items
                    document.querySelectorAll('.accordion-item').forEach(i => {
                        i.classList.remove('active');
                    });
                    
                    // Open clicked item if it wasn't active
                    if (!isActive) {
                        item.classList.add('active');
                    }
                });
            });
        }

        // Scroll to Top Button
        setupScrollToTop() {
            const scrollToTopBtn = document.createElement('button');
            scrollToTopBtn.className = 'scroll-to-top';
            scrollToTopBtn.innerHTML = '↑';
            scrollToTopBtn.setAttribute('aria-label', 'Scroll to top');
            
            document.body.appendChild(scrollToTopBtn);
            
            window.addEventListener('scroll', this.throttle(() => {
                if (window.pageYOffset > 300) {
                    scrollToTopBtn.classList.add('visible');
                } else {
                    scrollToTopBtn.classList.remove('visible');
                }
            }, 100));
            
            scrollToTopBtn.addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }

        // Theme Toggle Enhancement
        setupThemeToggle() {
            const themeToggle = document.querySelector('.theme-toggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', () => {
                    document.body.classList.toggle('dark-theme');
                    const isDark = document.body.classList.contains('dark-theme');
                    localStorage.setItem('theme', isDark ? 'dark' : 'light');
                });
                
                // Load saved theme
                const savedTheme = localStorage.getItem('theme');
                if (savedTheme === 'dark') {
                    document.body.classList.add('dark-theme');
                }
            }
        }

        // Search Enhancements
        setupSearchEnhancements() {
            const searchInputs = document.querySelectorAll('.search-input');
            
            searchInputs.forEach(input => {
                input.addEventListener('input', this.debounce((e) => {
                    this.performSearch(e.target.value);
                }, 300));
            });
        }

        performSearch(query) {
            // Implement search functionality
            console.log('Searching for:', query);
        }

        // Notification System
        setupNotifications() {
            window.showNotification = (message, type = 'info', duration = 5000) => {
                const notification = document.createElement('div');
                notification.className = `notification notification-${type}`;
                notification.textContent = message;
                
                const container = document.querySelector('.notification-container') || this.createNotificationContainer();
                container.appendChild(notification);
                
                setTimeout(() => notification.classList.add('visible'), 10);
                
                setTimeout(() => {
                    notification.classList.remove('visible');
                    setTimeout(() => notification.remove(), 300);
                }, duration);
            };
        }

        createNotificationContainer() {
            const container = document.createElement('div');
            container.className = 'notification-container';
            document.body.appendChild(container);
            return container;
        }

        // Keyboard Shortcuts
        setupKeyboardShortcuts() {
            document.addEventListener('keydown', (e) => {
                // Ctrl/Cmd + K for search
                if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                    e.preventDefault();
                    const searchInput = document.querySelector('.search-input');
                    if (searchInput) {
                        searchInput.focus();
                    }
                }
                
                // Escape to close modals/menus
                if (e.key === 'Escape') {
                    this.closeModal();
                    const mobileMenu = document.querySelector('.mobile-menu.active');
                    if (mobileMenu) {
                        mobileMenu.classList.remove('active');
                    }
                }
            });
        }

        // Performance Optimizations
        setupPerformanceOptimizations() {
            // Preload critical resources
            this.preloadCriticalResources();
            
            // Optimize images
            this.optimizeImages();
            
            // Setup service worker
            this.setupServiceWorker();
        }

        preloadCriticalResources() {
            const criticalResources = [
                '/static/css/ui-enhancements.css',
                '/static/js/accessibility.js'
            ];
            
            criticalResources.forEach(resource => {
                const link = document.createElement('link');
                link.rel = 'preload';
                link.href = resource;
                link.as = resource.endsWith('.css') ? 'style' : 'script';
                document.head.appendChild(link);
            });
        }

        optimizeImages() {
            document.querySelectorAll('img').forEach(img => {
                if (!img.hasAttribute('loading')) {
                    img.setAttribute('loading', 'lazy');
                }
                
                if (!img.hasAttribute('decoding')) {
                    img.setAttribute('decoding', 'async');
                }
            });
        }

        setupServiceWorker() {
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('/static/js/sw.js')
                    .then(registration => {
                        console.log('Service Worker registered:', registration);
                    })
                    .catch(error => {
                        console.log('Service Worker registration failed:', error);
                    });
            }
        }

        // Utility Functions
        throttle(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        }

        debounce(func, delay) {
            let timeoutId;
            return function() {
                const args = arguments;
                const context = this;
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => func.apply(context, args), delay);
            };
        }

        validateEmail(input) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const isValid = emailRegex.test(input.value);
            
            input.classList.toggle('invalid', !isValid && input.value.length > 0);
            input.classList.toggle('valid', isValid);
        }

        createPasswordStrengthIndicator() {
            const indicator = document.createElement('div');
            indicator.className = 'password-strength';
            indicator.innerHTML = `
                <div class="strength-bar">
                    <div class="strength-fill"></div>
                </div>
                <div class="strength-text">Password strength</div>
            `;
            return indicator;
        }

        updatePasswordStrength(password, indicator) {
            let strength = 0;
            let text = 'Weak';
            
            if (password.length >= 8) strength++;
            if (/[a-z]/.test(password)) strength++;
            if (/[A-Z]/.test(password)) strength++;
            if (/[0-9]/.test(password)) strength++;
            if (/[^A-Za-z0-9]/.test(password)) strength++;
            
            const fill = indicator.querySelector('.strength-fill');
            const textEl = indicator.querySelector('.strength-text');
            
            switch (strength) {
                case 0:
                case 1:
                    text = 'Very Weak';
                    fill.style.width = '20%';
                    fill.style.backgroundColor = '#ef4444';
                    break;
                case 2:
                    text = 'Weak';
                    fill.style.width = '40%';
                    fill.style.backgroundColor = '#f59e0b';
                    break;
                case 3:
                    text = 'Fair';
                    fill.style.width = '60%';
                    fill.style.backgroundColor = '#eab308';
                    break;
                case 4:
                    text = 'Good';
                    fill.style.width = '80%';
                    fill.style.backgroundColor = '#22c55e';
                    break;
                case 5:
                    text = 'Strong';
                    fill.style.width = '100%';
                    fill.style.backgroundColor = '#10b981';
                    break;
            }
            
            textEl.textContent = text;
        }
    }

    // Initialize UI Enhancements
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            new UIEnhancementManager();
        });
    } else {
        new UIEnhancementManager();
    }

    // Export for manual initialization if needed
    window.UIEnhancementManager = UIEnhancementManager;

})();

// Additional CSS for UI enhancements
const additionalStyles = `
.scroll-to-top {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    background: var(--primary-600, #3b82f6);
    color: white;
    border: none;
    border-radius: 50%;
    font-size: 20px;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 1000;
}

.scroll-to-top.visible {
    opacity: 1;
    visibility: visible;
}

.scroll-to-top:hover {
    background: var(--primary-700, #2563eb);
    transform: translateY(-2px);
}

.notification-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1080;
    pointer-events: none;
}

.notification {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 10px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    transform: translateX(100%);
    opacity: 0;
    transition: all 0.3s ease;
    pointer-events: auto;
    max-width: 300px;
}

.notification.visible {
    transform: translateX(0);
    opacity: 1;
}

.notification-success {
    border-left: 4px solid #10b981;
}

.notification-error {
    border-left: 4px solid #ef4444;
}

.notification-warning {
    border-left: 4px solid #f59e0b;
}

.notification-info {
    border-left: 4px solid #06b6d4;
}

.tooltip-popup {
    position: absolute;
    background: #1f2937;
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 14px;
    z-index: 1070;
    opacity: 0;
    transition: opacity 0.2s ease;
    pointer-events: none;
}

.tooltip-popup.visible {
    opacity: 1;
}

.password-strength {
    margin-top: 8px;
}

.strength-bar {
    width: 100%;
    height: 4px;
    background: #e5e7eb;
    border-radius: 2px;
    overflow: hidden;
}

.strength-fill {
    height: 100%;
    width: 0;
    transition: all 0.3s ease;
}

.strength-text {
    font-size: 12px;
    margin-top: 4px;
    color: #6b7280;
}
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

console.log('UI/UX enhancements loaded');