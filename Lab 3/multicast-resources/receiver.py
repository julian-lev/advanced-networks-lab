import socket
import struct
import argparse

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Multicast Receiver.')

    # Add arguments
    parser.add_argument('group', type=str, help='Multicast group address (e.g., 224.1.1.1)')
    parser.add_argument('port', type=int, help='The port number to listen on')

    # Parse the arguments
    args = parser.parse_args()
    multicast_group = args.group
    port = args.port

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set socket options to allow reusing the address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    # Tell the operating system to add this socket to the multicast group
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f'Listening on multicast group {multicast_group}, port {port}...')

    while True:
        # Receive messages and print them
        data, _ = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        print(data.decode('utf-8'))

if __name__ == '__main__':
    main()
