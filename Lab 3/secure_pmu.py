import socket
import argparse
import ssl

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Process some command line arguments.')

    # Add arguments
    parser.add_argument('port', type=int, help='The port number')
    parser.add_argument('certificate', type=str, help='The path to cert')
    parser.add_argument('key', type=str, help='The path to key')

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    port = args.port
    certificate = args.certificate
    key = args.key

    hostname = '127.0.0.1'

    # Create the SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certificate, keyfile=key)

    # Create and bind the socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((hostname, port))
        sock.listen(5)

        print(f'Server listening on {hostname}:{port}...')

        while True:
            try:
                # Accept a connection
                conn, addr = sock.accept()
                print(f'Connection from {addr} has been established.')

                # Wrap the accepted socket with SSL
                with context.wrap_socket(conn, server_side=True) as ssock:
                    data = ssock.recv(1024)  # Increased buffer size to 1024 bytes
                    if data.decode() == "CMD_short:0":
                        # Send response messages
                        for i in range(4):  # Sending 4 messages
                            ssock.sendall(f"This is PMU data {i}".encode())
                    else:
                        print(f'Unknown command received: {data.decode()}')
            except Exception as e:
                print(f'Error occurred: {e}')
            finally:
                conn.close()  # Ensure the connection is closed

if __name__ == '__main__':
    main()
