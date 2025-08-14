// DOM elements
const urlForm = document.getElementById('urlForm');
const urlInput = document.getElementById('urlInput');
const shortenBtn = document.getElementById('shortenBtn');
const resultContainer = document.getElementById('resultContainer');
const errorContainer = document.getElementById('errorContainer');
const loadingContainer = document.getElementById('loadingContainer');
const originalUrl = document.getElementById('originalUrl');
const shortenedUrl = document.getElementById('shortenedUrl');
const copyBtn = document.getElementById('copyBtn');
const newUrlBtn = document.getElementById('newUrlBtn');
const testLink = document.getElementById('testLink');
const errorMessage = document.getElementById('errorMessage');
const dismissError = document.getElementById('dismissError');

// Event listeners
urlForm.addEventListener('submit', handleUrlSubmit);
copyBtn.addEventListener('click', copyToClipboard);
newUrlBtn.addEventListener('click', resetForm);
dismissError.addEventListener('click', hideError);

// Handle URL form submission
async function handleUrlSubmit(e) {
    e.preventDefault();
    
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Please enter a URL');
        return;
    }
    
    // Show loading state
    showLoading();
    hideError();
    hideResult();
    
    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to shorten URL');
        }
        
        // Display result
        displayResult(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// Display the shortened URL result
function displayResult(data) {
    originalUrl.textContent = data.original_url;
    shortenedUrl.value = data.short_url;
    testLink.href = data.short_url;
    
    showResult();
    
    // Scroll to result
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Copy shortened URL to clipboard
async function copyToClipboard() {
    try {
        await navigator.clipboard.writeText(shortenedUrl.value);
        
        // Update button text temporarily
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        copyBtn.classList.add('copied');
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.classList.remove('copied');
        }, 2000);
        
    } catch (error) {
        // Fallback for older browsers
        shortenedUrl.select();
        document.execCommand('copy');
        
        // Show feedback
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        copyBtn.classList.add('copied');
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.classList.remove('copied');
        }, 2000);
    }
}

// Reset form to initial state
function resetForm() {
    urlForm.reset();
    hideResult();
    hideError();
    urlInput.focus();
}

// Show loading state
function showLoading() {
    loadingContainer.style.display = 'flex';
    shortenBtn.disabled = true;
    shortenBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Shortening...';
}

// Hide loading state
function hideLoading() {
    loadingContainer.style.display = 'none';
    shortenBtn.disabled = false;
    shortenBtn.innerHTML = '<i class="fas fa-cut"></i> Shorten';
}

// Show result container
function showResult() {
    resultContainer.style.display = 'block';
}

// Hide result container
function hideResult() {
    resultContainer.style.display = 'none';
}

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorContainer.style.display = 'block';
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Hide error message
function hideError() {
    errorContainer.style.display = 'none';
}

// URL validation helper
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// Auto-focus URL input on page load
document.addEventListener('DOMContentLoaded', () => {
    urlInput.focus();
    
    // Add some nice animations
    const elements = document.querySelectorAll('.url-form, .result-card, .error-card');
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            el.style.transition = 'all 0.6s ease';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        urlForm.dispatchEvent(new Event('submit'));
    }
    
    // Escape to reset form
    if (e.key === 'Escape') {
        resetForm();
    }
});

// Add some visual feedback for form interactions
urlInput.addEventListener('input', () => {
    if (urlInput.value.trim()) {
        urlInput.style.borderColor = '#667eea';
    } else {
        urlInput.style.borderColor = '#e1e5e9';
    }
});

// Prevent form submission on Enter if input is empty
urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !urlInput.value.trim()) {
        e.preventDefault();
        showError('Please enter a URL');
    }
});
