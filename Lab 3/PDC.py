import socket
import argparse

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Process some command line arguments.')

    # Add arguments
    parser.add_argument('server', type=str, help='The server address (IPv4 or hostname)')
    parser.add_argument('port', type=int, help='The port number')

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    server = args.server
    port = args.port
 
    # Create udp socket
    ipv4_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ipv6_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    # message
    message = "RESET:20".encode()


    total_num_request = 0
    for i in range(60):

        # boolean for the loop
        received = False
        num_requests = 0

        while received == False:

            num_requests += 1
            # try ipv4
            ipv4_sock.sendto(message, (server,port))
            ipv4_sock.settimeout(1)

            try:
                data, address = ipv4_sock.recvfrom(1024)
                print(data.decode())
                received = True
            except socket.timeout:
                pass

            # try ipv6
            ipv6_sock.sendto(message, (server,port))
            ipv6_sock.settimeout(1)

            try:
                data, address = ipv6_sock.recvfrom(1024)
                print(data.decode())
                received = True
            except socket.timeout:
                pass
        total_num_request += num_requests

    print(total_num_request/60)
    


if __name__ == '__main__':
    main()


