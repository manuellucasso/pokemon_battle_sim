from pokemon import Pokemon
from move import Move
from move_manager import MoveManager
from data_loader import load_game_data, get_data_folder
from test_suite import test_suite







def main():
    """
    Main entry point for the Pokemon Battle Simulator.
    Handles data initialization and test cases.
    """
    print("--- Initializing Pokemon Battle Simulator ---") 

    # 1. Load the Global Moves Library (Pre-loading logic)
    # This ensures we only read the large CSV file once at startup
    base_path, parent_dir, data_dir = get_data_folder()
    GLOBAL_POKEMON_DATA, GLOBAL_MOVES_LIBRARY = load_game_data(data_dir)
     

    print("\n--- Game Data Loaded ---")

    test_suite(GLOBAL_POKEMON_DATA, GLOBAL_MOVES_LIBRARY)   

if __name__ == "__main__":
    main()
    