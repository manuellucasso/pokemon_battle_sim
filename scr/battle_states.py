import random
from data_loader import typewriter_print

class BattleStates:
    
    @staticmethod
    def can_attack(pokemon):
        """
        Checks all flags and statuses before the Pokemon executes a move.
        Returns True if it can attack, False if prevented by a flag.
        """
        # 1. Check Recharging (Ex: Hyper Beam)
        if pokemon.is_recharging:
            typewriter_print(f"{pokemon.name} must recharge!")
            pokemon.is_recharging = False # Resets for the next turn
            return False
            
        # 2. Check Flinch (Ex: Bite, Rock Slide)
        if pokemon.is_flinching:
            typewriter_print(f"{pokemon.name} flinched and couldn't move!")
            pokemon.is_flinching = False # Flinch only lasts for the current turn
            return False
            
        # 3. Check fixed Status Conditions (Sleep, Freeze, Paralysis)
        if pokemon.status_conditions == "SLP":
            # Simple example: 25% chance to wake up
            if random.randint(1, 100) <= 25:
                typewriter_print(f"{pokemon.name} woke up!")
                pokemon.status_conditions = None
            else:
                typewriter_print(f"{pokemon.name} is fast asleep.")
                return False
                
        if pokemon.status_conditions == "FRZ":
            # 20% chance to thaw out
            if random.randint(1, 100) <= 25:
                typewriter_print(f"{pokemon.name} thawed out!")
                pokemon.status_conditions = None
            else:
                typewriter_print(f"{pokemon.name} is frozen solid!")
                return False
                
        if pokemon.status_conditions == "PAR":
            # 25% chance of paralysis preventing the attack
            if random.randint(1, 100) <= 25:
                typewriter_print(f"{pokemon.name} is paralyzed! It can't move!")
                return False

        # If it passed all checks, it can attack!
        return True

    @staticmethod
    def apply_end_of_turn_effects(pokemon):
        """
        Processes effects that occur at the end of the turn (Trap damage, Poison, etc).
        """
        # Check continuous Status Damage
        if pokemon.status_conditions == "PSN":
            dmg = max(1, pokemon.hp_max // 8)
            pokemon.hp_current -= dmg
            typewriter_print(f"{pokemon.name} is hurt by poison!")
            
        elif pokemon.status_conditions == "BRN":
            dmg = max(1, pokemon.hp_max // 8)
            pokemon.hp_current -= dmg
            typewriter_print(f"{pokemon.name} is hurt by its burn!")

        # Check Traps (Ex: Bind, Fire Spin)
        if pokemon.trap_turns > 0:
            dmg = max(1, pokemon.hp_max // 16) # Light trap damage
            pokemon.hp_current -= dmg
            pokemon.trap_turns -= 1
            typewriter_print(f"{pokemon.name} is hurt by the trap!")
            if pokemon.trap_turns == 0:
                typewriter_print(f"{pokemon.name} was freed from the trap!")