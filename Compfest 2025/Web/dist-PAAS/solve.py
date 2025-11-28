import base64
import pickletools

# Decode the base64 string
payload = base64.urlsafe_b64decode(
    "gASVJAAAAAAAAACMAm50lIwGc3lzdGVtlJOUjAxjYXQgZmxhZy50eHSUhZRSlC4="
)

# Disassemble the pickle to see its operations
pickletools.dis(payload)
