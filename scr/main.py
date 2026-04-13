from pokemon import Pokemon
import socket
from trainer import Trainer
from battle import Battle
from move import Move
from move_manager import MoveManager
from data_loader import load_game_data, get_data_folder,typewriter_print
from test_suite import test_suite
from data_loader import set_network_connection







def start_game():
    """
    Main entry point for the Pokemon Battle Simulator.
    Handles data initialization and test cases.
    """
    typewriter_print("--- Initializing Pokemon Battle Simulator ---") 

    # 1. Load the Global Moves Library (Pre-loading logic)
    # This ensures we only read the large CSV file once at startup
    base_path, parent_dir, data_dir = get_data_folder()
    
    # Make sure GLOBAL_POKEMON_DATA is properly populated here so your 
    # Trainer's create_team method can access the loaded data!
    GLOBAL_POKEMON_DATA, GLOBAL_MOVES_LIBRARY = load_game_data(data_dir)
     
    typewriter_print("\n--- Game Data Loaded ---")

    # 2. Create the socket connection (Server)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # '0.0.0.0' allows connections from the local PC and the network.
    # Port 5050 is the door we are leaving open.
    server.bind(('0.0.0.0', 5050))
    server.listen()
    
    print("Waiting for Vinicius (or the test client) to connect...")
    # The game freezes here until you run client.py in the other terminal
    connection, address = server.accept()
    print(f"Player connected from {address}!")
    
    # 3. Turn on the network printing system globally
    set_network_connection(connection)
    
    # 4. Create the trainers using the new architecture
    
    # Manuel is local (uses keyboard)
    t1 = Trainer(name="Manuel", is_local=True)
    # Building the team using your new method!
    t1.create_team(["Squirtle", "Geodude", "Pidgey"], level=10)
    
    # Vinicius is remote (uses the network client)
    t2 = Trainer(name="Vinicius", is_local=False)
    t2.create_team(["Charmander", "Pikachu", "Weedle"], level=10)
    
    # PLUG THE CONNECTION INTO HIS TRAINER CLASS!
    t2.network_connection = connection
    
    # 5. Start the battle
    print("\nStarting the battle engine...")
    battle = Battle(t1, t2, connection)
    
    # Assuming your main loop method in Battle is called 'start' or 'run_battle'
    # battle.run_battle()  <-- Use whichever method name actually starts the turns
    battle.start()
     #test_suite(GLOBAL_POKEMON_DATA, GLOBAL_MOVES_LIBRARY)  

    

if __name__ == "__main__":
    start_game()
    