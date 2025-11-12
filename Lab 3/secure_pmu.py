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

    # port= 5003
    # path to certificate= /cert/output/certificate.crt
    # path to key= /343473_key.pem

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    port = args.port
    certificate = args.certificate
    key = args.key

    hostname = '127.0.0.1'

    # Create the ssl context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certificate, key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((hostname, port))
        sock.listen(5)

        while True:

            conn, addr = sock.accept()
            with context.wrap_socket(conn, server_side=True) as ssock:
                data = ssock.recv(11)
                if data.decode() == "CMD_short:0":
                    ssock.sendall("This is PMU data 0".encode())
                    ssock.sendall("This is PMU data 1".encode())
                    ssock.sendall("This is PMU data 2".encode())
                    ssock.sendall("This is PMU data 3".encode())
                    ssock.close()

                else:
                    ssock.close()
            

if __name__ == '__main__':
    main()


