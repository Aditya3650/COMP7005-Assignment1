import os
import socket
import argparse

# Function to start the server
def start_server(socket_path):
    # Ensure the socket doesn't already exist
    if os.path.exists(socket_path):
        os.remove(socket_path)

    # Create a Unix Domain Socket
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        # Bind the socket to the path
        server_socket.bind(socket_path)

        # Listen for incoming connections
        server_socket.listen(1)
        print("Server is listening for connections...")

        while True:
            # Accept a connection
            connection, _ = server_socket.accept()
            try:
                print(f"Connection received from client")

                # Receive the request
                data = connection.recv(1024)
                if data:
                    request = data.decode('utf-8')
                    print("Received request:", request)

                    # Process the request
                    if request.startswith("READ "):
                        file_name = request[5:]  # Extract the file name
                        try:
                            with open(file_name, 'r') as file:
                                content = file.read()
                            response = content
                        except Exception as e:
                            response = f"Error reading file: {str(e)}"

                    elif request.startswith("WRITE "):
                        parts = request.split(" ", 2)
                        if len(parts) < 3:
                            response = "Invalid request format. Use: WRITE filename content"
                        else:
                            file_name = parts[1]
                            content = parts[2]
                            try:
                                with open(file_name, 'w') as file:
                                    file.write(content)
                                response = f"Wrote to {file_name} successfully."
                            except Exception as e:
                                response = f"Error writing to file: {str(e)}"

                    else:
                        response = "Invalid command. Use READ or WRITE."

                    # Send back the response
                    connection.sendall(response.encode('utf-8'))

            finally:
                # Close the connection
                connection.close()

    finally:
        # Clean up the server socket
        server_socket.close()
        os.remove(socket_path)

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="UNIX Domain Socket Server")
    parser.add_argument("socket_path", help="Path for the UNIX socket")
    args = parser.parse_args()

    start_server(args.socket_path)
