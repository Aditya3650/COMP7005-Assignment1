import socket
import argparse

# Function to start the client
def start_client(socket_path, request_data):
    # Create a Unix Domain Socket
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        # Try to connect to the server
        client_socket.connect(socket_path)

        # Send the request
        client_socket.sendall(request_data.encode('utf-8'))
        print("Sent request:", request_data)

        # Receive the response
        response = client_socket.recv(1024)
        print("Received response:", response.decode('utf-8'))

    except FileNotFoundError:
        print(f"Error: The server socket at '{socket_path}' was not found. Make sure the server is running and the path is correct.")
    except ConnectionRefusedError:
        print(f"Error: Unable to connect to the server at '{socket_path}'. The server might not be accepting connections.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="UNIX Domain Socket Client")
    parser.add_argument("socket_path", help="Path for the UNIX socket")
    parser.add_argument("request_data", help="Request data to send to the server")
    args = parser.parse_args()

    start_client(args.socket_path, args.request_data)
