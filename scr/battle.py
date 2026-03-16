import random
from data_loader import MOVES_LIBRARY, typewriter_print

# Type Effectiveness Chart
TYPE_CHART = {
    "Normal": {"Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
    "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0},
    "Water": {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0, "Rock": 2.0, "Dragon": 0.5},
    "Electric": {"Water": 2.0, "Grass": 0.5, "Electric": 0.5, "Ground": 0.0, "Flying": 2.0, "Dragon": 0.5},
    "Grass": {"Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5, "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0, "Dragon": 0.5, "Steel": 0.5},
    "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 0.5, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Steel": 0.5},
    "Fighting": {"Normal": 2.0, "Ice": 2.0, "Rock": 2.0, "Dark": 2.0, "Steel": 2.0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Ghost": 0.0, "Fairy": 0.5},
    "Poison": {"Grass": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0.0, "Fairy": 2.0},
    "Ground": {"Fire": 2.0, "Electric": 2.0, "Grass": 0.5, "Poison": 2.0, "Flying": 0.0, "Bug": 0.5, "Rock": 2.0, "Steel": 2.0},
    "Flying": {"Electric": 0.5, "Grass": 2.0, "Fighting": 2.0, "Bug": 2.0, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Dark": 0.0, "Steel": 0.5},
    "Bug": {"Fire": 0.5, "Grass": 2.0, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2.0, "Ghost": 0.5, "Dark": 2.0, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2.0, "Ice": 2.0, "Fighting": 0.5, "Ground": 0.5, "Flying": 2.0, "Bug": 2.0, "Steel": 0.5},
    "Ghost": {"Normal": 0.0, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5},
    "Dragon": {"Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0},
    "Dark": {"Fighting": 0.5, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2.0, "Rock": 2.0, "Steel": 0.5, "Fairy": 2.0},
    "Fairy": {"Fire": 0.5, "Fighting": 2.0, "Poison": 0.5, "Dragon": 2.0, "Dark": 2.0, "Steel": 0.5}
}

class Battle:
    def __init__(self, trainer1, trainer2):
        """
        Initializes a battle between two trainers.
        """
        self.t1 = trainer1
        self.t2 = trainer2
        self.turn_count = 1
        self.battle_log = [] # Useful for syncing future online matches

    def start(self):
        """
        Main battle loop that runs until one trainer has no usable Pokemon.
        """
        typewriter_print(f"\n--- Battle Started: {self.t1.name} vs {self.t2.name} ---")
        
        while self.check_battle_status():
            typewriter_print(f"\n=== Turn {self.turn_count} ===")
            self.run_turn()
            self.turn_count += 1

    def check_battle_status(self):
        """
        Checks if both trainers still have at least one conscious Pokemon.
        Returns False if a trainer is defeated.
        """
        t1_can_fight = any(p.hp_current > 0 for p in self.t1.pokemons)
        t2_can_fight = any(p.hp_current > 0 for p in self.t2.pokemons)
        
        if not t1_can_fight:
            typewriter_print(f"\n{self.t1.name} is out of usable Pokemon! {self.t2.name} wins!")
            return False
        if not t2_can_fight:
            typewriter_print(f"\n{self.t2.name} is out of usable Pokemon! {self.t1.name} wins!")
            return False
        return True

    def handle_faint(self, trainer):
        """
        Forces the trainer to switch to a healthy Pokemon if available.
        Returns True if the trainer can continue, False if defeated.
        """
        # Check for remaining conscious Pokemon in team
        can_continue = any(p.hp_current > 0 for p in trainer.pokemons)
        
        if can_continue:
            typewriter_print(f"{trainer.name} must choose a new Pokemon!")
            trainer.switch_pokemon()
            return True
        else:
            typewriter_print(f"{trainer.name} has no more Pokemon left to fight!")
            return False
    
    def run_turn(self):
        """
        Orchestrates the sequence of actions in a single turn.
        Prioritizes Switching/Items before processing Speed-based attacks.
        """
        action1 = self.get_battle_action(self.t1)
        action2 = self.get_battle_action(self.t2)

        # Phase 1: Switching/Items (Switch logic handled within Trainer method)
        if action1[0] == "SWITCH" or action1[0] == "ITEM":
            pass 
        if action2[0] == "SWITCH" or action2[0] == "ITEM":
            pass

        # Phase 2: Speed check and attacks
        pokemon1 = self.t1.get_active_pokemon()
        pokemon2 = self.t2.get_active_pokemon()

        if action1[0] == "MOVE" and action2[0] == "MOVE":
            # Determine turn order based on Speed stat
            if pokemon1.stats['Speed'] >= pokemon2.stats['Speed']:
                self.execute_attack(self.t1, self.t2, action1[1])
                
                # Check if defender survived the first strike
                if not pokemon2.is_fainted(): 
                    self.execute_attack(self.t2, self.t1, action2[1])
                    # Check if pokemon1 fainted from the counter-attack
                    if pokemon1.is_fainted():
                        typewriter_print(f"\n{pokemon1.name} fainted!")
                        if self.handle_faint(self.t1): 
                            pokemon1 = self.t1.get_active_pokemon()            
                        else:
                            return

                else:
                    # pokemon2 fainted from the first hit
                    typewriter_print(f"\n{pokemon2.name} fainted!")
                    if self.handle_faint(self.t2): 
                        pokemon2 = self.t2.get_active_pokemon()
                    else:
                        return # End turn if trainer is defeated
            
            else:
                self.execute_attack(self.t2, self.t1, action2[1])
                
                # Check if defender survived the first strike
                if not pokemon1.is_fainted():
                    self.execute_attack(self.t1, self.t2, action1[1])
                    # Check if pokemon2 fainted from the counter-attack
                    if pokemon2.is_fainted():
                        typewriter_print(f"\n{pokemon2.name} fainted!")
                        if self.handle_faint(self.t1): 
                            pokemon2 = self.t2.get_active_pokemon()            
                        else:
                            return

                else:
                    typewriter_print(f"\n{pokemon1.name} fainted!")
                    if self.handle_faint(self.t1): 
                        pokemon1 = self.t1.get_active_pokemon()
                    else:
                        return # End turn if trainer is defeated
        
        # Scenario where only one Pokemon attacks (due to switch or item use)
        elif action1[0] == "MOVE":
            self.execute_attack(self.t1, self.t2, action1[1])
            if pokemon2.is_fainted(): 
                typewriter_print(f"\n{pokemon2.name} fainted!")
                if self.handle_faint(self.t2): 
                    pokemon2 = self.t2.get_active_pokemon()
                else:
                    return 

        elif action2[0] == "MOVE":
            self.execute_attack(self.t2, self.t1, action2[1])
            if pokemon1.is_fainted(): 
                typewriter_print(f"\n{pokemon1.name} fainted!")
                if self.handle_faint(self.t1): 
                    pokemon1 = self.t1.get_active_pokemon()
                else:
                    return 

        typewriter_print("\n" + "-"*30)
        typewriter_print("STATUS UPDATE:")
        typewriter_print(f"{pokemon1.name}: {pokemon1.hp_current}/{pokemon1.hp_max} HP")
        typewriter_print(f"{pokemon2.name}: {pokemon2.hp_current}/{pokemon2.hp_max} HP")
        typewriter_print("-"*30)        

    def get_battle_action(self, trainer):
        """
        Displays the battle menu and returns the selected action.
        """
        typewriter_print(f"\n--- What will {trainer.name} do? ---")
        typewriter_print("1. Fight")
        typewriter_print("2. Switch Pokemon")
        typewriter_print("3. Item (Not implemented)")
        
        choice = input("Select (1-3): ")
        
        if choice == '1':
            move = trainer.choose_move() # Returns move name as string
            return ("MOVE", move)
        elif choice == '2':
            trainer.switch_pokemon() 
            return ("SWITCH", trainer.get_active_pokemon())
        else:
            typewriter_print("Action not available yet! Please select again.")
            return self.get_battle_action(trainer) 

    def bonus_type(self, move_type, defender_type):
        """
        Calculates type effectiveness. Multiplies values for dual-type defenders.
        """
        modifier = 1.0
        for d_type in defender_type:
            if move_type in TYPE_CHART:
                modifier *= TYPE_CHART[move_type].get(d_type, 1.0)
        return modifier

    def attack_effect(self, move_name):
        """Placeholder for future status effects or stat changes."""
        pass 

    def execute_attack(self, attacker_trainer, defender_trainer, move_name):
        """
        Executes a move, calculates damage using the official formula, 
        and updates the defender's HP.
        """
        attacker = attacker_trainer.get_active_pokemon()
        defender = defender_trainer.get_active_pokemon()
        move_data = MOVES_LIBRARY[move_name]
            
        typewriter_print(f"{attacker.name} used {move_name}!")
            
        # PP check through MoveManager
        if not attacker.move_manager.spend_pp(move_name):
            return
            
        # Official Damage Formula components
        level_part = (2 * attacker.level / 5) + 2
        stat_ratio = attacker.stats['Attack'] / defender.stats['Defense']
        base_damage = ((level_part * int(move_data.power) * stat_ratio) / 50) + 2
        random_factor = random.uniform(0.85, 1.0)
            
        # STAB check: x1.5 if move type matches attacker's type
        stab = 1.5 if move_data.type in attacker.type else 1.0

        # Type effectiveness calculation
        type_modifier = self.bonus_type(move_data.type, defender.type)
        if type_modifier > 1:
            typewriter_print("It's super effective!")
        elif 0 < type_modifier < 1:
            typewriter_print("It's not very effective...")
        elif type_modifier == 0:
            typewriter_print(f"It doesn't affect {defender.name}...")
        
        # Calculate and apply final damage
        modifier = random_factor * stab * type_modifier
        final_damage = int(base_damage * modifier)

        defender.hp_current -= final_damage
        if defender.hp_current < 0:
            defender.hp_current = 0

        # Execute secondary effects
        self.attack_effect(move_name)

        return