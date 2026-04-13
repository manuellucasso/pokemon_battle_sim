import socket

def initiate_server():
    # 1. Create the connection tunnel (Socket)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Define the IP and Port. 
    # Using '0.0.0.0' means the server will listen on all available network interfaces.
    # Port 5050 is an arbitrary port number that is usually free.
    servidor.bind(('0.0.0.0', 5050))
    
    # 3. Start listening for incoming connections...
    servidor.listen()
    print("Server started! Waiting for player 2...")
    
    # 4. Accept the connection when the client (Vinicius) connects
    connection, address = servidor.accept()
    print(f"Opponent connected from IP: {address}")
    
    # 5. Conversation loop (Simulating a turn's input)
    while True:
        # Ask for your input via keyboard
        your_action = input("You: ")
        connection.send(your_action.encode('utf-8')) # Send it to the opponent
        
        # Wait for the opponent's response
        print("Waiting for the opponent's turn...")
        opponent_action = connection.recv(1024).decode('utf-8')
        print(f"Opponent: {opponent_action}")

if __name__ == "__main__":
    initiate_server()