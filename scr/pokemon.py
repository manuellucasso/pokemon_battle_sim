import random
from move import Move
from move_manager import MoveManager
from data_loader import typewriter_print

class Pokemon:
    def __init__(self, POKEMON_DATA, level, status_conditions=None):
        """
        Initializes a Pokemon instance with base stats and level-dependent scaling.
        """
        
        # Extract base stats from the provided POKEMON_DATA dictionary
        stats_ref = POKEMON_DATA['base_stats']
        
        self.name = stats_ref['Name']
        self.type = stats_ref['Type'].split()
        self.level = level
        
        # Getting the reference stats from the base stats in the POKEMON_DATA
        stat_keys = ["Attack", "Defense", "SpAtk", "SpDef", "Speed","HP","Total"]
        self.initial_stats = {key: stats_ref[key] for key in stat_keys}
        
       
        # Attributes calculated based on the current level
        self.stats = self.stats_calculator(self.level, self.initial_stats)
        self.hp_max = self.stats['HP']
        self.xp_max = self.stats['XP']   # Threshold for the next level
        
        # Dynamic battle attributes
        self.hp_current = self.hp_max    # Starts with full HP
        self.xp_current = 0              # Accumulated experience
        self.status_conditions = status_conditions if status_conditions else []
        self.evasion_multiplier = 1
        self.accuracy_multiplier = 1

        # State Flags for battle
        self.is_flinching = False
        self.is_recharging = False
        self.trap_turns = 0
        
        # Move set and status management
        self.move_set_list = POKEMON_DATA["lvl_up"]
        self.teach_list = POKEMON_DATA["teach"]  
        
       # Initialize the MoveManager for handling move learning and management 
        self.move_manager = MoveManager(
                pokemon_name=self.name,
                pokemon_level=self.level,
                pokemon_lvl_up_moves=self.move_set_list,
                pokemon_teach_moves=self.teach_list
            )

    def __repr__(self):
        f"{self.name} ({self.hp_current}/{self.hp_max} HP)"
    
    def gain_xp(self, xp):
        """
        Adds XP and triggers level-up sequence if the threshold is met.
        """
        self.xp_current += xp
        typewriter_print(f"\n{self.name} gained {xp} XP!")

        # Check for multiple level-ups if enough XP is gained
        while self.xp_current >= self.xp_max:
            self.level_up()

    def level_up(self): 
        """
        Increases level and updates all stats and thresholds accordingly.
        """
        self.level += 1            
        typewriter_print(f"\n{self.name} leveled up to level {self.level}!")

        # Recalculate stats for the new level
        self.stats = self.stats_calculator(self.level, self.initial_stats)

        # Update max thresholds
        self.hp_current_max = self.hp_max
        self.hp_max = self.stats['HP']  
        self.xp_max = self.stats['XP']

        # Proportional HP increase based on the growth of hp_max
        hp_increase = self.hp_max - self.hp_current_max
        self.hp_current += hp_increase

        # Learn new moves after leveling up 
        self.move_manager.learn_move_by_level_up(self.level)

    def stats_calculator(self, level, initial_stats):
        """
        Mathematical model to scale stats from level 1 base values.
        """
        current_stats = {}
        
        # HP Calculation (20% growth per level)
        current_stats['HP'] = int(initial_stats['HP']*2*level/100 +10+level)
        
        # XP Threshold (Power law growth for difficulty curve)
        current_stats['XP'] = level ** 3 
        current_stats['XP_reward'] = int(current_stats['XP'] * 0.1)
        
        # Combat Stats (10% growth per level)
        for stat in ['Attack', 'Defense', 'SpAtk', 'SpDef', 'Speed']:
            current_stats[stat] = int(initial_stats[stat]*2*level/100 +5)

        current_stats['Total'] = sum(current_stats[stat] for stat in ['Attack', 'Defense', 'SpAtk', 'SpDef', 'Speed']) + current_stats['HP']    

        return current_stats
    
    def is_fainted(self):
        """
        Checks if the Pokemon has fainted (HP reached 0).
        """
        if self.hp_current <= 0:
            return True
        else:
            return False 
    

    
