// Performance Optimizations for Muntazir Portfolio

// Lazy Loading for Images
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Preload Critical Resources
function preloadCriticalResources() {
    const criticalResources = [
        '/static/css/responsive.css',
        '/static/css/home-fixes.css'
    ];

    criticalResources.forEach(resource => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'style';
        link.href = resource;
        document.head.appendChild(link);
    });
}

// Optimize Font Loading
function optimizeFontLoading() {
    // Add font-display: swap to improve loading performance
    const style = document.createElement('style');
    style.textContent = `
        @font-face {
            font-family: 'system-ui';
            font-display: swap;
        }
    `;
    document.head.appendChild(style);
}

// Debounce Function for Performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimize Scroll Performance
function optimizeScrollPerformance() {
    let ticking = false;

    function updateScrollPosition() {
        // Handle scroll-based animations efficiently
        const scrollTop = window.pageYOffset;
        
        // Update any scroll-dependent elements here
        document.documentElement.style.setProperty('--scroll-y', scrollTop + 'px');
        
        ticking = false;
    }

    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateScrollPosition);
            ticking = true;
        }
    }

    window.addEventListener('scroll', requestTick, { passive: true });
}

// Reduce Layout Thrashing
function reduceLayoutThrashing() {
    // Batch DOM reads and writes
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    function batchDOMOperations() {
        // Read phase
        const measurements = [];
        elements.forEach(el => {
            measurements.push({
                element: el,
                rect: el.getBoundingClientRect()
            });
        });
        
        // Write phase
        measurements.forEach(({ element, rect }) => {
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                element.classList.add('in-view');
            }
        });
    }
    
    const debouncedBatch = debounce(batchDOMOperations, 16);
    window.addEventListener('scroll', debouncedBatch, { passive: true });
}

// Service Worker Registration for Caching
function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => {
                    console.log('SW registered: ', registration);
                })
                .catch(registrationError => {
                    console.log('SW registration failed: ', registrationError);
                });
        });
    }
}

// Critical CSS Inlining
function inlineCriticalCSS() {
    const criticalCSS = `
        /* Critical above-the-fold styles */
        body { margin: 0; font-family: system-ui, -apple-system, sans-serif; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 1rem; }
        .hero { min-height: 50vh; display: flex; align-items: center; }
        .nav { position: sticky; top: 0; z-index: 100; }
    `;
    
    const style = document.createElement('style');
    style.textContent = criticalCSS;
    document.head.appendChild(style);
}

// Initialize all optimizations
function initPerformanceOptimizations() {
    // Run immediately
    inlineCriticalCSS();
    optimizeFontLoading();
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initLazyLoading();
            optimizeScrollPerformance();
            reduceLayoutThrashing();
        });
    } else {
        initLazyLoading();
        optimizeScrollPerformance();
        reduceLayoutThrashing();
    }
    
    // Run when page is fully loaded
    window.addEventListener('load', () => {
        preloadCriticalResources();
        registerServiceWorker();
    });
}

// Auto-initialize
initPerformanceOptimizations();

// Export for manual initialization if needed
window.PerformanceOptimizations = {
    initLazyLoading,
    preloadCriticalResources,
    optimizeFontLoading,
    optimizeScrollPerformance,
    reduceLayoutThrashing,
    registerServiceWorker,
    debounce
};