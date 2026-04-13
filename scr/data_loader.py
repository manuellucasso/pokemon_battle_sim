import pandas as pd
from move import Move
import os
import time
import sys


# Global variable to hold the network socket
# It starts as None so the game works perfectly offline
NETWORK_CONNECTION = None

def set_network_connection(connection):
    """
    Allows the main battle engine to plug the network socket in here.
    """
    global NETWORK_CONNECTION
    NETWORK_CONNECTION = connection

def typewriter_print(text, delay=0.03,is_me=True, broadcast=True):
    """
    Prints text with a typewriter effect based on visibility flags.
    
    - broadcast=True: Shows on both Screen 1 and Screen 2.
    - broadcast=False & is_me=True: Shows ONLY on Screen 1 (Host).
    - broadcast=False & is_me=False: Shows ONLY on Screen 2 (Client).
    """
    # Logic based on your rules:
    show_local = broadcast or (not broadcast and is_me)
    show_remote = broadcast or (not broadcast and not is_me)

    # --- Screen 1 (Local/Host) ---
    if show_local:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    # --- Screen 2 (Remote/Client) ---
    global NETWORK_CONNECTION
    if NETWORK_CONNECTION and show_remote:
        try:
            message = f"PRINT|{text}\n"
            NETWORK_CONNECTION.send(message.encode('utf-8'))
            time.sleep(0.05) 
        except Exception:
            pass

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