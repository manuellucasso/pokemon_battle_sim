from pokemon import Pokemon
from move import Move
import pandas as pd

def load_game_data():
    """
    Loads all CSV files into memory at startup.
    Returns a dictionary structured by Pokemon name.
    """
    # Load the base stats and names
    df_pokedex = pd.read_csv('pokemon_base_stats.csv')
    df_learnsets = pd.read_csv('pokemon_learnsets.csv')
    df_tm_hm = pd.read_csv('pokemon_tm_hm.csv')

    pokemon_data = {}

    for name in df_pokedex['Name']:
        # Filter moves for this specific pokemon
        lvl_moves = df_learnsets[df_learnsets['pokemon'] == name][['level', 'move_name']].to_dict('records')
        tm_moves = df_tm_hm[df_tm_hm['pokemon'] == name]['move_name'].tolist()
        base_stats = df_pokedex[df_pokedex['Name'] == name].iloc[0].to_dict()

        pokemon_data[name] = {
            'lvl_up': lvl_moves,
            'teach': tm_moves,
            'base_stats': base_stats
        }
    
    moves_library = Move.get_all_moves()

    return pokemon_data,moves_library





def main():
    """
    Main entry point for the Pokemon Battle Simulator.
    Handles data initialization and test cases.
    """
    print("--- Initializing Pokemon Battle Simulator ---") 

    # 1. Load the Global Moves Library (Pre-loading logic)
    # This ensures we only read the large CSV file once at startup
    GLOBAL_POKEMON_DATA, GLOBAL_MOVES_LIBRARY = load_game_data()
     

    print("\n--- Game Data Loaded ---")

    print("\n--- Sample Pokemon Creation ---")
    # Create a sample Pokemon instance (e.g., Pikachu at level 5)
    pikachu=Pokemon(POKEMON_DATA=GLOBAL_POKEMON_DATA['Pikachu'], level=5, moves=None, status_conditions=None)   
    print(f"Created Pokemon: {pikachu.name}, Level: {pikachu.level}, HP: {pikachu.hp_current}/{pikachu.hp_max}")



if __name__ == "__main__":
    main()    