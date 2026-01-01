// Content script to automatically detect and analyze images on the page

(function() {
  'use strict';

  const API_URL = 'http://localhost:5000/api/detect';
  const analyzedImages = new Map(); // Cache to avoid re-analyzing same images

  // Style for badges
  const badgeStyle = `
    .deepfake-image-wrapper {
      position: relative !important;
      display: inline-block !important;
    }
    .deepfake-image-wrapper img {
      display: block !important;
      max-width: 100% !important;
      height: auto !important;
    }
    .deepfake-badge {
      position: absolute !important;
      top: 8px !important;
      left: 8px !important;
      padding: 6px 12px !important;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
      font-size: 11px !important;
      font-weight: 600 !important;
      letter-spacing: 0.5px !important;
      text-transform: uppercase !important;
      border: 2px solid !important;
      z-index: 2147483647 !important;
      pointer-events: none !important;
      box-shadow: 0 2px 8px rgba(0,0,0,0.5) !important;
      white-space: nowrap !important;
      line-height: 1.2 !important;
    }
    .deepfake-badge.real {
      background-color: #ffffff !important;
      color: #000000 !important;
      border-color: #000000 !important;
    }
    .deepfake-badge.fake {
      background-color: #000000 !important;
      color: #ffffff !important;
      border-color: #ffffff !important;
    }
    .deepfake-badge.analyzing {
      background-color: #666666 !important;
      color: #ffffff !important;
      border-color: #666666 !important;
    }
    .deepfake-badge.error {
      background-color: #ff0000 !important;
      color: #ffffff !important;
      border-color: #ffffff !important;
    }
  `;

  // Inject styles
  const styleSheet = document.createElement('style');
  styleSheet.textContent = badgeStyle;
  document.head.appendChild(styleSheet);

  // Add badge to image
  function addBadge(img, type, text) {
    // Remove existing badge first
    removeBadge(img);

    // Check if image is still in DOM
    if (!document.body.contains(img)) {
      console.log('Image no longer in DOM, skipping badge');
      return;
    }

    // Wrap image if not already wrapped
    let wrapper = img.parentElement;
    if (!wrapper || !wrapper.classList.contains('deepfake-image-wrapper')) {
      // Create wrapper
      wrapper = document.createElement('div');
      wrapper.className = 'deepfake-image-wrapper';
      
      // Insert wrapper before image
      if (img.parentNode) {
        img.parentNode.insertBefore(wrapper, img);
        // Move image into wrapper
        wrapper.appendChild(img);
      } else {
        console.log('Image has no parent, cannot wrap');
        return;
      }
    }

    // Create badge
    const badge = document.createElement('div');
    badge.className = `deepfake-badge ${type}`;
    badge.textContent = text;
    wrapper.appendChild(badge);
    
    console.log(`Badge added: ${text} (${type}) on image`, img.src?.substring(0, 50));
  }

  // Remove badge from image (but keep wrapper)
  function removeBadge(img) {
    const wrapper = img.closest('.deepfake-image-wrapper');
    if (wrapper) {
      const badge = wrapper.querySelector('.deepfake-badge');
      if (badge) {
        badge.remove();
      }
    }
  }

  // Send image to backend
  async function sendToBackend(blob, img, imgSrc) {
    try {
      const formData = new FormData();
      formData.append('image', blob, 'image.png');

      console.log('Sending image to backend:', API_URL);
      const apiResponse = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      });

      if (!apiResponse.ok) {
        const errorText = await apiResponse.text().catch(() => 'Unknown error');
        console.error('API error:', apiResponse.status, errorText);
        throw new Error(`API request failed: ${apiResponse.status} - ${errorText}`);
      }

      const data = await apiResponse.json();
      console.log('API response:', data);
      
      if (data.success !== false && data.prediction) {
        const prediction = data.prediction.toLowerCase();
        const confidence = data.confidence || 0;
        analyzedImages.set(imgSrc, { 
          status: 'done', 
          prediction: prediction,
          confidence: confidence 
        });
        addBadge(img, prediction, `${prediction.toUpperCase()} (${confidence}%)`);
        console.log(`✓ Image analyzed: ${prediction.toUpperCase()} (${confidence}%) - ${imgSrc.substring(0, 50)}...`);
      } else {
        throw new Error('Invalid response from API: ' + JSON.stringify(data));
      }
    } catch (error) {
      console.error('Error in sendToBackend:', error);
      throw error; // Re-throw to be caught by analyzeImage
    }
  }

  // Analyze a single image
  async function analyzeImage(img) {
    const imgSrc = img.src || img.currentSrc || img.getAttribute('src');
    if (!imgSrc || imgSrc.startsWith('data:') || imgSrc.trim() === '') {
      return; // Skip data URLs and empty src
    }

    // Skip if already analyzed or currently analyzing
    if (analyzedImages.has(imgSrc)) {
      const status = analyzedImages.get(imgSrc).status;
      if (status === 'done' || status === 'analyzing') {
        return;
      }
    }

    // Mark as analyzing
    analyzedImages.set(imgSrc, { status: 'analyzing' });
    addBadge(img, 'analyzing', 'Analyzing...');

    try {
      // Fetch image and convert to blob
      let response;
      try {
        response = await fetch(imgSrc, { mode: 'cors' });
      } catch (fetchError) {
        // Try using canvas to convert image to blob as fallback
        console.warn('CORS error, trying canvas method:', fetchError);
        try {
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          const width = img.naturalWidth || img.width || 500;
          const height = img.naturalHeight || img.height || 500;
          canvas.width = width;
          canvas.height = height;
          ctx.drawImage(img, 0, 0);
          
          // Wait for canvas to blob conversion
          const blob = await new Promise((resolve, reject) => {
            canvas.toBlob((blob) => {
              if (blob) {
                resolve(blob);
              } else {
                reject(new Error('Failed to convert image to blob'));
              }
            }, 'image/png');
          });
          
          await sendToBackend(blob, img, imgSrc);
          return;
        } catch (canvasError) {
          console.error('Canvas method also failed:', canvasError);
          throw new Error('Failed to fetch image: ' + fetchError.message);
        }
      }
      
      if (!response.ok) {
        throw new Error(`Failed to fetch image: ${response.status}`);
      }
      const blob = await response.blob();
      await sendToBackend(blob, img, imgSrc);
    } catch (error) {
      console.error('Error analyzing image:', error, imgSrc);
      analyzedImages.set(imgSrc, { status: 'error' });
      // Show error badge (keep it visible)
      addBadge(img, 'error', 'Error: ' + error.message.substring(0, 20));
    }
  }

  // Scan page for images
  function scanPage() {
    const allImages = Array.from(document.querySelectorAll('img'));
    const images = allImages.filter(img => {
      // Filter out very small images (likely icons/sprites)
      const width = img.naturalWidth || img.width || 0;
      const height = img.naturalHeight || img.height || 0;
      return width > 50 && height > 50; // Only analyze images larger than 50x50
    });
    
    console.log(`Content script: Found ${images.length} images to analyze (filtered from ${allImages.length} total)`);

    if (images.length === 0) {
      console.log('No images found to analyze');
      return;
    }

    // Analyze first 10 images initially (to avoid overwhelming backend)
    const imagesToAnalyze = images.slice(0, 10);
    
    imagesToAnalyze.forEach((img, index) => {
      // Wait a bit between requests to avoid overwhelming the backend
      setTimeout(() => {
        analyzeImage(img);
      }, index * 300); // 300ms delay between each image
    });
    
    // If there are more images, analyze them after a delay
    if (images.length > 10) {
      setTimeout(() => {
        images.slice(10).forEach((img, index) => {
          setTimeout(() => {
            analyzeImage(img);
          }, index * 300);
        });
      }, 5000);
    }
  }

  // Listen for messages from popup
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'scanPage') {
      console.log('Content script: Received scanPage request');
      scanPage();
      sendResponse({ success: true, message: 'Scan started' });
      return true; // Keep channel open for async response
    } else if (request.action === 'clearBadges') {
      console.log('Content script: Received clearBadges request');
      document.querySelectorAll('.deepfake-badge').forEach(badge => badge.remove());
      document.querySelectorAll('.deepfake-image-wrapper').forEach(wrapper => {
        const img = wrapper.querySelector('img');
        if (img && wrapper.parentNode) {
          wrapper.parentNode.insertBefore(img, wrapper);
          wrapper.remove();
        }
      });
      analyzedImages.clear();
      sendResponse({ success: true, message: 'Badges cleared' });
      return true;
    }
    return false;
  });

  // Don't auto-scan on page load - wait for user to click "Scan This Page"
  console.log('Deepfake Detector content script loaded. Click "Scan This Page" in the extension popup to start.');

})();
