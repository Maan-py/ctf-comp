#!/usr/bin/env python3

import socket
import re
from math import isqrt, gcd

def long_to_bytes(n):
    """Convert integer to bytes"""
    if n == 0:
        return b'\x00'
    byte_length = (n.bit_length() + 7) // 8
    return n.to_bytes(byte_length, 'big')

# Answers from config
ANSWERS = [
    "Be Positive, Just Smile",
    "Be Persistent, Jackpot Soon",
    "Break Problems, Just Solve",
    "Beat Procrastination, Just Start",
    "Believe in Progress, Joint Success",
]

def parse_stage(data):
    """Parse stage data to extract public keys and ciphertext"""
    keys = []
    c = None
    
    # Extract n and e values
    n_pattern = r'\* n = (\d+)'
    e_pattern = r'\* e = (\d+)'
    c_pattern = r'\* c = (\d+)'
    
    n_matches = re.findall(n_pattern, data)
    e_matches = re.findall(e_pattern, data)
    c_match = re.search(c_pattern, data)
    
    if c_match:
        c = int(c_match.group(1))
    
    for n_str, e_str in zip(n_matches, e_matches):
        keys.append((int(n_str), int(e_str)))
    
    return keys, c

def factor_small_primes(n, limit=1000000):
    """Try to factor n using trial division for small primes"""
    # This is unlikely to work for 1024-bit RSA, but worth trying
    for i in range(2, min(limit, isqrt(n) + 1)):
        if n % i == 0:
            return i, n // i
    return None, None

def wiener_attack(n, e):
    """Wiener's attack for small private exponent d"""
    # Continued fraction expansion of e/n
    def continued_fractions(a, b):
        cf = []
        while b != 0:
            q = a // b
            cf.append(q)
            a, b = b, a % b
        return cf
    
    # Convergents
    def convergents(cf):
        h0, h1 = 0, 1
        k0, k1 = 1, 0
        for q in cf:
            h = q * h1 + h0
            k = q * k1 + k0
            yield (h, k)
            h0, h1 = h1, h
            k0, k1 = k1, k
    
    cf = continued_fractions(e, n)
    conv = list(convergents(cf))
    
    # Wiener's attack: for each convergent h/k of e/n,
    # test if k could be d (the private exponent)
    # The relationship is: e*d = 1 + k'*phi, where k' is typically h
    for h, k in conv[1:]:  # Skip first trivial convergent
        if k == 0:
            continue
        
        d_candidate = k
        
        # In the convergent h/k, h is typically the k' in e*d = 1 + k'*phi
        # So phi = (e*d - 1) / h
        if h > 0:
            if (e * d_candidate - 1) % h == 0:
                phi = (e * d_candidate - 1) // h
                if phi > 0 and phi < n:
                    # Check if phi is valid: n - phi + 1 = p + q
                    # We can solve: x^2 - (p+q)*x + n = 0
                    b = n - phi + 1
                    discriminant = b * b - 4 * n
                    if discriminant >= 0:
                        root = isqrt(discriminant)
                        if root * root == discriminant:
                            p = (b + root) // 2
                            q = (b - root) // 2
                            
                            if p > 0 and q > 0 and p * q == n:
                                # Verify: e*d ≡ 1 (mod phi)
                                phi_check = (p - 1) * (q - 1)
                                if phi_check == phi and (e * d_candidate) % phi_check == 1:
                                    return d_candidate, p, q
        
        # Also try with k' = 1 (in case h doesn't work)
        if (e * d_candidate - 1) % 1 == 0:  # Always true, but let's be explicit
            phi = (e * d_candidate - 1) // 1
            if phi > 0 and phi < n:
                b = n - phi + 1
                discriminant = b * b - 4 * n
                if discriminant >= 0:
                    root = isqrt(discriminant)
                    if root * root == discriminant:
                        p = (b + root) // 2
                        q = (b - root) // 2
                        if p > 0 and q > 0 and p * q == n:
                            phi_check = (p - 1) * (q - 1)
                            if phi_check == phi and (e * d_candidate) % phi_check == 1:
                                return d_candidate, p, q
    
    return None, None, None

def try_decrypt_all_keys(keys, c):
    """Try to decrypt ciphertext with all keys"""
    for i, (n, e) in enumerate(keys):
        print(f"Trying key {i+1}...")
        
        # Try Wiener's attack
        d, p, q = wiener_attack(n, e)
        if d:
            print(f"  Found d using Wiener's attack!")
            m = pow(c, d, n)
            try:
                msg = long_to_bytes(m).decode()
                if msg in ANSWERS:
                    print(f"  Valid message found: {msg}")
                    return msg
            except:
                pass
        
        # Try to factor n (unlikely but worth trying)
        p, q = factor_small_primes(n)
        if p and q:
            print(f"  Factored n!")
            phi = (p - 1) * (q - 1)
            d = pow(e, -1, phi)
            m = pow(c, d, n)
            try:
                msg = long_to_bytes(m).decode()
                if msg in ANSWERS:
                    print(f"  Valid message found: {msg}")
                    return msg
            except:
                pass
    
    return None

def solve_stage(keys, c):
    """Solve a single stage"""
    # Try each key
    for i, (n, e) in enumerate(keys):
        print(f"\nTrying key {i+1}: n={n}, e={e}")
        
        # Check if e is large (which suggests d is small)
        if e.bit_length() > 512:  # half_bits = 512
            print(f"  Large e detected ({e.bit_length()} bits), trying Wiener's attack...")
            d, p, q = wiener_attack(n, e)
            if d:
                print(f"  Success! d found")
                m = pow(c, d, n)
                try:
                    msg = long_to_bytes(m).decode()
                    print(f"  Decrypted: {msg}")
                    if msg in ANSWERS:
                        return msg
                except:
                    print(f"  Decryption failed (not valid text)")
        
        # Also try if we can compute d directly (if n is factorable)
        # This is very unlikely for 1024-bit RSA, but let's try
        
    return None

def main():
    host = "157.10.160.46"
    port = 10091
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    buffer = ""
    
    try:
        while True:
            data = s.recv(4096).decode()
            if not data:
                break
            
            buffer += data
            # Print banner, stage info, and anything with flag/congratulations
            if "#####" in data or "Stage [" in data or "flag" in data.lower() or "congratulations" in data.lower() or "Thank you" in data:
                print(data, end='')
            
            # Check if we need to send an answer
            if "BPJS? Correct Answer Only ~> " in buffer:
                # Extract stage data
                keys, c = parse_stage(buffer)
                
                if keys and c:
                    # Try to solve - try all keys
                    # The vulnerability is that d is small (around 2^254 bits for 1024-bit n)
                    # This makes e large, so we should try Wiener's attack on all keys
                    answer = None
                    for i, (n, e) in enumerate(keys):
                        # Try Wiener's attack (d is small by design, so e will be large)
                        d, p, q = wiener_attack(n, e)
                        if d:
                            m = pow(c, d, n)
                            try:
                                msg = long_to_bytes(m).decode()
                                if msg in ANSWERS:
                                    answer = msg
                                    break
                            except:
                                pass
                    
                    if answer:
                        # Extract stage number for progress
                        stage_match = re.search(r'Stage \[(\d+)\]', buffer)
                        if stage_match:
                            stage_num = stage_match.group(1)
                            print(f"Stage {stage_num}/100 solved!", flush=True)
                        s.send((answer + "\n").encode())
                    else:
                        print("\n[ERROR] Could not decrypt any key!")
                        # Try sending first answer as fallback (should fail)
                        s.send((ANSWERS[0] + "\n").encode())
                
                buffer = ""
            
            # Check if we got the flag
            if "flag" in buffer.lower() or "congratulations" in buffer.lower():
                print("\n" + "="*70)
                print("FLAG FOUND!")
                print("="*70)
                # Extract and print flag
                flag_match = re.search(r'flag\{[^}]+\}', buffer, re.IGNORECASE)
                if flag_match:
                    print(f"\nFLAG: {flag_match.group(0)}\n")
                print(buffer)
                print("="*70)
                break
                
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        s.close()

if __name__ == "__main__":
    main()

