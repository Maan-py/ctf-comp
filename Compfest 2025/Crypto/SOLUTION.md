# 🐣 Ayam Enak Sekali - Padding Oracle Attack Solution

## 🔍 Challenge Analysis

This is a **Padding Oracle Attack** challenge on AES-CBC encryption. The vulnerability lies in the server's error handling when decrypting ciphertexts with invalid padding.

### Key Vulnerabilities:

1. **Padding Oracle**: Option 2 reveals whether padding is valid or invalid
2. **Error Information Leakage**: "Oops mesin pemecah telur rusak" indicates invalid padding
3. **AES-CBC Mode**: Allows block manipulation for the attack

## 🚀 Exploit Strategy

### Step 1: Get Encrypted Flag

- Use option 3 to get the encrypted flag in hex format
- This gives us the IV + ciphertext blocks

### Step 2: Padding Oracle Attack

For each ciphertext block (except IV):

1. Decrypt byte by byte from end to start (position 15 to 0)
2. For each byte position, try all 256 possible values
3. Use option 2 to test if padding is valid
4. When valid padding is found, we've found the correct byte

### Step 3: Algorithm Details

```
For each block C[i] with previous block C[i-1]:
  For each byte position j (15 to 0):
    padding_len = 16 - j
    For each guess g (0 to 255):
      modified_prev[j] = g ⊕ padding_len
      Set known padding bytes in modified_prev
      test_ct = modified_prev + C[i]
      if oracle_says_valid_padding(test_ct):
        decrypted_byte = g
        break
```

## 📋 Complete Exploit Code

```python
import subprocess
import sys
import time
import re

class PaddingOracleExploit:
    def __init__(self, script_path):
        self.script_path = script_path
        self.process = None

    def start_server(self):
        self.process = subprocess.Popen(
            [sys.executable, self.script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        time.sleep(1)

    def read_until_prompt(self):
        output = ""
        while True:
            char = self.process.stdout.read(1)
            if char == '>':
                break
            output += char
        return output

    def send_command(self, command):
        self.process.stdin.write(command + '\n')
        self.process.stdin.flush()
        time.sleep(0.1)

    def get_encrypted_flag(self):
        self.send_command("3")
        self.read_until_prompt()
        response = self.process.stdout.readline().strip()
        return response

    def test_padding_oracle(self, ct_hex):
        self.send_command("2")
        self.read_until_prompt()
        self.send_command(ct_hex)
        response = self.read_until_prompt()
        return "Oops mesin pemecah telur rusak" not in response

    def decrypt_block(self, target_block, prev_block):
        decrypted = b''

        for byte_pos in range(15, -1, -1):
            padding_len = 16 - byte_pos

            modified_prev = bytearray(prev_block)
            for i in range(byte_pos + 1, 16):
                modified_prev[i] = decrypted[15 - i] ^ padding_len

            for guess in range(256):
                modified_prev[byte_pos] = guess ^ padding_len

                test_ct = bytes(modified_prev) + target_block
                test_ct_hex = test_ct.hex()

                if self.test_padding_oracle(test_ct_hex):
                    decrypted = bytes([guess]) + decrypted
                    break

        return decrypted

    def decrypt_flag(self):
        encrypted_flag_hex = self.get_encrypted_flag()
        ct = bytes.fromhex(encrypted_flag_hex)
        iv = ct[:16]
        ciphertext = ct[16:]

        blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]

        decrypted = b''
        for i, block in enumerate(blocks):
            prev_block = blocks[i-1] if i > 0 else iv
            decrypted_block = self.decrypt_block(block, prev_block)
            decrypted += decrypted_block

        return decrypted

    def close(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

# Main exploit
if __name__ == "__main__":
    exploit = PaddingOracleExploit("chall-Ayam Enak Sekali copy.py")

    try:
        exploit.start_server()
        flag = exploit.decrypt_flag()
        print(f"Flag: {flag.decode()}")
    finally:
        exploit.close()
```

## 🎯 Key Insights

1. **Padding Oracle**: The server reveals padding validity through error messages
2. **Block-by-Block**: We decrypt each 16-byte block independently
3. **Byte-by-Byte**: Within each block, we decrypt from end to start
4. **XOR Manipulation**: We modify the previous block to control padding
5. **No Key Required**: We can decrypt without knowing the encryption key

## 💡 Attack Complexity

- **Queries per byte**: Up to 256
- **Bytes per block**: 16
- **Total queries**: ~256 × 16 × number_of_blocks
- **Time complexity**: O(n) where n is the number of ciphertext bytes

## 🎉 Expected Result

The flag should be in the format: `COMPFEST17{...}`

The actual flag will be revealed by running the complete padding oracle attack against the challenge server.

## 🔧 Requirements

- Python with subprocess support
- Proper handling of server I/O
- Hex encoding/decoding utilities
- XOR operations for block manipulation

## 🚨 Important Notes

1. The attack requires many queries to the server
2. Handle server responses carefully
3. Be patient - the attack takes time
4. Test with known plaintexts first
5. Handle edge cases properly
