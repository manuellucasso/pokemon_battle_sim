import random
from move import Move

class Pokemon:
    def __init__(self, POKEMON_DATA, level, moves=None, status_conditions=None):
        """
        Initializes a Pokemon instance with base stats and level-dependent scaling.
        """
        
        # Extract base stats from the provided POKEMON_DATA dictionary
        stats_ref = POKEMON_DATA['base_stats']
        
        self.name = stats_ref['Name']
        self.type = stats_ref['Type']
        self.level = level
        
        # Getting the reference stats from the base stats in the POKEMON_DATA
        stat_keys = ["Attack", "Defense", "SpAtk", "SpDef", "Speed","HP","Total"]
        self.initial_stats = {key: stats_ref[key] for key in stat_keys}
       
        # Attributes calculated based on the current level
        self.stats = self.stats_calculator(self.level, self.initial_stats)
       
        # Dynamic battle attributes
        self.hp_max = stats_ref['HP']
        self.hp_current = self.hp_max    # Starts with full HP
        self.xp_current = 0              # Accumulated experience
        self.xp_max = self.stats['XP']   # Threshold for the next level


        # Move set and status management
        self.move_set_list = POKEMON_DATA["lvl_up"]
        self.teach_list = POKEMON_DATA["teach"]  
        self.moves = moves if moves else self.initial_move_set(self.move_set_list)
        self.status_conditions = status_conditions if status_conditions else []

    def gain_xp(self, xp):
        """
        Adds XP and triggers level-up sequence if the threshold is met.
        """
        self.xp_current += xp
        print(f"{self.name} gained {xp} XP!")

        # Check for multiple level-ups if enough XP is gained
        while self.xp_current >= self.xp_max:
            self.level_up()

    def level_up(self): 
        """
        Increases level and updates all stats and thresholds accordingly.
        """
        self.level += 1            
        print(f"{self.name} leveled up to level {self.level}!")

        # Recalculate stats for the new level
        self.stats = self.stats_calculator(self.level, self.initial_stats)

        # Update max thresholds
        self.hp_current_max = self.hp_max
        self.hp_max = self.stats['HP']  
        self.xp_max = self.stats['XP']

        # Proportional HP increase based on the growth of hp_max
        hp_increase = self.hp_max - self.hp_current_max
        self.hp_current += hp_increase

        # Check for move learning opportunities at the new level  
        for move in self.move_set_list:
            if move['level'] == self.level:
                self.learn_move(move['move'])

    def stats_calculator(self, level, initial_stats):
        """
        Mathematical model to scale stats from level 1 base values.
        """
        current_stats = {}
        
        # HP Calculation (20% growth per level)
        current_stats['HP'] = initial_stats["HP"] + initial_stats["HP"] * 0.2 * (level - 1)
        
        # XP Threshold (Power law growth for difficulty curve)
        current_stats['XP'] = int(100 * (level ** 1.5)) 
        current_stats['XP_reward'] = int(current_stats['XP'] * 0.1)
        
        # Combat Stats (10% growth per level)
        for stat in ['Attack', 'Defense', 'SpAtk', 'SpDef', 'Speed', 'Total']:
            current_stats[stat] = int(initial_stats[stat] + (initial_stats[stat] * 0.1 * (level - 1)))

        return current_stats
    
    def learn_move(self, move):
        """
        Handles move learning logic, including the 4-move limit replacement.
        """
        if len(self.moves) < 4:
            self.moves.append(move)
            print(f"{self.name} learned {move.name}!")
        else:
            print(f"{self.name} can't learn {move.name} because it already knows 4 moves.")
            print(f"{self.name} may forget a move to learn {move.name}.")
            print("Do you want to forget a move? (yes/no)")
            
            choice = input().lower()
            if choice == 'yes':
                print("Which move do you want to forget (1-4)?")
                for i, m in enumerate(self.moves, 1):
                    print(f"[{i}] {m.name}")

                move_to_forget = int(input()) - 1

                if 0 <= move_to_forget < len(self.moves):
                    forgotten_move = self.moves.pop(move_to_forget)
                    self.moves.insert(move_to_forget, move)
                    print(f"1, 2, 3 and... Done! {self.name} forgot {forgotten_move.name} and learned {move.name}!")    
                else:
                    print("Invalid choice. No move was forgotten.")


    def initial_move_set(self, move_list):
        """
        Initializes the Pokemon's move set based on its level and a provided move list.
        """

        # Available moves at the current level
        available_moves = [m['move_name'] for m in move_list if m['level'] is not None and m['level'] <= self.level]
        
        # Get the 6th strongest moves from the available moves
        initial_moves = available_moves[-6:]

        # If there are more than 6 moves, randomly select 4 from the last 6
        if len(initial_moves) > 4:
            return random.sample(initial_moves, 4)          

        return initial_moves  

