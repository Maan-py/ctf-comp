# Writeup: Cerdas Cermath - CTF Crypto Challenge

**Challenge:** Cerdas Cermath  
**Points:** 100  
**Category:** Cryptography  
**Author:** xchopath  
**Connection:** `nc 157.10.160.46 10091`

## Challenge Overview

Challenge ini adalah soal RSA yang mengharuskan kita menyelesaikan 100 stage. Setiap stage memberikan:

- 3 public key RSA (n, e)
- 1 ciphertext (c)
- Kita perlu menentukan key mana yang digunakan untuk enkripsi dan mendekripsi pesan

Pesan yang terenkripsi adalah salah satu dari 5 jawaban berikut:

- "Be Positive, Just Smile"
- "Be Persistent, Jackpot Soon"
- "Break Problems, Just Solve"
- "Beat Procrastination, Just Start"
- "Believe in Progress, Joint Success"

## Vulnerability Analysis

Mari kita analisis source code yang diberikan:

### Key Generation (`crypto_utils.py`)

```python
def generate_keypair(bits: int = BITS, rng: secrets.SystemRandom | None = None) -> RSASecret:
    rng = rng or secrets.SystemRandom()
    max_d = isqrt(isqrt(1 << bits)) // 3
    half_bits = bits // 2
    d_min = max_d // 2

    while True:
        p = getPrime(half_bits)
        q = getPrime(half_bits)
        if p == q:
            continue

        n = p * q
        phi = (p - 1) * (q - 1)

        for _ in range(10_000):
            span = max(1, max_d - d_min)
            d = d_min + rng.randrange(span)

            if gcd(d, phi) != 1:
                continue

            try:
                e = pow(d, -1, phi)
            except ValueError:
                continue

            if e.bit_length() > half_bits:
                return RSASecret(n=n, e=e, d=d, phi=phi)
```

**Vulnerability yang ditemukan:**

1. **Private exponent `d` yang kecil:**

   - `max_d = isqrt(isqrt(1 << bits)) // 3`
   - Untuk 1024-bit RSA: `max_d ≈ 2^256 / 3 ≈ 2^254`
   - `d` dipilih dalam range `[d_min, max_d]` dimana `d_min = max_d // 2`
   - Jadi `d` berada dalam range `[2^253, 2^254]`

2. **Public exponent `e` yang besar:**

   - Karena `d` kecil, dan `e = d^(-1) mod phi`, maka `e` akan menjadi sangat besar
   - Kondisi `e.bit_length() > half_bits` memastikan `e` lebih besar dari 512 bits

3. **Wiener's Attack:**
   - Wiener's attack bekerja ketika `d < n^(1/4) / 3`
   - Untuk 1024-bit n: `n^(1/4) / 3 ≈ 2^256 / 3 ≈ 2^254`
   - Karena `d` berada di sekitar `2^254`, ini tepat berada dalam batas Wiener's attack!

## Solution Approach

### Wiener's Attack

Wiener's attack memanfaatkan continued fraction expansion dari `e/n` untuk menemukan private exponent `d` yang kecil.

**Teori:**

- Jika `d` kecil, maka `k/d` adalah convergent dari continued fraction expansion dari `e/n`
- Dimana `k` adalah bilangan bulat yang memenuhi: `e*d = 1 + k*phi`
- Kita dapat memulihkan `phi` dan kemudian memfaktorkan `n`

**Algoritma:**

1. Hitung continued fraction expansion dari `e/n`
2. Untuk setiap convergent `h/k`:
   - Coba `d = k` sebagai kandidat private exponent
   - Hitung `phi = (e*d - 1) / h` (atau nilai k' lainnya)
   - Verifikasi apakah `phi` valid dengan menyelesaikan persamaan kuadrat untuk mendapatkan `p` dan `q`
   - Jika valid, kita telah menemukan `d`!

### Implementation Strategy

1. **Parse stage data:** Ekstrak 3 public key dan ciphertext dari output server
2. **Try each key:** Untuk setiap public key, coba Wiener's attack
3. **Decrypt:** Jika `d` ditemukan, dekripsi ciphertext
4. **Verify:** Periksa apakah hasil dekripsi adalah salah satu dari 5 jawaban yang valid
5. **Submit:** Kirim jawaban yang benar ke server
6. **Repeat:** Lakukan untuk semua 100 stage

## Implementation

### Code Structure

```python
def wiener_attack(n, e):
    """Wiener's attack untuk menemukan private exponent d yang kecil"""
    # Continued fraction expansion dari e/n
    def continued_fractions(a, b):
        cf = []
        while b != 0:
            q = a // b
            cf.append(q)
            a, b = b, a % b
        return cf

    # Generate convergents
    def convergents(cf):
        h0, h1 = 0, 1
        k0, k1 = 1, 0
        for q in cf:
            h = q * h1 + h0
            k = q * k1 + k0
            yield (h, k)
            h0, h1 = h1, h
            k0, k1 = k1, k

    # Main attack
    cf = continued_fractions(e, n)
    conv = list(convergents(cf))

    for h, k in conv[1:]:  # Skip trivial convergent
        if k == 0:
            continue

        d_candidate = k

        # Try dengan h sebagai k' dalam e*d = 1 + k'*phi
        if h > 0:
            if (e * d_candidate - 1) % h == 0:
                phi = (e * d_candidate - 1) // h
                if phi > 0 and phi < n:
                    # Verify phi dengan menyelesaikan persamaan kuadrat
                    b = n - phi + 1  # p + q
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

    return None, None, None
```

### Main Solving Loop

```python
def main():
    host = "157.10.160.46"
    port = 10091

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    buffer = ""

    while True:
        data = s.recv(4096).decode()
        buffer += data

        if "BPJS? Correct Answer Only ~> " in buffer:
            keys, c = parse_stage(buffer)

            # Try semua key sampai menemukan yang benar
            answer = None
            for n, e in keys:
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
                s.send((answer + "\n").encode())

        if "flag" in buffer.lower() or "congratulations" in buffer.lower():
            # Extract dan print flag
            flag_match = re.search(r'flag\{[^}]+\}', buffer, re.IGNORECASE)
            if flag_match:
                print(f"FLAG: {flag_match.group(0)}")
            break
```

## Execution

### Prerequisites

Script hanya memerlukan Python standard library:

- `socket` untuk koneksi network
- `re` untuk parsing
- `math` untuk perhitungan matematis

Tidak perlu library eksternal seperti `pycryptodome` karena kita implementasikan `long_to_bytes` sendiri.

### Running the Script

Jalankan script:

```bash
python solve.py
```

Script akan:

1. Terhubung ke server `157.10.160.46:10091`
2. Menyelesaikan 100 stage secara otomatis
3. Menampilkan progress untuk setiap stage
4. Menampilkan flag di akhir

**Output:**

```
##### Cerdas Cermath #####

----- Stage [1] -----
Stage 1/100 solved!

True!

----- Stage [2] -----
Stage 2/100 solved!

True!

...

----- Stage [100] -----
Stage 100/100 solved!

True!

Thank you for being so OP...
Congratulations! BPJS{w13n3r_w1en3r_ch1ck3n_d1nn3r_g0tchu!}
```

### Script Features

- **Automatic parsing:** Mengekstrak public keys dan ciphertext dari output server
- **Wiener's attack:** Mencoba semua 3 key sampai menemukan yang benar
- **Validation:** Memverifikasi hasil dekripsi dengan daftar jawaban yang valid
- **Error handling:** Menangani error dengan graceful
- **Progress tracking:** Menampilkan progress untuk setiap stage

## Flag

```
BPJS{w13n3r_w1en3r_ch1ck3n_d1nn3r_g0tchu!}
```

## Mathematical Details

### Why Wiener's Attack Works

Untuk RSA dengan modulus `n = p * q` dan `phi = (p-1)(q-1)`, kita punya:

- `e * d ≡ 1 (mod phi)`
- Jadi: `e * d = 1 + k * phi` untuk beberapa integer `k`

Jika `d` kecil, maka:

- `k` juga relatif kecil
- `e/n ≈ k/d` (karena `phi ≈ n`)
- `k/d` adalah convergent dari continued fraction expansion dari `e/n`

### Example Calculation

Untuk 1024-bit RSA:

- `n ≈ 2^1024`
- `n^(1/4) ≈ 2^256`
- `max_d = n^(1/4) / 3 ≈ 2^254`
- `d` dalam range `[2^253, 2^254]`

Wiener's attack bekerja ketika `d < n^(1/4) / 3`, yang tepat sesuai dengan implementasi challenge ini!

### Verification Process

Setelah menemukan kandidat `d` dari convergent:

1. Hitung `phi = (e*d - 1) / k'` untuk beberapa nilai `k'`
2. Gunakan identitas: `n - phi + 1 = p + q`
3. Selesaikan persamaan kuadrat: `x^2 - (p+q)*x + n = 0`
4. Jika diskriminan adalah perfect square, kita dapat memfaktorkan `n`
5. Verify: `e * d ≡ 1 (mod phi)`

## Key Takeaways

1. **Wiener's Attack:** Sangat efektif ketika private exponent `d` kecil (d < n^(1/4)/3)
2. **Continued Fractions:** Alat matematika yang powerful untuk cryptanalysis
3. **Key Generation:** Harus hati-hati dalam memilih `d` - jangan terlalu kecil!
4. **Automation:** Untuk challenge dengan banyak stage, automation adalah kunci
5. **Verification:** Selalu verifikasi hasil dengan memfaktorkan `n` dan memeriksa relasi RSA

## Conclusion

Challenge ini adalah contoh klasik dari implementasi RSA yang vulnerable terhadap Wiener's attack. Dengan private exponent `d` yang terlalu kecil, kita dapat memulihkan private key hanya dari public key menggunakan continued fraction expansion.

Kunci keberhasilan:

1. **Identifikasi vulnerability:** Mengenali bahwa `d` kecil dari analisis source code
2. **Implementasi attack:** Mengimplementasikan Wiener's attack dengan benar
3. **Automation:** Membuat script yang dapat menyelesaikan 100 stage secara otomatis
4. **Verification:** Memastikan hasil dekripsi valid sebelum mengirim ke server

Challenge ini mengajarkan pentingnya:

- Memilih parameter RSA yang aman
- Memahami berbagai attack pada RSA
- Kemampuan untuk mengotomatisasi proses solving

## References

- Wiener, M. J. (1990). "Cryptanalysis of short RSA secret exponents". IEEE Transactions on Information Theory, 36(3), 553-558.
- Boneh, D. (1999). "Twenty years of attacks on the RSA cryptosystem". Notices of the AMS, 46(2), 203-213.
- Continued Fractions dalam Cryptanalysis
- RSA Cryptosystem

## Files

- `solve.py` - Script solver utama
- `WRITEUP.md` - Writeup ini
- Source code challenge (disediakan dalam distribusi)

---

**Solver:** Auto (AI Assistant)  
**Date:** 2025  
**Tools:** Python, Socket Programming, Wiener's Attack Implementation  
**Time to solve:** ~5-10 menit (untuk 100 stage)
