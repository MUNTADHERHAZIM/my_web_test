// Modern Design JavaScript for Muntazir Portfolio

class ModernDesignManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupScrollEffects();
        this.setupNavbarEffects();
        this.setupScrollReveal();
        this.setupParallaxEffects();
        this.setupSmoothScrolling();
        this.setupModernAnimations();
        this.setupIntersectionObserver();
        this.setupModernInteractions();
        this.setupPerformanceOptimizations();
    }

    // Modern Navbar Effects
    setupNavbarEffects() {
        const navbar = document.querySelector('.modern-navbar');
        if (!navbar) return;

        let lastScrollY = window.scrollY;
        let ticking = false;

        const updateNavbar = () => {
            const scrollY = window.scrollY;
            
            // Add scrolled class for backdrop blur effect
            if (scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            // Hide/show navbar on scroll
            if (scrollY > lastScrollY && scrollY > 100) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }

            lastScrollY = scrollY;
            ticking = false;
        };

        const requestTick = () => {
            if (!ticking) {
                requestAnimationFrame(updateNavbar);
                ticking = true;
            }
        };

        window.addEventListener('scroll', requestTick, { passive: true });
    }

    // Scroll Reveal Animations
    setupScrollReveal() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    // Add staggered animation for child elements
                    const children = entry.target.querySelectorAll('.modern-card, .modern-feature');
                    children.forEach((child, index) => {
                        setTimeout(() => {
                            child.style.animation = `fadeInUp 0.6s ease forwards`;
                            child.style.animationDelay = `${index * 0.1}s`;
                        }, index * 100);
                    });
                }
            });
        }, observerOptions);

        // Observe all scroll-reveal elements
        document.querySelectorAll('.scroll-reveal').forEach(el => {
            observer.observe(el);
        });
    }

    // Modern Parallax Effects
    setupParallaxEffects() {
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        
        if (parallaxElements.length === 0) return;

        let ticking = false;

        const updateParallax = () => {
            const scrollY = window.pageYOffset;

            parallaxElements.forEach(element => {
                const speed = element.dataset.parallax || 0.5;
                const yPos = -(scrollY * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });

            ticking = false;
        };

        const requestTick = () => {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        };

        window.addEventListener('scroll', requestTick, { passive: true });
    }

    // Enhanced Smooth Scrolling
    setupSmoothScrolling() {
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                
                if (target) {
                    const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    // Modern Animations and Interactions
    setupModernAnimations() {
        // Floating animation for hero elements
        const floatingElements = document.querySelectorAll('.floating');
        floatingElements.forEach((element, index) => {
            element.style.animationDelay = `${index * 0.5}s`;
        });

        // Modern card hover effects
        const cards = document.querySelectorAll('.modern-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-8px) scale(1.02)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Modern button effects
        const buttons = document.querySelectorAll('.modern-btn');
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                // Ripple effect
                const ripple = document.createElement('span');
                const rect = button.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    width: ${size}px;
                    height: ${size}px;
                    left: ${x}px;
                    top: ${y}px;
                    background: rgba(255, 255, 255, 0.3);
                    border-radius: 50%;
                    transform: scale(0);
                    animation: ripple 0.6s linear;
                    pointer-events: none;
                `;
                
                button.style.position = 'relative';
                button.style.overflow = 'hidden';
                button.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }

    // Advanced Intersection Observer
    setupIntersectionObserver() {
        const observerOptions = {
            threshold: [0, 0.25, 0.5, 0.75, 1],
            rootMargin: '-10% 0px -10% 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const element = entry.target;
                const ratio = entry.intersectionRatio;

                // Progressive reveal based on intersection ratio
                if (ratio > 0.1) {
                    element.style.opacity = Math.min(ratio * 1.5, 1);
                    element.style.transform = `translateY(${(1 - ratio) * 20}px)`;
                }

                // Add special effects for different elements
                if (entry.isIntersecting) {
                    if (element.classList.contains('modern-counter')) {
                        this.animateCounter(element);
                    }
                    
                    if (element.classList.contains('modern-progress')) {
                        this.animateProgress(element);
                    }
                }
            });
        }, observerOptions);

        // Observe animated elements
        document.querySelectorAll('.modern-animate').forEach(el => {
            observer.observe(el);
        });
    }

    // Modern Interactive Features
    setupModernInteractions() {
        // Modern tooltip system
        this.setupModernTooltips();
        
        // Modern modal system
        this.setupModernModals();
        
        // Modern tabs system
        this.setupModernTabs();
        
        // Modern accordion system
        this.setupModernAccordion();
        
        // Modern image gallery
        this.setupModernGallery();
    }

    // Modern Tooltips
    setupModernTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        
        tooltipElements.forEach(element => {
            let tooltip = null;
            
            element.addEventListener('mouseenter', () => {
                const text = element.dataset.tooltip;
                const position = element.dataset.tooltipPosition || 'top';
                
                tooltip = document.createElement('div');
                tooltip.className = 'modern-tooltip';
                tooltip.textContent = text;
                tooltip.style.cssText = `
                    position: absolute;
                    background: rgba(0, 0, 0, 0.9);
                    color: white;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-size: 14px;
                    white-space: nowrap;
                    z-index: 1000;
                    opacity: 0;
                    transform: translateY(10px);
                    transition: all 0.3s ease;
                    pointer-events: none;
                `;
                
                document.body.appendChild(tooltip);
                
                const rect = element.getBoundingClientRect();
                const tooltipRect = tooltip.getBoundingClientRect();
                
                let left = rect.left + (rect.width - tooltipRect.width) / 2;
                let top = rect.top - tooltipRect.height - 10;
                
                if (position === 'bottom') {
                    top = rect.bottom + 10;
                }
                
                tooltip.style.left = `${left}px`;
                tooltip.style.top = `${top}px`;
                
                requestAnimationFrame(() => {
                    tooltip.style.opacity = '1';
                    tooltip.style.transform = 'translateY(0)';
                });
            });
            
            element.addEventListener('mouseleave', () => {
                if (tooltip) {
                    tooltip.style.opacity = '0';
                    tooltip.style.transform = 'translateY(10px)';
                    setTimeout(() => {
                        if (tooltip && tooltip.parentNode) {
                            tooltip.parentNode.removeChild(tooltip);
                        }
                    }, 300);
                }
            });
        });
    }

    // Modern Modal System
    setupModernModals() {
        const modalTriggers = document.querySelectorAll('[data-modal]');
        
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const modalId = trigger.dataset.modal;
                const modal = document.getElementById(modalId);
                
                if (modal) {
                    this.openModal(modal);
                }
            });
        });
        
        // Close modal on backdrop click
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modern-modal-backdrop')) {
                this.closeModal(e.target.closest('.modern-modal'));
            }
        });
        
        // Close modal on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const openModal = document.querySelector('.modern-modal.active');
                if (openModal) {
                    this.closeModal(openModal);
                }
            }
        });
    }

    openModal(modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Focus management
        const focusableElements = modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length > 0) {
            focusableElements[0].focus();
        }
    }

    closeModal(modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Modern Tabs System
    setupModernTabs() {
        const tabContainers = document.querySelectorAll('.modern-tabs');
        
        tabContainers.forEach(container => {
            const tabs = container.querySelectorAll('.modern-tab');
            const panels = container.querySelectorAll('.modern-tab-panel');
            
            tabs.forEach((tab, index) => {
                tab.addEventListener('click', () => {
                    // Remove active class from all tabs and panels
                    tabs.forEach(t => t.classList.remove('active'));
                    panels.forEach(p => p.classList.remove('active'));
                    
                    // Add active class to clicked tab and corresponding panel
                    tab.classList.add('active');
                    if (panels[index]) {
                        panels[index].classList.add('active');
                    }
                });
            });
        });
    }

    // Modern Accordion System
    setupModernAccordion() {
        const accordionItems = document.querySelectorAll('.modern-accordion-item');
        
        accordionItems.forEach(item => {
            const header = item.querySelector('.modern-accordion-header');
            const content = item.querySelector('.modern-accordion-content');
            
            if (header && content) {
                header.addEventListener('click', () => {
                    const isActive = item.classList.contains('active');
                    
                    // Close all accordion items in the same group
                    const group = item.closest('.modern-accordion');
                    if (group) {
                        group.querySelectorAll('.modern-accordion-item').forEach(i => {
                            i.classList.remove('active');
                        });
                    }
                    
                    // Toggle current item
                    if (!isActive) {
                        item.classList.add('active');
                    }
                });
            }
        });
    }

    // Modern Image Gallery
    setupModernGallery() {
        const galleryImages = document.querySelectorAll('.modern-gallery img');
        
        galleryImages.forEach((img, index) => {
            img.addEventListener('click', () => {
                this.openLightbox(img, index, galleryImages);
            });
        });
    }

    openLightbox(img, index, images) {
        const lightbox = document.createElement('div');
        lightbox.className = 'modern-lightbox';
        lightbox.innerHTML = `
            <div class="modern-lightbox-backdrop"></div>
            <div class="modern-lightbox-content">
                <button class="modern-lightbox-close">&times;</button>
                <button class="modern-lightbox-prev">&#8249;</button>
                <img src="${img.src}" alt="${img.alt}">
                <button class="modern-lightbox-next">&#8250;</button>
                <div class="modern-lightbox-counter">${index + 1} / ${images.length}</div>
            </div>
        `;
        
        document.body.appendChild(lightbox);
        document.body.style.overflow = 'hidden';
        
        // Event listeners for lightbox
        const close = lightbox.querySelector('.modern-lightbox-close');
        const backdrop = lightbox.querySelector('.modern-lightbox-backdrop');
        const prev = lightbox.querySelector('.modern-lightbox-prev');
        const next = lightbox.querySelector('.modern-lightbox-next');
        const imgElement = lightbox.querySelector('img');
        const counter = lightbox.querySelector('.modern-lightbox-counter');
        
        let currentIndex = index;
        
        const updateImage = () => {
            imgElement.src = images[currentIndex].src;
            imgElement.alt = images[currentIndex].alt;
            counter.textContent = `${currentIndex + 1} / ${images.length}`;
        };
        
        prev.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + images.length) % images.length;
            updateImage();
        });
        
        next.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % images.length;
            updateImage();
        });
        
        const closeLightbox = () => {
            lightbox.remove();
            document.body.style.overflow = '';
        };
        
        close.addEventListener('click', closeLightbox);
        backdrop.addEventListener('click', closeLightbox);
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowLeft') prev.click();
            if (e.key === 'ArrowRight') next.click();
        });
    }

    // Counter Animation
    animateCounter(element) {
        const target = parseInt(element.dataset.count) || 0;
        const duration = parseInt(element.dataset.duration) || 2000;
        const start = 0;
        const startTime = performance.now();
        
        const updateCounter = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = Math.floor(start + (target - start) * this.easeOutQuart(progress));
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        };
        
        requestAnimationFrame(updateCounter);
    }

    // Progress Bar Animation
    animateProgress(element) {
        const target = parseInt(element.dataset.progress) || 0;
        const bar = element.querySelector('.modern-progress-bar');
        
        if (bar) {
            bar.style.width = `${target}%`;
        }
    }

    // Easing function
    easeOutQuart(t) {
        return 1 - (--t) * t * t * t;
    }

    // Performance Optimizations
    setupPerformanceOptimizations() {
        // Lazy load images
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('modern-skeleton');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => {
            img.classList.add('modern-skeleton');
            imageObserver.observe(img);
        });
        
        // Preload critical resources
        this.preloadCriticalResources();
        
        // Setup service worker if available
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => {
                    console.log('SW registered: ', registration);
                })
                .catch(registrationError => {
                    console.log('SW registration failed: ', registrationError);
                });
        }
    }

    preloadCriticalResources() {
        const criticalResources = [
            '/static/css/modern-design.css',
            '/static/js/modern-design.js'
        ];
        
        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = resource;
            link.as = resource.endsWith('.css') ? 'style' : 'script';
            document.head.appendChild(link);
        });
    }
}

// CSS Animations for JavaScript
const modernAnimationStyles = `
<style>
@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

.modern-lightbox {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
}

.modern-lightbox-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(10px);
}

.modern-lightbox-content {
    position: relative;
    max-width: 90vw;
    max-height: 90vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.modern-lightbox img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modern-lightbox-close,
.modern-lightbox-prev,
.modern-lightbox-next {
    position: absolute;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    color: white;
    font-size: 24px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.modern-lightbox-close {
    top: 20px;
    right: 20px;
}

.modern-lightbox-prev {
    left: 20px;
}

.modern-lightbox-next {
    right: 20px;
}

.modern-lightbox-counter {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
}

.modern-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
}

.modern-modal.active {
    opacity: 1;
    visibility: visible;
}

.modern-modal-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(5px);
}

.modern-modal-content {
    position: relative;
    background: white;
    border-radius: 12px;
    padding: 2rem;
    max-width: 90vw;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    transform: scale(0.9);
    transition: transform 0.3s ease;
}

.modern-modal.active .modern-modal-content {
    transform: scale(1);
}
</style>
`;

// Inject styles
document.head.insertAdjacentHTML('beforeend', modernAnimationStyles);

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ModernDesignManager();
    });
} else {
    new ModernDesignManager();
}

// Export for use in other scripts
window.ModernDesignManager = ModernDesignManager;