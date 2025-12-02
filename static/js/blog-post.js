// Blog Post JavaScript Functions

// Font size control variables
let currentFontSize = 100;
const minFontSize = 80;
const maxFontSize = 150;
const fontSizeStep = 10;

// Initialize font size controls
function initializeFontControls() {
    // Load saved font size
    const savedFontSize = localStorage.getItem('articleFontSize');
    if (savedFontSize) {
        currentFontSize = parseInt(savedFontSize);
        updateFontSize();
    }
}

// Update font size
function updateFontSize() {
    const postContent = document.querySelector('.post-content');
    if (postContent) {
        postContent.style.fontSize = `${currentFontSize}%`;
    }
    
    // Update display
    const display = document.getElementById('font-size-display');
    if (display) {
        display.textContent = `${currentFontSize}%`;
    }
    
    // Update button states
    const decreaseBtn = document.getElementById('decrease-font');
    const increaseBtn = document.getElementById('increase-font');
    
    if (decreaseBtn) {
        decreaseBtn.disabled = currentFontSize <= minFontSize;
        decreaseBtn.style.opacity = currentFontSize <= minFontSize ? '0.5' : '1';
    }
    
    if (increaseBtn) {
        increaseBtn.disabled = currentFontSize >= maxFontSize;
        increaseBtn.style.opacity = currentFontSize >= maxFontSize ? '0.5' : '1';
    }
    
    // Save to localStorage
    localStorage.setItem('articleFontSize', currentFontSize);
}

// Increase font size
function increaseFontSize() {
    if (currentFontSize < maxFontSize) {
        currentFontSize += fontSizeStep;
        updateFontSize();
        showToast(`Font size increased to ${currentFontSize}%`);
    }
}

// Decrease font size
function decreaseFontSize() {
    if (currentFontSize > minFontSize) {
        currentFontSize -= fontSizeStep;
        updateFontSize();
        showToast(`Font size decreased to ${currentFontSize}%`);
    }
}

// Reset font size
function resetFontSize() {
    currentFontSize = 100;
    updateFontSize();
    showToast('Font size reset to default');
}

// Social sharing functions
function shareOn(platform) {
    const url = encodeURIComponent(window.location.href);
    const title = encodeURIComponent(document.title);
    const text = encodeURIComponent(document.querySelector('meta[name="description"]')?.content || '');
    
    let shareUrl = '';
    
    switch(platform) {
        case 'twitter':
            shareUrl = `https://twitter.com/intent/tweet?text=${title}&url=${url}`;
            break;
        case 'facebook':
            shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}&quote=${title}`;
            break;
        case 'linkedin':
            shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}&title=${title}&summary=${text}`;
            break;
        case 'whatsapp':
            shareUrl = `https://wa.me/?text=${title}%20${url}`;
            break;
        case 'telegram':
            shareUrl = `https://t.me/share/url?url=${url}&text=${title}`;
            break;
        case 'reddit':
            shareUrl = `https://reddit.com/submit?url=${url}&title=${title}`;
            break;
        case 'email':
            shareUrl = `mailto:?subject=${title}&body=${text}%0A%0A${url}`;
            break;
    }
    
    if (shareUrl) {
        if (platform === 'email') {
            window.location.href = shareUrl;
        } else {
            window.open(shareUrl, '_blank', 'width=600,height=400');
        }
        
        // Track share action
        trackShare(platform);
    }
}

// Native Web Share API
function nativeShare() {
    if (navigator.share) {
        navigator.share({
            title: document.title,
            text: document.querySelector('meta[name="description"]')?.content || '',
            url: window.location.href
        }).then(() => {
            showToast('Article shared successfully!');
            trackShare('native');
        }).catch((error) => {
            console.log('Error sharing:', error);
        });
    } else {
        // Fallback to copy link
        copyLink();
    }
}

// Copy link to clipboard
function copyLink() {
    navigator.clipboard.writeText(window.location.href).then(() => {
        showToast('Link copied to clipboard!');
        trackShare('copy');
    }).catch(() => {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = window.location.href;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showToast('Link copied to clipboard!');
            trackShare('copy');
        } catch (err) {
            showToast('Failed to copy link', 'error');
        }
        document.body.removeChild(textArea);
    });
}

// Track sharing analytics
function trackShare(platform) {
    const postId = document.querySelector('[data-post-id]')?.dataset.postId || 'unknown';
    const shares = JSON.parse(localStorage.getItem(`articleShares_${postId}`) || '{}');
    shares[platform] = (shares[platform] || 0) + 1;
    localStorage.setItem(`articleShares_${postId}`, JSON.stringify(shares));
}

// Show toast notification
function showToast(message, type = 'success') {
    // Remove existing toast
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast fixed top-4 right-4 z-50 px-4 py-2 rounded-lg text-white transition-all duration-300 transform translate-x-full`;
    toast.style.backgroundColor = type === 'error' ? '#ef4444' : '#10b981';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Hide toast after 3 seconds
    setTimeout(() => {
        toast.style.transform = 'translateX(full)';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeFontControls();
    initializeReactions();
    
    // Show native share button if supported
    if (navigator.share) {
        const nativeShareBtn = document.getElementById('native-share-btn');
        if (nativeShareBtn) {
            nativeShareBtn.style.display = 'block';
        }
    }
});

// Toggle bookmark function
function toggleBookmark() {
    const bookmarkBtn = document.querySelector('.bookmark-btn');
    const postId = document.querySelector('[data-post-id]')?.dataset.postId;
    
    if (!postId) {
        showToast('Unable to bookmark this article', 'error');
        return;
    }
    
    // Get current bookmarks from localStorage
    const bookmarks = JSON.parse(localStorage.getItem('bookmarkedPosts') || '[]');
    const isBookmarked = bookmarks.includes(postId);
    
    if (isBookmarked) {
        // Remove bookmark
        const index = bookmarks.indexOf(postId);
        bookmarks.splice(index, 1);
        localStorage.setItem('bookmarkedPosts', JSON.stringify(bookmarks));
        
        if (bookmarkBtn) {
            bookmarkBtn.innerHTML = '<i class="fas fa-bookmark-o"></i> Bookmark';
            bookmarkBtn.classList.remove('bookmarked');
        }
        showToast('Bookmark removed');
    } else {
        // Add bookmark
        bookmarks.push(postId);
        localStorage.setItem('bookmarkedPosts', JSON.stringify(bookmarks));
        
        if (bookmarkBtn) {
            bookmarkBtn.innerHTML = '<i class="fas fa-bookmark"></i> Bookmarked';
            bookmarkBtn.classList.add('bookmarked');
        }
        showToast('Article bookmarked!');
    }
}

// Print article function
function printArticle() {
    try {
        // Create a new window for printing
        const printWindow = window.open('', '_blank');
        
        // Check if window was created successfully
        if (!printWindow) {
            showToast('Unable to open print window. Please check popup blocker settings.', 'error');
            return;
        }
        
        // Get article content
        const title = document.querySelector('h1')?.textContent || document.title;
        const content = document.querySelector('.post-content')?.innerHTML || '';
        
        // Try multiple selectors to find author name
        let author = '';
        const authorElement = document.querySelector('.font-medium.text-gray-900.dark\\:text-white') || 
                             document.querySelector('[class*="author"]') ||
                             document.querySelector('p.font-medium');
        if (authorElement) {
            author = authorElement.textContent.trim();
        }
        
        // Try to find date
        let date = '';
        const dateElement = document.querySelector('time') || 
                           document.querySelector('[datetime]') ||
                           document.querySelector('.post-date');
        if (dateElement) {
            date = dateElement.textContent.trim();
        }
        
        // Create print-friendly HTML
        const printHTML = `<!DOCTYPE html>
<html>
<head>
    <title>${title}</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .meta {
            color: #666;
            font-style: italic;
            margin-bottom: 20px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        pre {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding-left: 20px;
            font-style: italic;
        }
        @media print {
            body { font-size: 12pt; }
            h1 { font-size: 18pt; }
            h2 { font-size: 16pt; }
            h3 { font-size: 14pt; }
        }
    </style>
</head>
<body>
    <h1>${title}</h1>
    <div class="meta">
        ${author ? 'By: ' + author : ''}
        ${date ? ' | ' + date : ''}
    </div>
    <div class="content">
        ${content}
    </div>
</body>
</html>`;
        
        // Write content to print window
        printWindow.document.write(printHTML);
        printWindow.document.close();
        
        // Wait for content to load then print
        printWindow.onload = function() {
            printWindow.print();
            printWindow.close();
        };
        
        showToast('Print dialog opened');
    } catch (error) {
        console.error('Print error:', error);
        showToast('Error opening print dialog', 'error');
    }
}

// Add reaction function
function addReaction(reactionType) {
    const postId = document.querySelector('[data-post-id]')?.dataset.postId;
    
    if (!postId) {
        showToast('Unable to add reaction', 'error');
        return;
    }
    
    // Get current reactions from localStorage
    const reactions = JSON.parse(localStorage.getItem(`postReactions_${postId}`) || '{}');
    
    // Initialize reaction count if not exists
    if (!reactions[reactionType]) {
        reactions[reactionType] = 0;
    }
    
    // Check if user already reacted with this type
    const userReactions = JSON.parse(localStorage.getItem(`userReactions_${postId}`) || '[]');
    const hasReacted = userReactions.includes(reactionType);
    
    if (hasReacted) {
        // Remove reaction
        reactions[reactionType] = Math.max(0, reactions[reactionType] - 1);
        const index = userReactions.indexOf(reactionType);
        userReactions.splice(index, 1);
        showToast(`${reactionType} reaction removed`);
    } else {
        // Add reaction
        reactions[reactionType] += 1;
        userReactions.push(reactionType);
        showToast(`${reactionType} reaction added!`);
    }
    
    // Save to localStorage
    localStorage.setItem(`postReactions_${postId}`, JSON.stringify(reactions));
    localStorage.setItem(`userReactions_${postId}`, JSON.stringify(userReactions));
    
    // Update UI
    updateReactionUI(reactionType, reactions[reactionType], hasReacted);
}

// Update reaction UI
function updateReactionUI(reactionType, count, wasReacted) {
    const reactionBtn = document.querySelector(`[data-reaction="${reactionType}"]`);
    if (reactionBtn) {
        const countElement = reactionBtn.querySelector('.reaction-count');
        if (countElement) {
            countElement.textContent = count;
        }
        
        // Toggle active state
        if (wasReacted) {
            reactionBtn.classList.remove('active');
        } else {
            reactionBtn.classList.add('active');
        }
    }
}

// Initialize reactions on page load
function initializeReactions() {
    const postId = document.querySelector('[data-post-id]')?.dataset.postId;
    if (!postId) return;
    
    const reactions = JSON.parse(localStorage.getItem(`postReactions_${postId}`) || '{}');
    const userReactions = JSON.parse(localStorage.getItem(`userReactions_${postId}`) || '[]');
    
    // Update all reaction buttons
    Object.keys(reactions).forEach(reactionType => {
        const count = reactions[reactionType];
        const hasReacted = userReactions.includes(reactionType);
        updateReactionUI(reactionType, count, !hasReacted); // Note: inverted because updateReactionUI toggles
    });
}

// Make functions globally available
window.increaseFontSize = increaseFontSize;
window.decreaseFontSize = decreaseFontSize;
window.resetFontSize = resetFontSize;
window.shareOn = shareOn;
window.nativeShare = nativeShare;
window.copyLink = copyLink;
window.showToast = showToast;
window.toggleBookmark = toggleBookmark;
window.printArticle = printArticle;
window.addReaction = addReaction;
window.initializeReactions = initializeReactions;