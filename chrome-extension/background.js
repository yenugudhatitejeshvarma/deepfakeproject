// Background service worker for Deepfake Detector extension

chrome.runtime.onInstalled.addListener(() => {
  console.log('Deepfake Detector extension installed');
  
  // Create context menu item
  chrome.contextMenus.create({
    id: 'detect-deepfake',
    title: 'Detect Deepfake',
    contexts: ['image']
  });
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'detect-deepfake' && info.srcUrl) {
    // Store the image URL
    chrome.storage.local.set({ imageUrl: info.srcUrl }, () => {
      // Show badge to indicate image is ready
      chrome.action.setBadgeText({ text: '1' });
      chrome.action.setBadgeBackgroundColor({ color: '#000000' });
      
      // Try to open popup (may not work in all contexts, but popup will check on load)
      chrome.action.openPopup(() => {
        // If popup failed to open, user can click extension icon
        // The popup will automatically load the image when opened
      });
    });
  }
});

