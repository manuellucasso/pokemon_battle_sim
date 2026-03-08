import pandas as pd
import requests
from io import StringIO

def save_pokedex_to_csv(filename='pokemon_base_stats.csv'):
    """
    Scrapes the Pokedex for the original 151 Pokemon and saves it to a CSV file.
    """
    url = "https://pokemondb.net/pokedex/all"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        r = requests.get(url, headers=header)
        # O Pandas lê todas as tabelas da página HTML
        tables = pd.read_html(StringIO(r.text))
        df = tables[0]
        
        # Filtra apenas a primeira geração (número <= 151)
        kanto_df = df[df['#'] <= 151].copy()
        
        # Remove duplicatas (como Mega Evoluções) para manter apenas as formas base
        kanto_df = kanto_df.drop_duplicates(subset=['#'], keep='first')
        
        # Renomeia as colunas para facilitar o uso no seu stats_calculator
        kanto_df.columns = ['ID', 'Name', 'Type', 'Total', 'HP', 'Attack', 'Defense', 'SpAtk', 'SpDef', 'Speed']
        
        # Salva o arquivo CSV
        kanto_df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Successfully saved {len(kanto_df)} Pokemon to {filename}!")
        
    except Exception as e:
        print(f"Error: {e}")




import pandas as pd
import requests
from io import StringIO
import time

def generate_full_learnset_csv(pokemon_list):
    """
    Scrapes Level-Up moves and TM/HM compatibility for each Pokemon in the list.
    Saves the data into 'pokemon_learnsets.csv' and 'pokemon_tm_hm.csv'.
    """
    all_lvl_data = []
    all_tm_data = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for name in pokemon_list:
        print(f"Fetching data for: {name}...")
        # URLs on PokemonDB are typically lowercase
        url = f"https://pokemondb.net/pokedex/{name.lower()}"
        
        try:
            response = requests.get(url, headers=headers)
            # Read all tables from the HTML content
            tables = pd.read_html(StringIO(response.text))
            
            found_lvl = False
            found_tm = False

            for df in tables:
                # 1. Identify Level-Up table (looks for 'Lv.' column)
                if 'Lv.' in df.columns and not found_lvl:
                    lvl_df = df[['Lv.', 'Move']].copy()
                    lvl_df['pokemon'] = name.capitalize()
                    lvl_df.rename(columns={'Lv.': 'level', 'Move': 'move_name'}, inplace=True)
                    # Standardize level 1 moves (represented as '—' on the site)
                    lvl_df['level'] = lvl_df['level'].replace('—', '1')
                    all_lvl_data.append(lvl_df)
                    found_lvl = True
                
                # 2. Identify TM/HM table (looks for 'TM' or 'Machine' column)
                elif ('TM' in df.columns or 'Machine' in df.columns) and not found_tm:
                    # Get the name of the first column (could be 'TM' or 'Machine')
                    tm_col_name = df.columns[0]
                    tm_df = df[[tm_col_name, 'Move']].copy()
                    tm_df['pokemon'] = name.capitalize()
                    tm_df.rename(columns={tm_col_name: 'tm_number', 'Move': 'move_name'}, inplace=True)
                    all_tm_data.append(tm_df)
                    found_tm = True
                
                # Exit table loop early if both are found to save processing time
                if found_lvl and found_tm:
                    break
            
            # Ethical delay to prevent server strain
            time.sleep(1)
            
        except Exception as e:
            print(f"Error processing {name}: {e}")

    # Consolidate and save Level-Up data
    if all_lvl_data:
        lvl_final_df = pd.concat(all_lvl_data, ignore_index=True)
        lvl_final_df = lvl_final_df[['pokemon', 'level', 'move_name']]
        lvl_final_df.to_csv('pokemon_learnsets.csv', index=False)
        print("Successfully generated 'pokemon_learnsets.csv'.")

    # Consolidate and save TM/HM data
    if all_tm_data:
        tm_final_df = pd.concat(all_tm_data, ignore_index=True)
        tm_final_df = tm_final_df[['pokemon', 'tm_number', 'move_name']]
        tm_final_df.to_csv('pokemon_tm_hm.csv', index=False)
        print("Successfully generated 'pokemon_tm_hm.csv'.")



if __name__ == "__main__":
    save_pokedex_to_csv()
    df_pokedex = pd.read_csv('pokemon_base_stats.csv')
    pokemon_names = df_pokedex['Name'].tolist()
    generate_full_learnset_csv(pokemon_list=pokemon_names)
    print("\n--- Setup Complete! All CSV data is ready for the simulator ---")