import pandas as pd
from move import Move
import os
import time
import sys


def typewriter_print(text, delay=0.03):
    """Prints text one character at a time to simulate a classic RPG feel."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush() # Força o terminal a mostrar a letra imediatamente
        time.sleep(delay)
    print() # Pula para a próxima linha no final

def get_data_folder():
    base_path = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_path)
    data_dir = os.path.join(parent_dir, 'data')

    return base_path, parent_dir, data_dir

def load_game_data(data_dir):
    """
    Loads all CSV files into memory at startup.
    Returns a dictionary structured by Pokemon name.
    """
    # Load the base stats and names
    df_pokedex = pd.read_csv(os.path.join(data_dir, 'pokemon_base_stats.csv'))
    df_learnsets = pd.read_csv(os.path.join(data_dir, 'pokemon_learnsets.csv'))
    df_tm_hm = pd.read_csv(os.path.join(data_dir, 'pokemon_tm_hm.csv'))

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
    
    MOVES_LIBRARY = Move.get_all_moves(data_dir)

    return pokemon_data,MOVES_LIBRARY


# Getting the data set at global level
base_path, parent_dir, data_dir = get_data_folder()
GLOBAL_POKEMON_DATA, MOVES_LIBRARY = load_game_data(data_dir)