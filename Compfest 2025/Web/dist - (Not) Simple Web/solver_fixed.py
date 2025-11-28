from math import isqrt

def long_to_bytes(n: int) -> bytes:
    """Convert long integer to bytes"""
    if n == 0:
        return b'\x00'
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

def inverse(a: int, m: int) -> int:
    """Calculate modular multiplicative inverse"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m

def is_square(n: int) -> bool:
    if n < 0: 
        return False
    r = isqrt(n)
    return r*r == n

def recover_pq_from_phi_prime(N: int, e: int):
    # r ≈ ((N-1)^2)/e
    r_est = ( (N - 1)**2 ) // e
    for delta in range(-3, 4):  # kecil saja; biasanya ±1 sudah cukup
        r = r_est + delta
        if r <= 0: 
            continue
        phi_prime = e*r + 1
        # Δ = (N+1)^2 - φ' = (p+q)^2  → harus kuadrat sempurna
        Delta = (N + 1)**2 - phi_prime
        if not is_square(Delta):
            continue
        S = isqrt(Delta)   # p + q
        D = S*S - 4*N      # (p - q)^2
        if not is_square(D):
            continue
        t = isqrt(D)
        p = (S + t) // 2
        q = (S - t) // 2
        if p*q == N and p>1 and q>1:
            # pastikan p ≥ q
            if p < q: p, q = q, p
            return p, q, r, phi_prime
    return None, None, None, None

def solve(N: int, e: int, ct: int):
    p, q, r, phi_prime = recover_pq_from_phi_prime(N, e)
    if not p:
        raise ValueError("Gagal memulihkan p,q. Coba perluas rentang pencarian r.")
    # d = φ' - r (sesuai konstruksi keygen)
    d = phi_prime - r
    # (opsional) verifikasi: (e*d) % phi_prime == 1
    assert (e*d) % phi_prime == 1
    m = pow(ct, d, N)
    pt = long_to_bytes(m)
    return pt, (p, q), r

# ==== ISI DARI CHALLENGE DI SINI ====
N  = int("PASTE_N_INTEGER_HERE")
e  = int("PASTE_E_INTEGER_HERE")
ct = int("PASTE_CT_INTEGER_HERE")

flag, (p, q), r = solve(N, e, ct)
print("p bits:", p.bit_length(), " q bits:", q.bit_length())
print("r =", r)
print("FLAG =", flag)
