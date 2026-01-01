// Popup script for Deepfake Detector Chrome Extension

let selectedFile = null;
let previewUrl = null;
let imageUrl = null;

// DOM elements
const fileInput = document.getElementById('file-input');
const uploadPlaceholder = document.getElementById('upload-placeholder');
const imagePreview = document.getElementById('image-preview');
const previewImage = document.getElementById('preview-image');
const clearButton = document.getElementById('clear-button');
const actions = document.getElementById('actions');
const analyzeButton = document.getElementById('analyze-button');
const errorMessage = document.getElementById('error-message');
const resultsSection = document.getElementById('results-section');
const resultsContent = document.getElementById('results-content');
const scanPageButton = document.getElementById('scan-page-button');
const clearBadgesButton = document.getElementById('clear-badges-button');

// Check for image URL from context menu on load
chrome.storage.local.get(['imageUrl'], (result) => {
  if (result.imageUrl) {
    imageUrl = result.imageUrl;
    // Clear the stored URL and badge
    chrome.storage.local.remove(['imageUrl']);
    chrome.action.setBadgeText({ text: '' });
    // Load and analyze the image
    loadImageFromUrl(imageUrl);
  }
});

// File input handler
fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    selectedFile = file;
    showImagePreview(file);
    showActions();
    hideError();
    hideResults();
  }
});

// Clear button handler
clearButton.addEventListener('click', () => {
  clearSelection();
});

// Scan page button handler
scanPageButton.addEventListener('click', async () => {
  scanPageButton.disabled = true;
  scanPageButton.textContent = 'Scanning...';
  hideError();
  
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (!tab || !tab.url) {
      throw new Error('No active tab found');
    }
    
    // Check if URL is a valid web page (not chrome://, edge://, etc.)
    if (tab.url.startsWith('chrome://') || tab.url.startsWith('edge://') || 
        tab.url.startsWith('chrome-extension://') || tab.url.startsWith('about:')) {
      throw new Error('Cannot scan system pages. Please navigate to a regular webpage.');
    }
    
    // Inject content script if not already injected
    try {
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
      });
    } catch (injectError) {
      // Script might already be injected, that's okay
      console.log('Script injection note:', injectError.message);
    }
    
    // Wait a bit for script to initialize
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Send message to content script
    chrome.tabs.sendMessage(tab.id, { action: 'scanPage' }, (response) => {
      if (chrome.runtime.lastError) {
        console.error('Error:', chrome.runtime.lastError);
        showError('Failed to scan page. Try refreshing the page and clicking Scan again.');
        scanPageButton.disabled = false;
        scanPageButton.textContent = 'Scan This Page';
      } else {
        // Success
        scanPageButton.disabled = false;
        scanPageButton.textContent = 'Scan Complete!';
        setTimeout(() => {
          scanPageButton.textContent = 'Scan This Page';
        }, 3000);
      }
    });
  } catch (err) {
    console.error('Scan error:', err);
    showError(err.message || 'Failed to scan page. Make sure you\'re on a valid webpage.');
    scanPageButton.disabled = false;
    scanPageButton.textContent = 'Scan This Page';
  }
});

// Clear badges button handler
clearBadgesButton.addEventListener('click', async () => {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.tabs.sendMessage(tab.id, { action: 'clearBadges' }, (response) => {
      if (chrome.runtime.lastError) {
        console.error('Error:', chrome.runtime.lastError);
      }
    });
  } catch (err) {
    console.error('Error clearing badges:', err);
  }
});

// Analyze button handler
analyzeButton.addEventListener('click', async () => {
  if (!selectedFile && !imageUrl) {
    showError('Please select an image first');
    return;
  }

  setLoading(true);
  hideError();
  hideResults();

  try {
    let formData = new FormData();
    
    if (imageUrl) {
      // Fetch image from URL and convert to blob
      const response = await fetch(imageUrl);
      if (!response.ok) {
        throw new Error('Failed to fetch image from URL');
      }
      const blob = await response.blob();
      formData.append('image', blob, 'image.png');
    } else {
      formData.append('image', selectedFile);
    }

    const response = await fetch('http://localhost:5000/api/detect', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `Server error: ${response.status}`);
    }

    const data = await response.json();

    if (data.success !== false) {
      showResults(data);
    } else {
      showError(data.error || 'Failed to analyze image');
    }
  } catch (err) {
    const errorMsg = err.message.includes('Failed to fetch') || err.message.includes('network')
      ? 'Failed to connect to backend. Make sure the backend is running on http://localhost:5000'
      : err.message;
    showError(errorMsg);
  } finally {
    setLoading(false);
  }
});

function showImagePreview(file) {
  if (previewUrl) {
    URL.revokeObjectURL(previewUrl);
  }

  previewUrl = URL.createObjectURL(file);
  previewImage.src = previewUrl;
  uploadPlaceholder.style.display = 'none';
  imagePreview.style.display = 'block';
}

async function loadImageFromUrl(url) {
  try {
    setLoading(true);
    hideError();
    hideResults();
    
    // Store the URL for analysis
    imageUrl = url;
    
    // Show preview
    previewUrl = url;
    previewImage.src = url;
    uploadPlaceholder.style.display = 'none';
    imagePreview.style.display = 'block';
    showActions();
    
    setLoading(false);
    
    // Automatically analyze
    analyzeButton.click();
  } catch (err) {
    setLoading(false);
    showError('Failed to load image: ' + err.message);
  }
}

function clearSelection() {
  selectedFile = null;
  imageUrl = null;
  if (previewUrl && previewUrl.startsWith('blob:')) {
    URL.revokeObjectURL(previewUrl);
  }
  previewUrl = null;
  fileInput.value = '';
  uploadPlaceholder.style.display = 'flex';
  imagePreview.style.display = 'none';
  actions.style.display = 'none';
  hideError();
  hideResults();
}

function showActions() {
  actions.style.display = 'block';
}

function hideError() {
  errorMessage.style.display = 'none';
  errorMessage.textContent = '';
}

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.style.display = 'block';
}

function setLoading(loading) {
  analyzeButton.disabled = loading;
  analyzeButton.textContent = loading ? 'Analyzing...' : 'Analyze Image';
}

function hideResults() {
  resultsSection.style.display = 'none';
}

function showResults(data) {
  resultsContent.innerHTML = generateResultsHTML(data);
  resultsSection.style.display = 'block';
}

function generateResultsHTML(data) {
  return `
    <div class="prediction-card">
      <div class="prediction-header">
        <span class="prediction-label">Prediction</span>
        <span class="prediction-value">${data.prediction}</span>
      </div>
      <div class="confidence-bar">
        <div class="confidence-fill" style="width: ${data.confidence}%"></div>
        <span class="confidence-text">${data.confidence}% confidence</span>
      </div>
    </div>

    <div class="probabilities">
      <div class="prob-item">
        <span class="prob-label">Fake</span>
        <div class="prob-bar">
          <div class="prob-fill" style="width: ${data.probabilities.fake}%"></div>
        </div>
        <span class="prob-value">${data.probabilities.fake}%</span>
      </div>
      <div class="prob-item">
        <span class="prob-label">Real</span>
        <div class="prob-bar">
          <div class="prob-fill" style="width: ${data.probabilities.real}%"></div>
        </div>
        <span class="prob-value">${data.probabilities.real}%</span>
      </div>
    </div>

    <div class="info-section">
      <h3>Interpretation</h3>
      <p style="font-size: 0.8125rem; line-height: 1.6; color: #333;">${data.interpretation}</p>
    </div>

    <div class="info-section">
      <h3>Model Information</h3>
      <div class="info-item">
        <span class="info-label">Model</span>
        <span class="info-value">${data.model_info.model_name.split('/')[1]}</span>
      </div>
      <div class="info-item">
        <span class="info-label">Device</span>
        <span class="info-value">${data.model_info.device.toUpperCase()}</span>
      </div>
      <div class="info-item">
        <span class="info-label">Framework</span>
        <span class="info-value">${data.model_info.framework}</span>
      </div>
    </div>

    <div class="info-section">
      <h3>Analysis Details</h3>
      <div class="info-item">
        <span class="info-label">Image Size</span>
        <span class="info-value">${data.analysis.image_size[0]} × ${data.analysis.image_size[1]} px</span>
      </div>
      <div class="info-item">
        <span class="info-label">Inference Time</span>
        <span class="info-value">${data.analysis.inference_time} ms</span>
      </div>
      <div class="info-item">
        <span class="info-label">Total Time</span>
        <span class="info-value">${data.analysis.total_time} ms</span>
      </div>
    </div>
  `;
}

