class Trainer:
    def __init__(self, name, is_ai=False):
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
        self.is_ai = is_ai

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
            print(f"{self.name}'s party is already full!")

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
        print(f"\n--- {self.name}'s Party ---")
        for i, p in enumerate(self.pokemons):
            status = f"{p.hp_current}/{p.hp_max} HP - (ACTIVE)" if i == self.active_pokemon_index else f"{p.hp_current}/{p.hp_max} HP"
            fainted_note = " (FAINTED)" if p.hp_current <= 0 else ""
            print(f"[{i+1}] {p.name} - {status}{fainted_note}")

        try:
            choice = int(input(f"\nSelect a Pokemon to send out (1-{len(self.pokemons)}): "))-1
            
            if 0 <= choice < len(self.pokemons) and not self.pokemons[choice].is_blocked_switch:
                if choice == self.active_pokemon_index:
                    print(f"{self.pokemons[choice].name} is already in battle!")
                elif self.pokemons[choice].hp_current > 0:
                    self.active_pokemon_index = choice
                    print(f"Go! {self.pokemons[choice].name}!")
                else:
                    print(f"{self.pokemons[choice].name} has no energy left to fight or can't be switched!")
            else:
                print("Invalid choice. Try again.")
                self.switch_pokemon()
        
        except ValueError:
            print("Invalid input. Please enter a number.")

    def choose_move(self):
        """
        Handles move selection logic. 
        
        """
        pokemon = self.get_active_pokemon()
        available_moves = pokemon.move_manager.active_moves 
        
        for i, move in enumerate(available_moves):
            print(f"[{i+1}] {move} (PP: {pokemon.move_manager.current_pp[move]})")
            
        try:
            choice = int(input("Select a move index: "))-1
            if 0 <= choice < len(available_moves):
                return available_moves[choice]
            else:
                print("Invalid selection. Defaulting to first move.")
                return available_moves[0]
        except ValueError:
            print("Invalid input. Defaulting to first move.")
            return available_moves[0]

    def use_item(self):
        """
        Placeholder for item usage logic (Potions, TMs, etc.).
        To be implemented in future versions.
        """
        pass