from data_loader import typewriter_print, GLOBAL_POKEMON_DATA
from pokemon import Pokemon
class Trainer:
    def __init__(self, name, is_local=True):
        """
        Initializes a Trainer instance.
        
        Args:
            name (str): The trainer's name.
            is_ai (bool): Flag to distinguish between human player and AI.
        """
        self.name = name
        self.pokemons = []  # List to store up to 6 Pokemon instances
        self.active_pokemon_index = 0  # Tracks which Pokemon is currently in battle
        self.inventory = {}  # Stores items, e.g., {"Potion": 5}
        self.is_local = is_local
        self.network_connection = None

         # State Flags for battle
        self.can_act= True

    def add_pokemon(self, pokemon_instance):
        """
        Adds a pre-instantiated Pokemon to the trainer's party.
        Limits the party size to 6.
        """
        if len(self.pokemons) < 6:
            self.pokemons.append(pokemon_instance)
        else:
            typewriter_print(f"{self.name}'s party is already full!",is_me=self.is_local, broadcast=False)

    def create_team(self, pokemon_names, level):
        """
        Builds a full team from a list of names and assigns the same level to all of them.
        """
        for name in pokemon_names:
            try:
                # Creates the Pokemon object using the global data
                new_pokemon = Pokemon(
                    POKEMON_DATA=GLOBAL_POKEMON_DATA[name], 
                    level=level, 
                    status_conditions=None
                )
                # Uses the class's own method to add it to the team safely
                self.add_pokemon(new_pokemon)
                
            except KeyError:
                print(f"Error: {name} was not found in the database!")           

    def get_active_pokemon(self):
        """
        Returns the Pokemon instance currently active in battle.
        """
        if self.pokemons:
            return self.pokemons[self.active_pokemon_index]
        return None

    def switch_pokemon(self):
        """
        Displays all Pokemon in the party and allows the trainer to choose a new active one.
        Ensures the selected Pokemon is conscious (HP > 0).
        """
        typewriter_print(f"\n--- {self.name}'s Party ---",is_me=self.is_local, broadcast=False)
        for i, p in enumerate(self.pokemons):
            status = f"{p.hp_current}/{p.hp_max} HP - (ACTIVE)" if i == self.active_pokemon_index else f"{p.hp_current}/{p.hp_max} HP"
            fainted_note = " (FAINTED)" if p.hp_current <= 0 else ""
            typewriter_print(f"[{i+1}] {p.name} - {status}{fainted_note}",is_me=self.is_local, broadcast=False)

        try:
            typewriter_print(f"\nSelect a Pokemon to send out (1-{len(self.pokemons)}): ",is_me=self.is_local, broadcast=False)

            # --- THE NETWORK CROSSROADS ---
            if not self.is_local and self.network_connection:
                # Send the tag to unlock the client's keyboard
                self.network_connection.send("ACTION|CHOOSE_POKEMON".encode('utf-8'))
                # Wait for the client's response
                choice_str = self.network_connection.recv(1024).decode('utf-8')
            else:
                # Use local keyboard (empty input since the prompt is printed above)
                choice_str = input()
                
            choice = int(choice_str) - 1            

            if 0 <= choice < len(self.pokemons) and not self.pokemons[choice].is_blocked_switch:
                if choice == self.active_pokemon_index:
                    typewriter_print(f"{self.pokemons[choice].name} is already in battle!",is_me=self.is_local, broadcast=False)
                elif self.pokemons[choice].hp_current > 0:
                    self.active_pokemon_index = choice
                else:
                    typewriter_print(f"{self.pokemons[choice].name} has no energy left to fight or can't be switched!",is_me=self.is_local, broadcast=False )
            else:
                typewriter_print("Invalid choice. Try again.",is_me=self.is_local, broadcast=False)
                self.switch_pokemon()
        
        except ValueError:
            typewriter_print("Invalid input. Please enter a number.",is_me=self.is_local, broadcast=False)

    def choose_move(self):
        """
        Handles move selection logic. 
        
        """
        pokemon = self.get_active_pokemon()
        available_moves = pokemon.move_manager.active_moves 
        
        for i, move in enumerate(available_moves):
            typewriter_print(f"[{i+1}] {move} (PP: {pokemon.move_manager.current_pp[move]})",is_me=self.is_local, broadcast=False)
            
        typewriter_print("Select a move index: ",is_me=self.is_local, broadcast=False)
        
        try: 
            # --- THE NETWORK CROSSROADS ---
            if not self.is_local and self.network_connection:
                # Send the tag to unlock the client's keyboard
                self.network_connection.send("ACTION|CHOOSE_MOVE".encode('utf-8'))
                # Wait for the client's response
                choice_str = self.network_connection.recv(1024).decode('utf-8')
            else:
                # Use local keyboard (empty input)
                choice_str = input()
                
            choice = int(choice_str) - 1

            if 0 <= choice < len(available_moves):
                return available_moves[choice]
            else:
                typewriter_print("Invalid selection. Defaulting to first move.",is_me=self.is_local, broadcast=False)
                return available_moves[0]
        except ValueError:
            typewriter_print("Invalid input. Defaulting to first move.",is_me=self.is_local, broadcast=False)
            return available_moves[0]

    def use_item(self):
        """
        Placeholder for item usage logic (Potions, TMs, etc.).
        To be implemented in future versions.
        """
        pass