import socket
import hashlib
import pickle

CHUNK_SIZE = 1024
HOST = 'localhost'
PORT = 5001

def calculate_checksum(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def send_file(file_path, sock):
    with open(file_path, 'rb') as f:
        data = f.read()
        sock.sendall(data + b"<END>")  # EOF marker

def receive_chunks(sock):
    total_chunks = pickle.loads(sock.recv(4096))
    checksum = pickle.loads(sock.recv(4096))
    received = {}

    while len(received) < total_chunks:
        packet = sock.recv(4096)
        if not packet:
            break
        seq, data = pickle.loads(packet)
        received[seq] = data

    return received, checksum

def main():
    file_to_send = 'data.txt'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("[Client] Connected to server.")

        # Upload file to server
        send_file(file_to_send, s)
        print("[Client] File sent to server.")

        # Receive file chunks
        chunks, server_checksum = receive_chunks(s)
        print(f"[Client] Received {len(chunks)} chunks from server.")
        print(f"[Client] Server Checksum: {server_checksum}")

        # Reassemble file
        assembled_data = b''.join(chunks[i] for i in sorted(chunks))
        with open('reconstructed_data.txt', 'wb') as f:
            f.write(assembled_data)

        # Verify checksum
        local_checksum = calculate_checksum(assembled_data)
        print(f"[Client] Local Checksum: {local_checksum}")

        if local_checksum == server_checksum:
            print("[Client] Transfer Successful. Checksums match.")
        else:
            print("[Client] Transfer Failed. Checksums do not match.")

if __name__ == "__main__":
    main()
