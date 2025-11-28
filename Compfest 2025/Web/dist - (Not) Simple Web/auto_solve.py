from math import isqrt
import socket
import re

def long_to_bytes(n: int) -> bytes:
    """Convert long integer to bytes"""
    if n == 0:
        return b'\x00'
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

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

def get_challenge_data(host='localhost', port=1234):
    """Connect to challenge server and get N, e, ct"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    # Get N
    data = sock.recv(4096).decode()
    print("Received:", data)
    N = int(re.search(r'N:\s*(\d+)', data).group(1))
    
    # Send large bound
    bound = str(2**2000)
    print(f"Sending bound: {bound}")
    sock.send((bound + '\n').encode())
    
    # Get e and ct
    data = sock.recv(4096).decode()
    print("Received:", data)
    e = int(re.search(r'e:\s*(\d+)', data).group(1))
    ct = int(re.search(r'ct:\s*(\d+)', data).group(1))
    
    sock.close()
    return N, e, ct

def main():
    print("=== RSA Custom Parameter Auto Solver ===")
    
    # Get server details
    host = input("Server host (default: localhost): ").strip() or 'localhost'
    port = int(input("Server port (default: 1234): ").strip() or '1234')
    
    print(f"\nConnecting to {host}:{port}...")
    
    try:
        # Get challenge data
        N, e, ct = get_challenge_data(host, port)
        print(f"\nChallenge data:")
        print(f"N = {N}")
        print(f"e = {e}")
        print(f"ct = {ct}")
        
        # Solve
        print("\nSolving...")
        flag, (p, q), r = solve(N, e, ct)
        
        print(f"\nSolution:")
        print(f"p bits: {p.bit_length()}, q bits: {q.bit_length()}")
        print(f"r = {r}")
        print(f"FLAG = {flag}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
