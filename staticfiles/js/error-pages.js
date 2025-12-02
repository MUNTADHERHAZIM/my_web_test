// Enhanced Error Pages JavaScript

// Particle System
class ParticleSystem {
    constructor(container) {
        this.container = container;
        this.particles = [];
        this.particleCount = 50;
        this.init();
    }

    init() {
        this.createParticles();
        this.animate();
    }

    createParticles() {
        for (let i = 0; i < this.particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 8 + 's';
            particle.style.animationDuration = (Math.random() * 4 + 8) + 's';
            this.container.appendChild(particle);
            this.particles.push(particle);
        }
    }

    animate() {
        // Additional particle animations can be added here
        setInterval(() => {
            this.particles.forEach(particle => {
                if (Math.random() < 0.1) {
                    particle.style.opacity = Math.random() * 0.5 + 0.3;
                }
            });
        }, 2000);
    }
}

// Interactive Elements
class InteractiveElements {
    constructor() {
        this.init();
    }

    init() {
        this.addHoverEffects();
        this.addClickEffects();
        this.addKeyboardNavigation();
        this.addMouseTracker();
    }

    addHoverEffects() {
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.addEventListener('mouseenter', (e) => {
                this.createRipple(e.target, e);
            });
        });
    }

    addClickEffects() {
        const interactiveElements = document.querySelectorAll('.interactive-element, .btn');
        interactiveElements.forEach(element => {
            element.addEventListener('click', (e) => {
                this.createClickEffect(e.target, e);
            });
        });
    }

    addKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                const focusedElement = document.activeElement;
                if (focusedElement.classList.contains('btn')) {
                    this.createClickEffect(focusedElement, e);
                }
            }
        });
    }

    addMouseTracker() {
        const errorCode = document.querySelector('.error-code');
        if (errorCode) {
            document.addEventListener('mousemove', (e) => {
                const rect = errorCode.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                
                const rotateX = (y / rect.height) * 10;
                const rotateY = (x / rect.width) * -10;
                
                errorCode.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });

            document.addEventListener('mouseleave', () => {
                errorCode.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
            });
        }
    }

    createRipple(element, event) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    createClickEffect(element, event) {
        element.style.transform = 'scale(0.95)';
        setTimeout(() => {
            element.style.transform = '';
        }, 150);
    }
}

// Error Page Animations
class ErrorPageAnimations {
    constructor() {
        this.init();
    }

    init() {
        this.animateOnLoad();
        this.addScrollAnimations();
        this.addRandomAnimations();
    }

    animateOnLoad() {
        const elements = document.querySelectorAll('.error-container > *');
        elements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                element.style.transition = 'all 0.6s ease';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }

    addScrollAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        });

        const animatedElements = document.querySelectorAll('.btn, .method-list');
        animatedElements.forEach(el => observer.observe(el));
    }

    addRandomAnimations() {
        const shapes = document.querySelectorAll('.shape, .element, .geometric-shape');
        shapes.forEach(shape => {
            setInterval(() => {
                if (Math.random() < 0.3) {
                    shape.style.transform += ' scale(1.1)';
                    setTimeout(() => {
                        shape.style.transform = shape.style.transform.replace(' scale(1.1)', '');
                    }, 300);
                }
            }, Math.random() * 5000 + 2000);
        });
    }
}

// Theme Manager
class ThemeManager {
    constructor() {
        this.init();
    }

    init() {
        this.detectTheme();
        this.addThemeToggle();
    }

    detectTheme() {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (prefersDark) {
            document.body.classList.add('dark-theme');
        }
    }

    addThemeToggle() {
        // Add theme toggle functionality if needed
        const themeToggle = document.createElement('button');
        themeToggle.innerHTML = '🌙';
        themeToggle.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 20px;
            cursor: pointer;
            z-index: 1000;
            transition: all 0.3s ease;
        `;
        
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-theme');
            themeToggle.innerHTML = document.body.classList.contains('dark-theme') ? '☀️' : '🌙';
        });
        
        document.body.appendChild(themeToggle);
    }
}

// Accessibility Enhancements
class AccessibilityEnhancements {
    constructor() {
        this.init();
    }

    init() {
        this.addFocusManagement();
        this.addScreenReaderSupport();
        this.addKeyboardShortcuts();
    }

    addFocusManagement() {
        const focusableElements = document.querySelectorAll('a, button, [tabindex]');
        focusableElements.forEach((element, index) => {
            element.addEventListener('focus', () => {
                element.style.outline = '3px solid #007bff';
                element.style.outlineOffset = '2px';
            });
            
            element.addEventListener('blur', () => {
                element.style.outline = '';
                element.style.outlineOffset = '';
            });
        });
    }

    addScreenReaderSupport() {
        const errorCode = document.querySelector('.error-code');
        if (errorCode) {
            errorCode.setAttribute('aria-label', `خطأ ${errorCode.textContent}`);
        }
        
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            if (!btn.getAttribute('aria-label')) {
                btn.setAttribute('aria-label', btn.textContent);
            }
        });
    }

    addKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Alt + H: Go to home
            if (e.altKey && e.key === 'h') {
                const homeLink = document.querySelector('a[href="/"]');
                if (homeLink) homeLink.click();
            }
            
            // Alt + B: Go back
            if (e.altKey && e.key === 'b') {
                history.back();
            }
            
            // Escape: Focus first button
            if (e.key === 'Escape') {
                const firstButton = document.querySelector('.btn');
                if (firstButton) firstButton.focus();
            }
        });
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Check if user prefers reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (!prefersReducedMotion) {
        // Create particle system
        const particleContainer = document.createElement('div');
        particleContainer.className = 'particles';
        document.body.appendChild(particleContainer);
        new ParticleSystem(particleContainer);
        
        // Initialize animations
        new ErrorPageAnimations();
    }
    
    // Always initialize these (they respect reduced motion preferences)
    new InteractiveElements();
    new ThemeManager();
    new AccessibilityEnhancements();
    
    // Add CSS for ripple effect
    const style = document.createElement('style');
    style.textContent = `
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .animate-in {
            animation: slideInUp 0.6s ease forwards;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .dark-theme {
            filter: brightness(0.8) contrast(1.2);
        }
    `;
    document.head.appendChild(style);
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        const loadTime = performance.now();
        if (loadTime > 3000) {
            console.warn('Error page loaded slowly:', loadTime + 'ms');
        }
    });
}