import random
from data_loader import MOVES_LIBRARY

class Battle:
    def __init__(self, trainer1, trainer2):
        """
        Initializes a battle between two trainers.
        """
        self.t1 = trainer1
        self.t2 = trainer2
        self.turn_count = 1
        self.battle_log = [] # Useful for syncing with your brother in Germany

    def start(self):
        """
        Main battle loop that runs until one trainer has no usable Pokemon.
        """
        print(f"\n--- Battle Started: {self.t1.name} vs {self.t2.name} ---")
        
        while self.check_battle_status():
            print(f"\n=== Turn {self.turn_count} ===")
            self.run_turn()
            self.turn_count += 1

    
    def check_battle_status(self):
        """
        Checks if both trainers still have at least one conscious Pokemon.
        """
        t1_can_fight = any(p.hp_current > 0 for p in self.t1.pokemons)
        t2_can_fight = any(p.hp_current > 0 for p in self.t2.pokemons)
        
        if not t1_can_fight:
            print(f"\n{self.t1.name} is out of usable Pokemon! {self.t2.name} wins!")
            return False
        if not t2_can_fight:
            print(f"\n{self.t2.name} is out of usable Pokemon! {self.t1.name} wins!")
            return False
        return True

    
    def run_turn(self):
        """
        Orchestrates the sequence of actions in a single turn.
        """
        action1 = self.get_battle_action(self.t1)
        action2 = self.get_battle_action(self.t2)

        # Switching goes first  // Switch happened via trainer method
        if action1[0] == "SWITCH" or action1[0] == "ITEM":
            pass 
        if action2[0] == "SWITCH" or action2[0] == "ITEM":
            pass

        # Pokemon attacks
        pokemon1 = self.t1.get_active_pokemon()
        pokemon2 = self.t2.get_active_pokemon()

        # Deciding who attacks first
        if action1[0] == "MOVE" and action2[0] == "MOVE":
            if pokemon1.stats['Speed'] >= pokemon2.stats['Speed']:
                self.execute_attack(self.t1, self.t2, action1[1])
                if self.is_fainted(pokemon2): # Strikes back only if it hasnt fainted
                    self.execute_attack(self.t2, self.t1, action2[1])
            else:
                self.execute_attack(self.t2, self.t1, action2[1])
                if self.is_fainted(pokemon1):
                    self.execute_attack(self.t1, self.t2, action1[1])
        
        # Se apenas um atacou (o outro trocou)
        elif action1[0] == "MOVE":
            self.execute_attack(self.t1, self.t2, action1[1])
        elif action2[0] == "MOVE":
            self.execute_attack(self.t2, self.t1, action2[1])


    def get_battle_action(self,trainer):
        """
        Main menu during a battle turn. 
        Returns a tuple: (type of action, action details)
        """
        print(f"\n--- What will {trainer.name} do? ---")
        print("1. Fight")
        print("2. Switch Pokemon")
        print("3. Item (Not implemented)")
        
        choice = input("Select (1-3): ")
        
        if choice == '1':
            move = trainer.choose_move() # Seu método que retorna o nome do golpe
            return ("MOVE", move)
        elif choice == '2':
            # Aqui chamamos o switch_pokemon que você criou, que já mostra a lista
            trainer.switch_pokemon() 
            return ("SWITCH", trainer.get_active_pokemon())
        else:
            print("Action not available yet! Please, select again! ")
            return  self.get_battle_action(trainer)  



    def bonus_type(self,attacker_type1,attacker_type2, defender_type1, defender_type2):
        return type_modifier

    def is_fainted(self,pokemon):
        """
        Checks if the Pokemon has fainted (HP reached 0).
        """
        if pokemon.hp_current <= 0:
        
            return True
        else:
            return False 

    def attack_effect(move_name):
        return         
    


    def execute_attack(self, attacker_trainer, defender_trainer, move_name):
        """
        Logic for processing a single attack.
        """
        attacker = attacker_trainer.get_active_pokemon()
        defender = defender_trainer.get_active_pokemon()
        move_data = MOVES_LIBRARY[move_name]
            
        print(f"{attacker.name} used {move_name}!")
            
        # Damage calculation logic here
        if not attacker.move_manager.spend_pp(move_name):
            return
            
        level_part = (2 * attacker.level / 5) + 2
        stat_ratio = attacker.stats['Attack'] / defender.stats['Defense']
        base_damage = ((level_part * move_data.power * stat_ratio) / 50) + 2
        random_factor = random.uniform(0.85, 1.0)
            
        # STAB (Same Type Attack Bonus): x1.5 if the type is the same as the pokemon
        stab = 1.5 if move_data.type == attacker.type1 or move_data.type == attacker.type2 else 1.0

        # Extra bonus for type
        type_modifier = bonus_type(attacker.type1,attacker.type2, defender.type1, defender.type2)
        
        # Multiplicador final
        modifier = random_factor * stab * type_modifier
        final_damage = int(base_damage * modifier)

        # Damage application
        defender.hp_current -= final_damage
        if defender.hp_current < 0:
            defender.hp_current = 0

        # Check Fainited
        if is_fainted(defender) == True:

        else:
            attack_effect(move_name)

        return    