import socket
import hashlib
import os
import random
import time
import pickle

CHUNK_SIZE = 1024
HOST = 'localhost'
PORT = 5001

def calculate_checksum(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

def split_file(file_path):
    chunks = []
    with open(file_path, 'rb') as f:
        seq = 0
        while chunk := f.read(CHUNK_SIZE):
            chunks.append((seq, chunk))
            seq += 1
    return chunks

def simulate_out_of_order(chunks):
    random.shuffle(chunks)
    return chunks

def send_chunks(client_socket, chunks, checksum):
    client_socket.send(pickle.dumps(len(chunks)))  # number of chunks
    time.sleep(0.1)
    client_socket.send(pickle.dumps(checksum))     # checksum
    time.sleep(0.1)

    for seq, data in chunks:
        packet = pickle.dumps((seq, data))
        client_socket.send(packet)
        time.sleep(0.01)  # simulate network delay

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[Server] Listening on {HOST}:{PORT}...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"[Server] Connected by {addr}")

            # Receive file from client
            file_data = b""
            while True:
                part = conn.recv(4096)
                if part.endswith(b"<END>"):
                    file_data += part[:-5]
                    break
                file_data += part

            file_path = 'received_input.txt'
            with open(file_path, 'wb') as f:
                f.write(file_data)

            # Split and checksum
            chunks = split_file(file_path)
            checksum = calculate_checksum(file_path)
            print(f"[Server] File received and split into {len(chunks)} chunks.")
            print(f"[Server] Checksum: {checksum}")

            # Simulate out-of-order transmission
            out_of_order_chunks = simulate_out_of_order(chunks)
            send_chunks(conn, out_of_order_chunks, checksum)
            print("[Server] Chunks sent.")

if __name__ == "__main__":
    main()
