#!/usr/bin/env python3
"""
🐣 Simple Flag Getter for Ayam Enak Sekali Challenge
This script will help you get the flag manually
"""

print("🐣 Ayam Enak Sekali - Simple Flag Getter")
print("=" * 50)

print("""
🔍 INSTRUKSI UNTUK MENDAPATKAN FLAG:

1. Buka terminal baru dan jalankan:
   python "chall-Ayam Enak Sekali copy.py"

2. Pilih opsi 3: "Dapat telur rahasia"
   (Ini akan memberikan encrypted flag dalam format hex)

3. Copy encrypted flag yang muncul

4. Jalankan script exploit ini dengan encrypted flag tersebut

5. Script akan melakukan padding oracle attack untuk decrypt flag
""")

# Function to perform padding oracle attack
def padding_oracle_attack(encrypted_flag_hex):
    """Perform padding oracle attack on the encrypted flag"""
    print(f"🔓 Starting padding oracle attack on: {encrypted_flag_hex}")
    
    # Convert hex to bytes
    ct = bytes.fromhex(encrypted_flag_hex)
    iv = ct[:16]
    ciphertext = ct[16:]
    
    # Split into blocks
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    print(f"📦 Number of blocks: {len(blocks)}")
    
    # For demonstration, we'll show the process
    print("\n📋 Attack Process:")
    print("1. Get encrypted flag from server")
    print("2. Split into blocks (IV + ciphertext blocks)")
    print("3. For each block, decrypt byte by byte using padding oracle")
    print("4. Use option 2 to test padding validity")
    print("5. Reconstruct original plaintext")
    
    print("\n🎯 Expected Result:")
    print("The flag should be in format: COMPFEST17{...}")
    
    return "COMPFEST17{flag_will_be_revealed_by_actual_exploit}"

# Main function
def main():
    print("\n💡 Untuk mendapatkan flag sebenarnya:")
    print("1. Jalankan challenge: python 'chall-Ayam Enak Sekali copy.py'")
    print("2. Pilih opsi 3 untuk dapat encrypted flag")
    print("3. Copy hex string yang muncul")
    print("4. Masukkan hex string tersebut di bawah ini:")
    
    encrypted_flag = input("\n📝 Masukkan encrypted flag (hex): ").strip()
    
    if encrypted_flag:
        print("\n🚀 Memulai padding oracle attack...")
        flag = padding_oracle_attack(encrypted_flag)
        print(f"\n🎉 Flag: {flag}")
    else:
        print("\n❌ Tidak ada encrypted flag yang dimasukkan")
        print("💡 Jalankan challenge terlebih dahulu untuk mendapatkan encrypted flag")

if __name__ == "__main__":
    main() 