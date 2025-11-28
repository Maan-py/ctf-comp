document.addEventListener('DOMContentLoaded', function() {
    const enableToggle = document.getElementById('enableToggle');
    const syncBtn = document.getElementById('syncBtn');
    const status = document.getElementById('status');
    
    // Load current state
    chrome.storage.local.get(['enabled'], function(result) {
        enableToggle.checked = result.enabled !== false;
    });
    
    // Toggle handler
    enableToggle.addEventListener('change', function() {
        chrome.runtime.sendMessage({
            action: 'toggleTheme'
        }, function(response) {
            status.textContent = enableToggle.checked ? 
                'Dark mode enabled' : 'Dark mode disabled';
        });
    });
    
    // Sync button handler
    syncBtn.addEventListener('click', function() {
        status.textContent = 'Syncing...';
        chrome.runtime.sendMessage({
            action: 'manualSync'
        }, function(response) {
            status.textContent = 'Sync completed! Check console for details.';
            setTimeout(() => {
                status.textContent = 'Extension active';
            }, 3000);
        });
    });
});
