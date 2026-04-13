import random
from data_loader import MOVES_LIBRARY, typewriter_print, set_network_connection
from battle_effects import BattleEffectsMixin
from battle_states import BattleStates

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

class Battle(BattleEffectsMixin):
    def __init__(self, trainer1, trainer2, network_socket=None):
        """
        Initializes a battle between two trainers.
        """
        self.t1 = trainer1
        self.t2 = trainer2
        self.turn_count = 1
        self.battle_log = [] # Useful for syncing future online matches
        self.t1_flag ={}
        self.t2_flag = {}

        # Save the network connection
        self.network_connection = network_socket

        # Plug the network cable into the printing system!
        if self.network_connection:
            set_network_connection(self.network_connection)

    def start(self):
        """
        Main battle loop that runs until one trainer has no usable Pokemon.
        """
        typewriter_print("")
        typewriter_print(f"--- Battle Started: {self.t1.name} vs {self.t2.name} ---")
        
        while self.check_battle_status():
            typewriter_print("")
            typewriter_print(f"=== Turn {self.turn_count} ===")
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
            typewriter_print("")
            typewriter_print(f"{self.t1.name} is out of usable Pokemon! {self.t2.name} wins!")
            return False
        if not t2_can_fight:
            typewriter_print("")
            typewriter_print(f"{self.t2.name} is out of usable Pokemon! {self.t1.name} wins!")
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
        # Check if trainers can act (for future status effects that may prevent action)
        if self.t1.can_act:
            action1 = self.get_battle_action(self.t1)
        else:
            action1[0] = "MOVE"
            action1[1] = self.t1.get_active_pokemon().last_move_used

        if self.t2.can_act:
            action2 = self.get_battle_action(self.t2)
        else:
            action2[0] = "MOVE"
            action2[1] = self.t2.get_active_pokemon().last_move_used

        # Checking it is was mimic or random move and adjusting the action accordingly
        if action1[0]=="MOVE" and action1[1].lower()=="mimic":
            last_move = self.t2.get_active_pokemon().last_move_used
            if last_move:
                action1 = ("MOVE", last_move)
            else:
                typewriter_print(f"But it failed! {self.t2.get_active_pokemon().name} hasn't used a move yet!")
                action1 = ("MOVE", "Splash") # Default to a weak move if Mimic fails

        if action1[0]=="MOVE" and action1[1].lower()=="metronome":
            random_move = MOVES_LIBRARY[random.choice(list(MOVES_LIBRARY.keys()))].name
            if random_move:
                action1 = ("MOVE", random_move) 


        if action2[0]=="MOVE" and action2[1].lower()=="metronome":
            random_move = MOVES_LIBRARY[random.choice(list(MOVES_LIBRARY.keys()))].name
            if random_move:
                action2 = ("MOVE", random_move)
     
     
        pokemon1 = self.t1.get_active_pokemon()
        pokemon2 = self.t2.get_active_pokemon()

        # Phase 1: Switching/Items (Switch logic handled within Trainer method)
        if action1[0] == "SWITCH":
            typewriter_print(f"{self.t1.name} switched the Pokemon! Go! {self.t1.get_active_pokemon().name}!", broadcast=True)
            pass 
        elif action1[0] == "ITEM":
            typewriter_print(f"{self.t1.name} used an item!")
            pass

        if action2[0] == "SWITCH":
            typewriter_print(f"{self.t2.name} switched the Pokemon! Go! {self.t2.get_active_pokemon().name}!", broadcast=True)
            pass
        elif action2[0] == "ITEM":
            typewriter_print(f"{self.t2.name} used an item!")
            pass

        
        # Phase 1: Speed check and attacks
        if action1[0] == "MOVE":
            if action1[1].lower() == "quick attack":
                pokemon1_speed = 10000+pokemon1.stats['Speed'] # Quick Attack always goes first
            else:   
                pokemon1_speed = pokemon1.stats['Speed']
        
        if action2[0] == "MOVE":
            if action2[1].lower() == "quick attack":
                pokemon2_speed = 10000+pokemon2.stats['Speed'] # Quick Attack always goes first
            else:
                pokemon2_speed = pokemon2.stats['Speed']

        if action1[0] == "MOVE" and action2[0] == "MOVE":
            # Determine turn order based on Speed stat
            if pokemon1_speed >= pokemon2_speed:

                # Check flags and status before attack
                if BattleStates.can_attack(pokemon1):
                    self.execute_attack(self.t1, self.t2, action1[1])

                elif BattleStates.can_attack(pokemon1)=="unleash_bide":
                    typewriter_print(f"{pokemon1.name} unleashed energy!")
                    vengence = pokemon1.bide_damage_taken * 2
                    pokemon2.hp_current = max(0, pokemon2.hp_current - vengence)
                    typewriter_print(f"It dealt {vengence} damage!")
                
                    # Zero Bide
                    pokemon1.bide_damage_taken = 0   
                
                # Check if defender survived the first strike
                if not pokemon2.is_fainted():
                    # Check flags and status before attack
                    if BattleStates.can_attack(pokemon2):
                        self.execute_attack(self.t2, self.t1, action2[1])

                    elif BattleStates.can_attack(pokemon2)=="unleash_bide":
                        typewriter_print(f"{pokemon2.name} unleashed energy!")
                        vengence = pokemon2.bide_damage_taken * 2
                        pokemon1.hp_current = max(0, pokemon1.hp_current - vengence)
                        typewriter_print(f"It dealt {vengence} damage!")
                    
                        # Zero Bide
                        pokemon2.bide_damage_taken = 0     
                    
                    # Check if pokemon1 fainted from the counter-attack
                    if pokemon1.is_fainted():
                        typewriter_print("")
                        typewriter_print(f"{pokemon1.name} fainted!")
                        if self.handle_faint(self.t1): 
                            pokemon1 = self.t1.get_active_pokemon()            
                        else:
                            return

                else:
                    # pokemon2 fainted from the first hit
                    typewriter_print("")
                    typewriter_print(f"{pokemon2.name} fainted!")
                    if self.handle_faint(self.t2): 
                        pokemon2 = self.t2.get_active_pokemon()
                    else:
                        return # End turn if trainer is defeated
            
            else:
                # Check flags and status before attack
                if BattleStates.can_attack(pokemon2):
                    self.execute_attack(self.t2, self.t1, action2[1])

                elif BattleStates.can_attack(pokemon2)=="unleash_bide":
                        typewriter_print(f"{pokemon2.name} unleashed energy!")
                        vengence = pokemon2.bide_damage_taken * 2
                        pokemon1.hp_current = max(0, pokemon1.hp_current - vengence)
                        typewriter_print(f"It dealt {vengence} damage!")

                        # Zero Bide
                        pokemon2.bide_damage_taken = 0      
                
                # Check if defender survived the first strike
                if not pokemon1.is_fainted():
                    
                    # Check flags and status before attack
                    if BattleStates.can_attack(pokemon1):
                        self.execute_attack(self.t1, self.t2, action1[1])

                    elif BattleStates.can_attack(pokemon1)=="unleash_bide":
                        typewriter_print(f"{pokemon1.name} unleashed energy!")
                        vengence = pokemon1.bide_damage_taken * 2
                        pokemon2.hp_current = max(0, pokemon2.hp_current - vengence)
                        typewriter_print(f"It dealt {vengence} damage!")
                    
                        # Zero Bide
                        pokemon1.bide_damage_taken = 0     
                    
                    # Check if pokemon2 fainted from the counter-attack
                    if pokemon2.is_fainted():
                        typewriter_print("")
                        typewriter_print(f"{pokemon2.name} fainted!")
                        if self.handle_faint(self.t): 
                            pokemon2 = self.t2.get_active_pokemon()            
                        else:
                            return

                else:
                    typewriter_print("")
                    typewriter_print(f"{pokemon1.name} fainted!")
                    if self.handle_faint(self.t1): 
                        pokemon1 = self.t1.get_active_pokemon()
                    else:
                        return # End turn if trainer is defeated
        
        # Scenario where only one Pokemon attacks (due to switch or item use)
        elif action1[0] == "MOVE":
            
            # Check flags and status before attack
            if BattleStates.can_attack(pokemon1):
                self.execute_attack(self.t1, self.t2, action1[1])

            elif BattleStates.can_attack(pokemon1)=="unleash_bide":
                    typewriter_print(f"{pokemon1.name} unleashed energy!")
                    vengence = pokemon1.bide_damage_taken * 2
                    pokemon2.hp_current = max(0, pokemon2.hp_current - vengence)
                    typewriter_print(f"It dealt {vengence} damage!")
                
                    # Zero Bide
                    pokemon1.bide_damage_taken = 0     
            
            if pokemon2.is_fainted(): 
                typewriter_print("")
                typewriter_print(f"{pokemon2.name} fainted!")
                if self.handle_faint(self.t2): 
                    pokemon2 = self.t2.get_active_pokemon()
                else:
                    return 

        elif action2[0] == "MOVE":
            
            # Check flags and status before attack
            if BattleStates.can_attack(pokemon2):
                self.execute_attack(self.t2, self.t1, action2[1])

            elif BattleStates.can_attack(pokemon2)=="unleash_bide":
                        typewriter_print(f"{pokemon2.name} unleashed energy!")
                        vengence = pokemon2.bide_damage_taken * 2
                        pokemon1.hp_current = max(0, pokemon1.hp_current - vengence)
                        typewriter_print(f"It dealt {vengence} damage!")

                        # Zero Bide
                        pokemon2.bide_damage_taken = 0    
            
            if pokemon1.is_fainted():
                typewriter_print("") 
                typewriter_print(f"{pokemon1.name} fainted!")
                if self.handle_faint(self.t1): 
                    pokemon1 = self.t1.get_active_pokemon()
                else:
                    return

        BattleStates.apply_end_of_turn_effects(pokemon1, pokemon2,self.t1)     
        BattleStates.apply_end_of_turn_effects(pokemon2, pokemon1,self.t2)     

        typewriter_print("")
        typewriter_print("-" * 30)
        typewriter_print("STATUS UPDATE:")
        typewriter_print(f"{pokemon1.name}: {pokemon1.hp_current}/{pokemon1.hp_max} HP")
        typewriter_print(f"{pokemon2.name}: {pokemon2.hp_current}/{pokemon2.hp_max} HP")
        typewriter_print("-"*30)        

    def get_battle_action(self, trainer):
        """
        Displays the battle menu and returns the selected action.
        """
        
        # The visual menu - This is automatically sent to the client via our new typewriter_print!
        typewriter_print("")
        typewriter_print(f"--- What will {trainer.name} do? ---",is_me=trainer.is_local, broadcast=False)
        typewriter_print("1. Fight",is_me=trainer.is_local, broadcast=False)
        typewriter_print("2. Switch Pokemon",is_me=trainer.is_local, broadcast=False)
        typewriter_print("3. Item (Not implemented)",is_me=trainer.is_local, broadcast=False)
        
        # --- THE NETWORK CROSSROADS ---
        # If it is the opponent's turn (t2) AND we are playing online
        if trainer == self.t2 and self.network_connection:
            
            # 1. Send the tag to unlock the client's keyboard
            self.network_connection.send("ACTION|CHOOSE_ACTION".encode('utf-8'))
            
            # 2. Pause the server and wait for the client's response over the internet
            choice = self.network_connection.recv(1024).decode('utf-8')
            
        else:
            # If it is your turn (t1) or an offline match, use local keyboard
            choice = input("Select (1-3): ")

        # --- ACTION PROCESSING ---       
        if choice == '1':
            move = trainer.choose_move() # Returns move name as string
            trainer.get_active_pokemon().last_move_used = move # Store last move for future reference
            return ("MOVE", move)
        
        elif choice == '2':
            active_poke = trainer.get_active_pokemon()
            
            # TRAP CHECK: Prevent switching if trapped
            if active_poke.trap_turns > 0:
                typewriter_print(f"{active_poke.name} is trapped by an attack and cannot switch out!")
                return self.get_battle_action(trainer) # Ask for input again    

            trainer.switch_pokemon() 
            return ("SWITCH", trainer.get_active_pokemon())
        
        else:
            typewriter_print("Action not available yet! Please select again.",is_me=trainer.is_local, broadcast=False)
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
        base_damage = ((level_part * int(move_data.power) * stat_ratio) / 50)
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


        # Calculate protection modifier based on defender's current state and move type
        protection_modifier = BattleStates.calculate_modifier_protection(defender, move_data)

        # Calculate and apply final damage
        modifier = random_factor * stab * type_modifier * protection_modifier
        final_damage = int(base_damage * modifier)

        # Checking if it will miss or not
        hit_chance = int(move_data.accuracy) * (attacker.accuracy_multiplier / defender.evasion_multiplier)

        if move_name.lower() == "swift":
            hit_chance=100

        # Execute secondary effects
        effect_result = BattleEffectsMixin.attack_effect(move_name,attacker,defender,final_damage)
                
        # Verify if it's a tuple of just a flag
        flag = "none"
        if isinstance(effect_result, tuple): 
            flag, value = effect_result

        elif isinstance(effect_result, str):
            flag = effect_result 
  

        # Test for hit
        if random.randint(1, 100) > hit_chance or defender.is_hidden:
            typewriter_print(f"{attacker.name}'s attack missed!")

            if flag == "self_on_miss":
                BattleStates.is_self_on_miss(attacker, final_damage)
                return # no no damage

            return # No damage
        
        else:
            
            if flag=="fixed_damage":
                BattleStates.is_fixed(attacker,defender, move_data, final_damage)

            elif flag=="preparing":
                BattleStates.is_preparing(attacker, defender, move_data, final_damage, attacker_trainer)    
            
            elif flag=="multi_hits":
                BattleStates.is_multi(attacker, defender, move_data, value, final_damage)

            elif flag=="self_damage":
                BattleStates.is_selfie(attacker, defender, move_data, final_damage)

            elif flag == "faint" or flag == "one_ko":
                mon = defender if flag == "one_ko" else attacker
                BattleStates.is_faint(mon)

            elif flag=="force_switch":
                BattleStates.is_force_switch(self, defender_trainer) 

            elif flag=="high_crit":
                BattleStates.is_high_crit(attacker, defender, move_data, final_damage)

            elif flag=="variable_damage":
                BattleStates.is_variable_damage(attacker, defender, move_data)

            elif flag=="double_at_hit":
                BattleStates.is_double_at_hit(attacker, defender, move_data, final_damage)

            elif flag=="protect_stats":
                BattleStates.is_protect_stats(attacker_trainer,value) 
                
            elif flag=="escape":
                BattleStates.is_escape(attacker) 

            elif flag=="halve_special":
                BattleStates.is_protect_spe(attacker_trainer,value) 

            elif flag=="halve_physical":
                BattleStates.is_protect_phy(attacker_trainer, value)        

            else:
                               
                defender.hp_current -= final_damage
                if defender.hp_current < 0:
                    defender.hp_current = 0

                elif defender.bide_turns > 0:
                    defender.bide_damage_taken += final_damage
                    typewriter_print(f"{defender.name} is storing energy!")    

        return
    


