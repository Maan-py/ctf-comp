from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from random import randint
from math import gcd
import gmpy2

# Simulate the challenge
FLAG = b"COMPFEST{test_flag_here}"

def generate_pub_key_simulated(bound):
    """Simulate the server's key generation"""
    while True:
        p = getPrime(512)  # Smaller for testing
        q = getPrime(512)
        if (p < q < 2*p) or (q < p < 2*q):
            break
    
    N = p * q
    phi = (p**2-1) * (q**2-1)
    
    # Generate d in range [phi-bound, phi-1]
    while True:
        d = randint(phi-bound, phi-1)
        if gcd(d, phi) == 1:
            break
    
    e = pow(d, -1, phi)
    return N, e, d, p, q

def encrypt(m, N, e):
    m = bytes_to_long(m)
    ct = pow(m, e, N)
    return ct

def continued_fraction(e, n):
    """Compute continued fraction expansion of e/n"""
    cf = []
    while n:
        q, r = divmod(e, n)
        cf.append(q)
        e, n = n, r
    return cf

def convergents(cf):
    """Compute convergents from continued fraction"""
    convergents = []
    for i in range(len(cf)):
        num, den = 1, 0
        for j in range(i, -1, -1):
            num, den = den, num
            num += cf[j] * den
        convergents.append((num, den))
    return convergents

def wiener_attack(e, n, ct):
    """Wiener's attack on RSA with small private exponent"""
    print("Attempting Wiener attack...")
    cf = continued_fraction(e, n)
    convergents_list = convergents(cf)
    
    for i, (k, d) in enumerate(convergents_list):
        if k == 0 or d == 0:
            continue
            
        # Check if this d could be the private key
        if e * d % k == 1:
            print(f"Found potential d: {d}")
            # Try to decrypt
            try:
                pt = pow(ct, d, n)
                flag = long_to_bytes(pt)
                if b'COMPFEST' in flag or b'flag' in flag.lower() or b'{' in flag:
                    print(f"SUCCESS! Flag: {flag}")
                    return flag
            except:
                continue
    
    print("Wiener attack failed")
    return None

def fermat_factor(n):
    """Fermat's factorization method for numbers with close factors"""
    print("Attempting Fermat factorization...")
    a = gmpy2.isqrt(n)
    if a * a == n:
        return a, a
    
    a += 1
    count = 0
    while count < 100000:  # Limit iterations for testing
        b2 = a * a - n
        b = gmpy2.isqrt(b2)
        if b * b == b2:
            p = a + b
            q = a - b
            print(f"Found factors: p={p}, q={q}")
            return p, q
        a += 1
        count += 1
    
    print("Fermat factorization failed")
    return None, None

def decrypt_with_factors(ct, e, p, q):
    """Decrypt using factors p and q"""
    n = p * q
    # For this challenge: phi = (p²-1)(q²-1)
    phi = (p*p - 1) * (q*q - 1)
    d = pow(e, -1, phi)
    pt = pow(ct, d, n)
    return long_to_bytes(pt)

def main():
    print("=== RSA Custom Parameter Local Test ===")
    print()
    
    # Test with different bounds
    bounds = [2**100, 2**200, 2**300, 2**400]
    
    for bound in bounds:
        print(f"\n--- Testing with bound = 2^{bound.bit_length()-1} ---")
        
        # Generate keys
        N, e, d_real, p, q = generate_pub_key_simulated(bound)
        print(f"N = {N}")
        print(f"e = {e}")
        print(f"Real d = {d_real}")
        print(f"p = {p}, q = {q}")
        
        # Encrypt flag
        ct = encrypt(FLAG, N, e)
        print(f"ct = {ct}")
        
        # Try Wiener attack
        flag = wiener_attack(e, N, ct)
        if flag:
            print("Wiener attack succeeded!")
            continue
        
        # Try Fermat factorization
        p_found, q_found = fermat_factor(N)
        if p_found and q_found:
            flag = decrypt_with_factors(ct, e, p_found, q_found)
            print(f"Fermat factorization succeeded! Flag: {flag}")
            continue
        
        print("Both attacks failed for this bound")
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    main()
