// Dark Mode Content Script
(function() {
    'use strict';
    
    // Apply dark mode CSS
    const darkModeCSS = `
        html {
            filter: invert(90%) hue-rotate(180deg) !important;
            background-color: #1a1a1a !important;
        }
        img, video, iframe {
            filter: invert(100%) hue-rotate(180deg) !important;
        }
    `;
    
    const style = document.createElement('style');
    style.textContent = darkModeCSS;
    document.head.appendChild(style);
    
    console.log('Dark Mode Plus: Theme applied');
})();
