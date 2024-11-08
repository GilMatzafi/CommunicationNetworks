import socket

def run_client(server_ip ,server_port):
    server_address = (server_ip, server_port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        
        # Enter a domain
        
        question = input()

        client_socket.sendto(question.encode('utf-8'), server_address)
        response, _ = client_socket.recvfrom(1024)
        print(f"{response.decode('utf-8')}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python client.py [serverIP] [serverPort]")
        sys.exit(1)

    server_ip , server_port = sys.argv[1:]
    run_client(server_ip , int(server_port))
