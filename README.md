# CTF Journey

Repositori dokumentasi perjalanan CTF (Capture The Flag) yang berisi write-up, solusi, dan exploit script dari berbagai kompetisi CTF yang telah diikuti.

## 📋 Daftar Isi

- [Tentang Repository](#tentang-repository)
- [Struktur Repository](#struktur-repository)
- [Kompetisi yang Diikuti](#kompetisi-yang-diikuti)
- [Kategori Challenge](#kategori-challenge)
- [Teknologi & Tools](#teknologi--tools)
- [Cara Menggunakan](#cara-menggunakan)
- [Disclaimer](#disclaimer)

## 🎯 Tentang Repository

Repository ini berisi dokumentasi lengkap dari berbagai kompetisi CTF yang telah diikuti, termasuk:

- **Write-up** dan dokumentasi solusi
- **Exploit scripts** untuk berbagai kategori challenge
- **Analisis vulnerability** dan teknik eksploitasi
- **Source code** dari challenge yang telah diselesaikan
- **PDF write-up** dari berbagai tim

Repository ini digunakan sebagai referensi pembelajaran dan dokumentasi perjalanan dalam dunia cybersecurity.

## 📁 Struktur Repository

```
CTF-Journey/
├── Solver/                          # Script dan code umum
│   ├── file-upload.php
│   ├── htb-bac.js                 # HackTheBox Broken Access Control exploit
│   └── xxe.py                     # XXE exploitation script
│
├── Compfest 2025/                 # Kompetisi Compfest 2025
│   ├── Blockchain/
│   ├── Crypto/
│   ├── Forensic/
│   ├── Misc/
│   └── Web/
│
├── Cyberkarta 2025/               # Kompetisi Cyberkarta 2025
│
├── FindIT 2025/                   # Kompetisi FindIT 2025
│   ├── D-Day/
│   ├── Warmup/
│   └── Write up official.txt
│
├── FIT 2025/                      # Kompetisi FIT 2025
│
├── Gemastik 2025/                 # Kompetisi Gemastik 2025
│   ├── Binary Exploitation/
│   ├── Cryptography/
│   ├── Forensic/
│   └── Reverse Engineering/
│
├── Healthkathon BPJS 2025/        # Kompetisi Healthkathon BPJS 2025
│   ├── Crypto/
│   ├── Digital Forensics/
│   ├── Pwn/
│   ├── Reverse Engineering/
│   └── Web Exploitation/
│
├── HTB/                          # HackTheBox challenges
│   └── HackTheBoo 2025/
│
├── NCS Aptikom 2025/             # Kompetisi NCS Aptikom 2025
│   ├── Final/
│   └── Qual/
│
├── Permifest 2025/               # Kompetisi Permifest 2025
│
├── Rise the Range 2025/          # Kompetisi Rise the Range 2025
│
└── Wreck IT 6.0 2025/            # Kompetisi Wreck IT 6.0 2025
    ├── General/
    ├── Junior/
    ├── Reverse Engineering/
    └── Web/
```

## 🏆 Kompetisi yang Diikuti

### 2025

1. **Compfest 2025**

   - Kategori: Blockchain, Crypto, Forensic, Misc, Web
   - Status: ✅ Completed
   - Write-up tersedia untuk beberapa challenge

2. **FindIT 2025**

   - Kategori: Crypto, Forensic, Misc, OSINT, PWN, Reverse, Web
   - Status: ✅ Completed
   - Write-up official tersedia

3. **Gemastik 2025**

   - Kategori: Binary Exploitation, Cryptography, Forensic, Reverse Engineering
   - Status: ✅ Completed
   - Multiple write-up PDF tersedia

4. **Healthkathon BPJS 2025**

   - Kategori: Crypto, Digital Forensics, Pwn, Reverse Engineering, Web Exploitation
   - Status: ✅ Completed
   - Write-up tersedia untuk beberapa challenge

5. **NCS Aptikom 2025**

   - Kategori: Qualifying & Final rounds
   - Status: ✅ Completed

6. **Wreck IT 6.0 2025**

   - Kategori: General, Junior, Reverse Engineering, Web
   - Status: ✅ Completed
   - Multiple write-up PDF tersedia

7. **FIT 2025**

   - Status: ✅ Completed
   - Write-up PDF tersedia

8. **Cyberkarta 2025**

   - Status: ✅ Completed

9. **Permifest 2025**

   - Status: ✅ Completed

10. **Rise the Range 2025**

    - Status: ✅ Completed

11. **HackTheBoo 2025 (HTB)**

    - Kategori: Web
    - Status: ✅ Completed

12. **CBD Season 2 2025**
    - Status: ✅ Completed

## 🔐 Kategori Challenge

### Web Exploitation

- **Teknik yang digunakan:**

  - SQL Injection
  - XXE (XML External Entity)
  - Broken Access Control
  - HTTP Request Smuggling
  - Server-Side Template Injection (SSTI)
  - File Upload Vulnerabilities
  - Authentication Bypass
  - Cookie Manipulation
  - SSRF (Server-Side Request Forgery)

- **Tools & Scripts:**
  - Python requests library
  - Burp Suite
  - Custom exploit scripts

### Cryptography

- **Teknik yang digunakan:**

  - RSA attacks
  - Padding Oracle attacks
  - Custom encryption schemes
  - Hash collisions
  - Modular arithmetic

- **Tools & Scripts:**
  - Python (cryptography, pycryptodome)
  - SageMath
  - Custom decryption scripts

### Reverse Engineering

- **Teknik yang digunakan:**

  - Static analysis
  - Dynamic analysis
  - Decompilation
  - Binary patching
  - eBPF analysis

- **Tools:**
  - Ghidra
  - IDA Pro
  - GDB
  - Radare2

### Binary Exploitation (PWN)

- **Teknik yang digunakan:**

  - Buffer overflow
  - Format string vulnerabilities
  - ROP (Return-Oriented Programming)
  - Heap exploitation

- **Tools:**
  - pwntools
  - GDB with GEF/PEDA
  - ROPgadget

### Digital Forensics

- **Teknik yang digunakan:**

  - File carving
  - Memory analysis
  - Network traffic analysis
  - Browser forensics
  - Event log analysis (Windows EVTX)

- **Tools:**
  - Wireshark
  - Volatility
  - Autopsy
  - binwalk
  - steghide

### Blockchain

- **Teknik yang digunakan:**

  - Smart contract vulnerabilities
  - Reentrancy attacks
  - Access control issues

- **Tools:**
  - Solidity
  - Foundry
  - Hardhat

### Miscellaneous

- **Teknik yang digunakan:**
  - Python jail escapes
  - Sandbox bypass
  - Encoding/decoding challenges
  - Steganography

## 🛠️ Teknologi & Tools

### Programming Languages

- **Python** - Primary language untuk exploit scripts
- **JavaScript/Node.js** - Web exploitation dan automation
- **Solidity** - Smart contract analysis
- **C/C++** - Binary analysis dan exploitation
- **Java** - Reverse engineering Java applications

### Libraries & Frameworks

- `requests` - HTTP requests
- `pwntools` - Binary exploitation
- `cryptography` / `pycryptodome` - Cryptographic operations
- `flask` / `express` - Web application testing
- `pandas` / `numpy` - Data analysis untuk forensics

### Tools

- **Burp Suite** - Web application security testing
- **Ghidra** - Reverse engineering
- **Wireshark** - Network analysis
- **Volatility** - Memory forensics
- **GDB** - Debugging
- **Docker** - Containerized challenges

## 📖 Cara Menggunakan

### 1. Menjelajahi Challenge

Setiap kompetisi memiliki folder terpisah dengan struktur:

```
[Competition Name]/
├── [Category]/
│   ├── [Challenge Name]/
│   │   ├── exploit.py          # Exploit script
│   │   ├── solve.py            # Solusi
│   │   ├── README.md           # Dokumentasi challenge
│   │   └── [challenge files]   # File challenge
```

### 2. Menjalankan Exploit Scripts

Sebagian besar exploit script menggunakan Python 3:

```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan exploit
python exploit.py
```

**Catatan:** Beberapa script mungkin memerlukan konfigurasi khusus (IP address, port, session cookies, dll). Periksa komentar dalam script untuk detail lebih lanjut.

### 3. Membaca Write-up

Write-up tersedia dalam berbagai format:

- **Markdown (.md)** - Dokumentasi teknis
- **PDF (.pdf)** - Write-up lengkap dari tim
- **Text (.txt)** - Write-up sederhana

### 4. Contoh Penggunaan

#### Web Exploitation - XXE

```bash
cd Solver/
python xxe.py
```

#### HackTheBox - Broken Access Control

```bash
cd Solver/
node htb-bac.js
```

## ⚠️ Disclaimer

1. **Hanya untuk Tujuan Edukasi**

   - Repository ini dibuat untuk tujuan pembelajaran dan dokumentasi
   - Semua exploit dan teknik yang digunakan adalah dalam konteks CTF yang legal

2. **Etika Hacking**

   - Jangan gunakan teknik atau script dalam repository ini untuk aktivitas ilegal
   - Hanya gunakan pada sistem yang Anda miliki atau memiliki izin eksplisit

3. **Akurasi**

   - Script dan solusi mungkin tidak selalu bekerja di semua environment
   - Beberapa challenge mungkin memerlukan konfigurasi khusus

4. **Konten Challenge**

   - Source code challenge disertakan untuk referensi pembelajaran
   - Beberapa file mungkin berisi informasi sensitif (sudah di-redact jika perlu)

5. **Legal**
   - Penggunaan repository ini adalah tanggung jawab pengguna
   - Penulis tidak bertanggung jawab atas penyalahgunaan konten

## 📝 Catatan

- Repository ini terus diperbarui seiring dengan partisipasi dalam kompetisi CTF baru
- Beberapa challenge mungkin tidak memiliki write-up lengkap (masih dalam proses)
- Jika menemukan kesalahan atau ingin berkontribusi, silakan buat issue atau pull request

## 📦 File Besar & Google Drive

Beberapa file besar (melebihi 100MB) tidak dapat di-upload ke GitHub karena batas ukuran file. File-file tersebut disimpan di Google Drive dan dapat diakses melalui link berikut:

**[📁 Google Drive - CTF Write-ups & Files](https://drive.google.com/drive/folders/1pctX9gAdF1IcTxR52ZS0BY2LzB7SFS52?hl=id)**

### File Besar yang Disimpan di Google Drive:

- `Gemastik 2025/Forensic/Hacked/dump.zip` (137.38 MB)
- `Wreck IT 6.0 2025/Junior_LastSeenIn2026_Writeup.pdf` (111.58 MB)
- File-file besar lainnya (zip, 7z, rar, tar.xz, dll)

### Folder di Google Drive:

- **CBD Season 2 2025**
- **Compfest 2025**
- **FindIT 2025**
- **FIT Competition 2025**
- **Gemastik 2025**
- **NCS Aptikom 2025**
- **Permifest 2025**
- **Wreck IT 6.0 2025**
- Template write-up Soft Spoken

## 🔗 Link Berguna

- [CTFtime](https://ctftime.org/) - Kalender kompetisi CTF
- [HackTheBox](https://www.hackthebox.com/) - Platform latihan cybersecurity
- [TryHackMe](https://tryhackme.com/) - Platform pembelajaran cybersecurity
- [OWASP](https://owasp.org/) - Open Web Application Security Project

## 📊 Statistik

- **Total Kompetisi:** 12+
- **Kategori Challenge:** 7+
- **Total Challenge:** 100+
- **Bahasa Pemrograman:** Python, JavaScript, Solidity, C/C++, Java
- **File Besar:** Disimpan di [Google Drive](https://drive.google.com/drive/folders/1pctX9gAdF1IcTxR52ZS0BY2LzB7SFS52?hl=id)

## 👥 Kontribusi

Kontribusi dalam bentuk:

- Perbaikan dokumentasi
- Penambahan write-up
- Perbaikan exploit scripts
- Penambahan catatan dan tips

Sangat diterima dan dihargai!

---

**Happy Hacking! 🚀**

_Last Updated: 2025_
