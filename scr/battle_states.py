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
            
            
        if pokemon.bide_turns > 0:
            typewriter_print(f"{pokemon.name} is enduring the hits!")
            return False # mon tanks
                
        elif pokemon.bide_turns == 0:
            return "unleash_bide"
            
  
        if pokemon.charge_turns > 0:
            typewriter_print(f"{pokemon.name} is still charging!")
            return False 
                
        elif pokemon.charge_turns == 0:
            pokemon.is_hidden = False
            pokemon.is_preparing = False
            return True            

        # If it passed all checks, it can attack!
        return True

    @staticmethod
    def apply_end_of_turn_effects(pokemon, opponent,trainer):
        """
        Processes effects that occur at the end of the turn (Trap damage, Poison, etc).
        """
        
        # Check for Bide turns 
        if pokemon.bide_turns > 0:
            pokemon.bide_turns -= 1
        
        # Check for charging state (Ex: Hyper Beam recharge)
        if pokemon.charge_turns > 0:
            pokemon.charge_turns -= 1
            if pokemon.charge_turns == 0:
                typewriter_print(f"{pokemon.name} has finished recharging!")   
        
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

        if pokemon.is_seeded:
            # Calculate damage: 1/8th of the afflicted Pokemon's maximum HP
            drain_amount = max(1, pokemon.hp_max // 8)
            
            # Apply the damage to the afflicted Pokemon
            pokemon.hp_current -= drain_amount
            if pokemon.hp_current < 0:
                pokemon.hp_current = 0
            typewriter_print(f"{pokemon.name}'s health is sapped by Leech Seed!")
            
            # Transfer the stolen HP to the opponent
            # Only heal if the opponent is alive and not already at full health
            if opponent.hp_current > 0 and opponent.hp_current < opponent.hp_max:
                opponent.hp_current = min(opponent.hp_max, opponent.hp_current + drain_amount)
                typewriter_print(f"{opponent.name} absorbed nutrients from the seed!")

        # Reduce time for mist protection
        if pokemon.stats_protected:
            for pokemon in trainer.pokemons:
                pokemon.stats_proctected_turns -= 1
                if pokemon.stats_proctected_turns <= 0:
                    pokemon.stats_protected = False
                    pokemon.stats_proctected_turns = 0
                    typewriter_print(f"{pokemon.name}'s mist protection wore off!")

        # Reduce time for special/physical barriers
        if pokemon.is_half_spe:
            for pokemon in trainer.pokemons:
                pokemon.is_half_spe_turns -= 1
                if pokemon.is_half_spe_turns <= 0:
                    pokemon.is_half_spe_turns = False
                    pokemon.is_half_spe_turns = 0
                    typewriter_print(f"{pokemon.name}'s special barrier wore off!")
           
           
        # Reduce time for special/physical barriers
        if pokemon.is_half_phy:
            for pokemon in trainer.pokemons:
                pokemon.is_half_phy_turns -= 1
                if pokemon.is_half_phy_turns <= 0:
                    pokemon.is_half_phy_turns = False
                    pokemon.is_half_phy_turns = 0
                    typewriter_print(f"{pokemon.name}'s physical barrier wore off!")
                              

    @staticmethod
    def is_fixed(attacker,defender, move, fixed_value):
        typewriter_print(f"It dealt a fixed {fixed_value} damage!")

        protection_modifier = BattleStates.calculate_modifier_protection(defender, move)

        fixed_value = int(fixed_value * protection_modifier)
        
        defender.hp_current -= fixed_value
        if defender.hp_current < 0:
            defender.hp_current = 0
        elif defender.bide_turns > 0:
            defender.bide_damage_taken += fixed_value
            typewriter_print(f"{defender.name} is storing energy!")

    @staticmethod
    def is_multi(attacker, defender, move, hits, final_damage):
        typewriter_print(f"Hit {hits} times!")
         
        protection_modifier = BattleStates.calculate_modifier_protection(defender, move)
        
        total_damage = int(final_damage * hits * protection_modifier)

        defender.hp_current -= total_damage
        if defender.hp_current < 0:
            defender.hp_current = 0
        elif defender.bide_turns > 0:
            defender.bide_damage_taken += total_damage
            typewriter_print(f"{defender.name} is storing energy!")

    @staticmethod
    def is_selfie(attacker, defender, move, final_damage):
        """
        ATENÇÃO: Como o `elif flag == "self_damage"` ignora o `else` final do seu código, 
        esta função precisa dar o dano no defensor PRIMEIRO, e depois dar o recoil no atacante!
        """
        
        protection_modifier = BattleStates.calculate_modifier_protection(defender, move)

        final_damage = int(final_damage * protection_modifier)
        
        # 1. Dá o dano no oponente
        defender.hp_current -= final_damage
        if defender.hp_current < 0:
            defender.hp_current = 0
        elif defender.bide_turns > 0:
            defender.bide_damage_taken += final_damage
            typewriter_print(f"{defender.name} is storing energy!")
            
        # 2. Aplica o recuo (recoil) no atacante
        recoil = max(1, final_damage // 4)
        attacker.hp_current = max(0, attacker.hp_current - recoil)
        typewriter_print(f"{attacker.name} took {recoil} recoil damage!")

    @staticmethod
    def is_self_on_miss(attacker, final_damage):
        # Dano de erro (como High Jump Kick) geralmente afeta só o atacante
        crash_dmg = max(1, final_damage // 2)
        attacker.hp_current = max(0, attacker.hp_current - crash_dmg)
        typewriter_print(f"{attacker.name} kept going and crashed for {crash_dmg} damage!")

    @staticmethod
    def is_preparing(attacker, defender, move, final_damage, trainer):
        
        protection_modifier = BattleStates.calculate_modifier_protection(defender, move)

        final_damage = int(final_damage * protection_modifier)
        
        if  attacker.is_preparing:
            trainer.can_act = False
            return
        else:
            trainer.can_act = True
            typewriter_print(f"{attacker.name} is ready to strike with full power!")
            defender.hp_current -= final_damage
            if defender.hp_current < 0:
                    defender.hp_current = 0

            elif defender.bide_turns > 0:
                    defender.bide_damage_taken += final_damage
                    typewriter_print(f"{defender.name} is storing energy!")  
   
    @staticmethod
    def is_faint(pokemon):
        pokemon.hp_current = 0
        typewriter_print(f"{pokemon.name} fainted instantly!")

    @staticmethod
    def is_force_switch(battle_instance, target_trainer):
        typewriter_print("The target was blown away!")
        battle_instance.handle_faint(target_trainer)

    @staticmethod
    def is_high_crit(attacker, defender, move, final_damage):

        protection_modifier = BattleStates.calculate_modifier_protection(defender, move)
        
        final_damage = int(final_damage * protection_modifier)

        # Higher critial chance
        if random.randint(1, 100) <= 15:
            typewriter_print("A critical hit!")
            damage_to_apply = int(final_damage * 1.5)
        else:
            damage_to_apply = final_damage
            
        defender.hp_current -= damage_to_apply
        if defender.hp_current < 0:
            defender.hp_current = 0
        elif defender.bide_turns > 0:
            defender.bide_damage_taken += damage_to_apply
            typewriter_print(f"{defender.name} is storing energy!")

    @staticmethod
    def is_variable_damage(attacker, defender, move):
        protection_modifier = BattleStates.calculate_modifier_protection(defender, move)

        multiplier = random.uniform(0.5, 1.5)
        
        damage_to_apply = int(attacker.level * multiplier * protection_modifier)
        
        typewriter_print("The attack's power fluctuated!")
        defender.hp_current -= damage_to_apply
        if defender.hp_current < 0:
            defender.hp_current = 0
        elif defender.bide_turns > 0:
            defender.bide_damage_taken += damage_to_apply
            typewriter_print(f"{defender.name} is storing energy!")

    @staticmethod
    def is_double_at_hit(attacker, defender, move, final_damage):
        typewriter_print("The move's power was doubled!")

        protection_modifier = BattleStates.calculate_modifier_protection(defender, move)

        damage_to_apply = final_damage * 2 * protection_modifier

        defender.hp_current -= damage_to_apply
        if defender.hp_current < 0:
            defender.hp_current = 0
        elif defender.bide_turns > 0:
            defender.bide_damage_taken += damage_to_apply
            typewriter_print(f"{defender.name} is storing energy!")  

    @staticmethod
    def is_protect_stats(trainer,number_of_turns):
        """
        Applies the Mist effect.
        Protects the user from having its stats lowered by the opponent.
        """
        for pokemon in trainer.pokemons:    
            if not pokemon.stats_protected:
                pokemon.stats_protected = True
                pokemon.stats_proctected_turns = number_of_turns # Mist lasts for the specified number of turns
                typewriter_print(f"{pokemon.name} is shrouded in mist!")
                typewriter_print("Its stats are now protected from reduction!")

    @staticmethod
    def is_protect_phy(trainer,number_of_turns):
        """
        Applies the protect physical effect.
        """
        for pokemon in trainer.pokemons:    
            pokemon.is_half_phy = True
            pokemon.is_half_phy = number_of_turns # Mist lasts for the specified number of turns
            typewriter_print(f"{pokemon.name} is reflecting damage!")
            typewriter_print("Pokemon from your team are now protected from physical attacks!")


    @staticmethod
    def is_protect_spe(trainer,number_of_turns):
        """
        Applies the protect special effect.
        """
        for pokemon in trainer.pokemons:    
            pokemon.is_half_spe = True
            pokemon.is_half_spe = number_of_turns # Mist lasts for the specified number of turns
            typewriter_print(f"{pokemon.name} is screening damage!")
            typewriter_print("Pokemon from your team are now protected from special attacks!")


    @staticmethod
    def is_escape(attacker):    
        typewriter_print(f"{attacker.name} escaped from battle!")
        typewriter_print(f"Failed to escape! {attacker.name} couldn't get away!")


    @staticmethod
    def calculate_modifier_protection(pokemon, move):
        # Check if the move is physical
        if move.type == 'physical':
            # If the Pokemon is under Reflect (half physical damage)
            if pokemon.is_half_phy:
                return 0.5
            else:
                return 1.0
        # Check if the move is special
        elif move.type == 'special':
            # If the Pokemon is under Light Screen (half special damage)
            if pokemon.is_half_spc:
                return 0.5
            else:
                return 1.0
        # If the move is neither physical nor special, no modifier
        else:
            return 1.0

    
                