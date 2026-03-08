from pokemon import Pokemon
from move import Move

def main():
    """
    Main entry point for the Pokemon Battle Simulator.
    Handles data initialization and test cases.
    """
    print("--- Initializing Pokemon Battle Simulator ---") 

    # 1. Load the Global Moves Library (Pre-loading logic)
    # This ensures we only read the large CSV file once at startup
    moves_library = Move.get_all_moves('moves_database.csv') 

    print("\n--- Creating Test Pokemon ---")   




if __name__ == "__main__":
    main()    