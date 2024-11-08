import socket

def load_mappings(file_path):
    # Load mappings from the specified file and return them as a dictionary
    mappings = {}
    with open(file_path, 'r') as file:
        for line in file:
            domain, ip = map(str.strip, line.split(','))
            mappings[domain] = ip
    return mappings

def save_mappings(file_path, mappings):
    # Save mappings to the specified file
    with open(file_path, 'w') as file:
        for domain, ip in mappings.items():
            file.write(f"{domain}, {ip}\n")

def handle_request(data, mappings, parent_socket,parent_address):
    # Process incoming requests from clients
    domain = data.decode('utf-8')
    if domain in mappings:
        # If the domain is in the local mappings, return the corresponding IP
        return mappings[domain].encode('utf-8')
    else:
        # If the domain is not in the local mappings, forward the request to the parent server
        parent_socket.sendto(data, parent_address)
        parent_response, _ = parent_socket.recvfrom(1024)
        ip = parent_response.decode('utf-8')
        # Update local mappings and save them to file
        mappings[domain] = ip
        save_mappings(ips_file, mappings)
        return ip.encode('utf-8')

def run_server(my_port, parent_ip, parent_port , ips_file):
    # Initialize variables
    mappings = load_mappings(ips_file)
        
    # Set up socket for communication with the parent server
    parent_address = (parent_ip, parent_port) 
    
    parent_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Set up socket for handling client requests
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', int(my_port)))
    
    #todo - delete later .
    
    # Print server information
    print(f"Server listening on port {my_port}")
    
    # Main server loop
    while True:
        data, client_address = server_socket.recvfrom(1024)
        response = handle_request(data, mappings, parent_socket,parent_address)
        server_socket.sendto(response, client_address)

if __name__ == "__main__":
    import sys
    
    # Check command-line arguments
    if len(sys.argv) != 5:
        print("Usage: python server.py [myPort] [parentIP] [parentPort] [ipsFileName]")
        sys.exit(1)

    # Extract command-line arguments
    my_port ,parent_ip , parent_port, ips_file = sys.argv[1:]
    
    # Run the server
    run_server(int(my_port), parent_ip , int(parent_port),ips_file)

