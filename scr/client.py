from http import client
import socket
import sys
import time

def typewriter_print(text, delay=0.03):
    """Prints text one character at a time for the RPG feel on the client side."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print() # New line at the end


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Server IP: Replace with the Host's IP (ZeroTier/Hamachi) when playing online
    # Use '127.0.0.1' for local testing
    server_ip = '127.0.0.1' 
    port = 5050
    
    try:
        client.connect((server_ip, port))
        typewriter_print("Successfully connected to Manuel's battle arena!\n")
        
        # Main listening loop
        while True:
            # 1. Wait for incoming data
            data = client.recv(4096).decode('utf-8')
            
            if not data:
                break
                
            # 2. Split the data by our separator and filter out empty strings
            messages = data.strip().split('\n')
            
            for msg in messages:
                # Process each individual message in the bundle
                if msg.startswith("PRINT|"):
                    actual_text = msg.split("PRINT|", 1)[1]
                    typewriter_print(actual_text)
                    
                elif msg.startswith("ACTION|"):
                    action_type = msg.split("ACTION|", 1)[1]
                    
                    if action_type == "CHOOSE_ACTION":
                        # Lembra que combinamos de deixar vazio? ;)
                        choice = input("Select (1-3):") 
                        client.send(choice.encode('utf-8'))
                        
                    elif action_type == "CHOOSE_MOVE":
                        move_choice = input()
                        client.send(move_choice.encode('utf-8'))
                        
                    elif action_type == "CHOOSE_POKEMON":
                        poke_choice = input()
                        client.send(poke_choice.encode('utf-8'))
                    
    except ConnectionRefusedError:
        typewriter_print("Could not find the server. Has the Host already started the match?")
    except KeyboardInterrupt:
        typewriter_print("\nExiting the game...")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()