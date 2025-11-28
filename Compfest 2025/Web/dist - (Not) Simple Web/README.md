# RSA Custom Parameter - CTF Challenge Exploit

## Challenge Analysis

Challenge ini menggunakan implementasi RSA yang tidak standar dengan beberapa kerentanan:

### Kerentanan Utama:

1. **Kontrol atas bound parameter**: Program memungkinkan kita mengontrol parameter `bound` yang digunakan untuk menghasilkan private key `d`
2. **RSA dengan phi tidak standar**: Menggunakan `phi = (p²-1)(q²-1)` bukan `phi = (p-1)(q-1)`
3. **Faktor p dan q yang berdekatan**: Kondisi `(p < q < 2*p) atau (q < p < 2*q)`

### Strategi Eksploitasi:

1. **Wiener Attack**: Dengan memilih `bound` yang sangat besar, kita bisa membuat `d` sangat kecil, yang membuat `e` sangat besar
2. **Fermat Factorization**: Karena p dan q berdekatan, kita bisa menggunakan metode Fermat untuk memfaktorkan N

## Cara Menggunakan

### 1. Script Utama (main_exploit.py)

```bash
python main_exploit.py
```

Script ini akan:

- Terhubung ke server
- Mengirim bound yang sangat besar (2^2000)
- Mencoba Wiener attack
- Jika gagal, mencoba Fermat factorization

### 2. Testing Lokal (local_test.py)

```bash
python local_test.py
```

Untuk testing dengan simulasi server lokal.

### 3. Script Interaktif (interactive_exploit.py)

```bash
python interactive_exploit.py
```

Versi yang lebih detail dengan output verbose.

## Alur Eksploitasi

1. **Koneksi ke Server**:

   ```
   Server: Generating public key....
   Server: N: <large_number>
   You: Enter bound: 2^2000
   Server: Done!
   Server: e: <very_large_number>
   Server: ct: <ciphertext>
   ```

2. **Wiener Attack**:

   - Dengan `bound` yang sangat besar, `d` akan sangat kecil
   - `e` akan sangat besar
   - Gunakan continued fraction expansion untuk menemukan `d`

3. **Fermat Factorization** (backup):
   - Karena p dan q berdekatan, gunakan metode Fermat
   - Setelah dapat p dan q, hitung phi dan d
   - Decrypt ciphertext

## Dependencies

```bash
pip install pycryptodome gmpy2
```

## Contoh Output

```
=== RSA Custom Parameter Exploit ===

Connecting to localhost:1234...

Parameters:
N = 123456789...
e = 987654321...
ct = 111222333...

Running Wiener attack...
Testing d = 12345
SUCCESS! Flag: COMPFEST{flag_here}
```

## Tips

1. **Bound Selection**: Gunakan bound yang sangat besar (2^2000 atau lebih) untuk memastikan d sangat kecil
2. **Multiple Attempts**: Jika Wiener attack gagal, coba dengan bound yang berbeda
3. **Fermat Backup**: Selalu ada Fermat factorization sebagai backup karena p dan q berdekatan
4. **Flag Detection**: Script akan mencari pola flag seperti 'COMPFEST', 'flag', atau '{'

## Vulnerability Details

```python
# Kerentanan dalam generate_pub_key():
bound = int(input("Enter bound: "))
if bound < 2**1000:
    print("Get out of here!")
    exit(1)
while True:
    d = randint(phi-bound,phi-1)  # d bisa sangat kecil jika bound besar
    if gcd(d,phi) == 1:
        break
e = pow(d,-1,phi)  # e akan sangat besar jika d kecil
```

Dengan memilih bound yang sangat besar, kita bisa membuat d sangat kecil, yang merupakan kondisi ideal untuk Wiener attack.
