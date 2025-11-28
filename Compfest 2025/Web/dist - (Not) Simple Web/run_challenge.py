#!/usr/bin/env python3
"""
Local RSA Custom Parameter Challenge Runner
Untuk testing eksploitasi secara lokal
"""

import socket
import threading
import time
from Crypto.Util.number import getPrime, bytes_to_long
from random import randint
from math import gcd

# Flag yang akan di-encrypt
FLAG = b"COMPFEST{test_flag_here_12345}"

def generate_pub_key(bound):
    """Generate public key dengan bound yang diberikan"""
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

def handle_client(client_socket):
    """Handle client connection"""
    try:
        # Send initial message
        client_socket.send(b"Generating public key....\n")
        
        # Generate N
        N, e, d, p, q = generate_pub_key(2**1000)  # Default bound
        client_socket.send(f"N: {N}\n".encode())
        
        # Get bound from client
        data = client_socket.recv(1024).decode().strip()
        try:
            bound = int(data)
            if bound < 2**1000:
                client_socket.send(b"Get out of here!\n")
                return
        except:
            client_socket.send(b"Invalid bound!\n")
            return
        
        # Regenerate with new bound
        N, e, d, p, q = generate_pub_key(bound)
        
        client_socket.send(b"Done!\n")
        
        # Encrypt flag
        ct = encrypt(FLAG, N, e)
        
        # Send e and ct
        client_socket.send(f"e: {e}\n".encode())
        client_socket.send(f"ct: {ct}\n".encode())
        
        print(f"Generated with bound {bound}:")
        print(f"N = {N}")
        print(f"e = {e}")
        print(f"d = {d}")
        print(f"ct = {ct}")
        print(f"Flag = {FLAG}")
        
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server(host='localhost', port=1234):
    """Start the challenge server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    
    print(f"Challenge server started on {host}:{port}")
    print(f"Flag: {FLAG}")
    print("Waiting for connections...")
    
    try:
        while True:
            client, addr = server.accept()
            print(f"Client connected from {addr}")
            client_thread = threading.Thread(target=handle_client, args=(client,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer stopped")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
