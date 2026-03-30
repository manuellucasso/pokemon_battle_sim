import random
from data_loader import MOVES_LIBRARY, typewriter_print

class BattleEffectsMixin:
    
    @staticmethod
    def attack_effect(move_name, attacker, defender,final_damage):
            """
            Comprehensive effect interpreter for the move_set.csv database.
            """
            move_data = MOVES_LIBRARY.get(move_name)
            if not move_data:
                return

            effect = str(move_data.effect).lower()
            if effect in ['nan', 'no effect','none']:
                return

            # --- 0. STATUS CONDITIONS (Uses the existing 'status' attribute) ---
            status_map = {
                "causes paralysis": "PAR",
                "causes sleep": "SLP",
                "causes poison": "PSN",
                "severe poison": "PSN",
                "causes burn": "BRN",
                "causes confusion": "CONF"
            }

            # Direct status application
            for key, code in status_map.items():
                if key in effect:
                    if not defender.status_conditions: # Only if not already afflicted
                        defender.status_conditions = code
                        typewriter_print(f"{defender.name} is now {code}!")
            
            # Chance-based status (Ex: 10% chance freeze)
            if "% chance" in effect:
                try:
                    chance = int(effect.split('%')[0])
                    if random.randint(1, 100) <= chance:
                        if "paralyze" in effect: 
                            defender.status_conditions = "PAR"
                            typewriter_print(f"{defender.name} was paralyzed!")
                        elif "burn" in effect: 
                            defender.status_conditions = "BRN"
                            typewriter_print(f"{defender.name} was burned!")
                        elif "freeze" in effect: 
                            defender.status_conditions = "FRZ"
                            typewriter_print(f"{defender.name} was frozen solid!")
                        elif "confuse" in effect: 
                            defender.status_conditions = "CONF"
                            typewriter_print(f"{defender.name} became confused!")
                        elif "sleep" in effect:
                            defender.status_conditions = "SLP"  
                            typewriter_print(f"{defender.name} is sleeping!")
                        elif "freeze" in effect:
                            typewriter_print(f"{defender.name} was frozen!")
                            defender.status_conditions = "FRZ"        
                except: pass



            # --- 1. FIXED DAMAGE (Ex: Fixed 40 damage, Fixed 20 damage) ---
            elif "halves current HP" in effect:
                try:
                    damage = int(defender.hp_current/2)
                    flag = "fixed_damage"
                    return flag,damage 
                except ValueError: pass

            elif "fixed" in effect and "damage" in effect:
                # Extract number from string like "fixed 40 damage"
                try:
                    fixed_dmg = int(''.join(filter(str.isdigit, effect)))
                    flag = "fixed_damage"
                    return flag,fixed_dmg                     
                except ValueError: pass    

            # --- 2. MULTI-HIT MOVES (Ex: Hits 2-5 times, Hits twice) ---
            elif "hits" in effect:
                if "2-5" in effect:
                    hits = random.randint(2, 5)
                elif "twice" in effect:
                    hits = 2
                else: hits = 1
                
                # Note: The first hit already happened in execute_attack. 
                # This logic would actually need to move into the damage loop 
                # for full accuracy, but as an effect:
                flag = "multi_hits"
                return flag, hits

            # --- 3. RECOIL & SELF-DAMAGE (Ex: User takes recoil, Recoil damage) ---
            elif "recoil" in effect or "self-damage"in effect:
                flag = "self_damage"
                return flag

            elif "faints" in effect:
                # attacker faints
                flag = "faint"
                return flag    

            # --- 4. ONE-HIT KO (Ex: One-hit KO) ---
            elif "one-hit ko" in effect:
                flag = "one_ko"
                return flag

            # --- 5. STAT SHARP CHANGES (Ex: Sharply raise Defense) ---
            elif "sharply" in effect:
                stat = ""
                if "attack" in effect: stat = "Attack"
                elif "defense" in effect: stat = "Defense"
                elif "speed" in effect: stat = "Speed"
                elif "special" in effect: stat = "Special"
                
                if "raise" in effect:
                    attacker.stats[stat] = int(attacker.stats[stat] * 1.2)
                    typewriter_print(f"{attacker.name}'s {stat} rose sharply!")
                elif "lower" in effect:
                    if defender.stats_protected:
                        typewriter_print(f"{defender.name} is protected from stat reduction!")
                        defender.stats[stat] = int(defender.stats[stat] * 1.0)  # No change
                    else:
                        defender.stats[stat] = int(defender.stats[stat] * 0.8)
                        typewriter_print(f"{defender.name}'s {stat} fell sharply!")


            # --- 5.5. NORMAL STAT CHANGES (Ex: Raise Attack, Lower Defense, Lower accuracy) ---
            elif ("raise" in effect or "lower" in effect) and "sharply" not in effect and "% chance" not in effect:
                stat = ""
                
                # Identify which stat is being targeted
                if "attack" in effect: stat = "Attack"
                elif "defense" in effect: stat = "Defense"
                elif "speed" in effect: stat = "Speed"
                elif "special" in effect: stat = "Special"
                elif "accuracy" in effect: stat = "Accuracy"
                elif "evasion" in effect: stat = "Evasion"
                
                # Handle regular stats directly in the dictionary
                if stat in ["Attack", "Defense", "Speed", "Special"]:
                    if "raise" in effect:
                        if stat in attacker.stats:
                            attacker.stats[stat] = int(attacker.stats[stat] * 1.1)
                        typewriter_print(f"{attacker.name}'s {stat} rose!")
                        
                    elif "lower" in effect:
                        if defender.stats_protected:
                            typewriter_print(f"{defender.name} is protected from stat reduction!")
                            defender.stats[stat] = int(defender.stats[stat] * 1.0)  # No change
                        else:
                            if stat in defender.stats:
                                defender.stats[stat] = int(defender.stats[stat] * 0.9)
                                typewriter_print(f"{defender.name}'s {stat} fell!")
                
                # Handle Accuracy and Evasion using your Flag System
                elif stat in ["Accuracy", "Evasion"]:
                    if "raise" in effect:
                        typewriter_print(f"{attacker.name}'s {stat} rose!")
                        flag = f"{stat.lower()}_multiplier"
                        current_value = getattr(attacker, flag)
                        setattr(attacker, flag, current_value * 1.1)
                          
                    
                    elif "lower" in effect:
                        if defender.stats_protected:
                            typewriter_print(f"{defender.name} is protected from stat reduction!")
                            flag = f"{stat.lower()}_multiplier"
                            current_value = getattr(defender, flag)
                            setattr(defender, flag, current_value * 1.0)  # No change
                        else:   
                            typewriter_print(f"{defender.name}'s {stat} fell!")
                            flag = f"{stat.lower()}_multiplier"
                            current_value = getattr(defender, flag)
                            setattr(defender, flag, current_value * 0.9)
                            

            # --- 6. PROBABILITY EFFECTS (Ex: 10% chance lower Defense) ---
            elif "% chance" in effect:
                try:
                    chance = int(effect.split('%')[0])
                    if random.randint(1, 100) <= chance:
                        if "lower" in effect:
                            # Logic to identify which stat to lower
                            for s in ["attack", "defense", "speed", "special"]:
                                if s in effect:
                                    stat_name = s.capitalize()
                                    if defender.stats_protected:
                                        typewriter_print(f"{defender.name} is protected from stat reduction!")
                                        defender.stats[stat_name] = int(defender.stats[stat_name] * 1.0)  # No change
                                    else:
                                        defender.stats[stat_name] = int(defender.stats[stat_name] * 0.9)
                                        typewriter_print(f"{defender.name}'s {stat_name} fell!")
                        elif "flinch" in effect:
                            typewriter_print(f"{defender.name} flinched!")
                            defender.is_flinching = True

                except: pass

            # --- 7. HEALING (Ex: Heal 50% HP) ---
            elif "heal" in effect and "50%" in effect:
                heal = int(attacker.hp_max // 2)
                attacker.hp_current = min(attacker.hp_max, attacker.hp_current + heal)
                typewriter_print(f"{attacker.name} regained health!")

            elif "heal" in effect and "sleep" in effect:
                heal = int(attacker.hp_max // 2)
                attacker.hp_current = min(attacker.hp_max, attacker.hp_current + heal)
                attacker.status_conditions = "SLP"  
                typewriter_print(f"{attacker.name} regained health and slept!\n")
                typewriter_print(f"{attacker.name} is sleeping!\n")    

            # --- 8. ABSORB/DRAIN (Ex: Recover 50% damage) ---
            elif "recover" in effect and "damage" in effect:
                # This would need the damage_dealt value from execute_attack
                # For now, a simple estimation:
                heal = int(final_damage*0.5)
                attacker.hp_current = min(attacker.hp_max, attacker.hp_current + heal)
                typewriter_print(f"{attacker.name} absorbed energy!")


            # --- 9. UNIQUE BATTLE UTILITY ---
            elif "force switch" in effect:
                flag = "force_switch"
                defender.is_blocked_switch = False
                return flag    

            # Reset stats (Ex: Reset stats)
            elif "reset stats" in effect:
                # We would need to store base_stats, for now we reset to current dictionary's base
                attacker.stats = attacker.stats_calculator(attacker.level, attacker.initial_stats)
                defender.stats = defender.stats_calculator(defender.level, defender.initial_stats)
                typewriter_print("All stat changes were eliminated!")

            # Protects stats (Ex: Protects stats)
            elif "protects stats" in effect:
                flag = "protect_stats"
                number_of_turns = 5 # Default to 5 turns if not specified
                if "for" in effect:
                    try:
                        number_of_turns = int(effect.split("for")[1].split("turn")[0].strip())
                    except: pass   
                return flag,number_of_turns

            # Changes user type (Ex: Changes user type to target)
            elif "changes user type" in effect:
                attacker.types = defender.types.copy()
                typewriter_print(f"{attacker.name} transformed into {defender.types} type!")

            elif "escape" in effect:
                flag = "escape"
                return flag    

            # --- 10. ADVANCED DAMAGE LOGIC ---

            # High critical ratio (Ex: High critical ratio)
            elif "high critical ratio" in effect:
                flag="high_crit"
                return flag

            # Fixed Damage (Ex: Fixed level damage)
            elif "fixed level damage" in effect:
                dmg = attacker.level
                flag="fixed_damage"
                return flag,dmg

            # Variable damage (Ex: Variable damage)
            elif "variable damage" in effect:
                flag = "variable_damage"
                return flag
            
            elif "double damage if hit" in effect:
                flag = "double_at_hit"
                return flag

            # Self-damage on miss (Ex: Self-damage on miss)
            elif "self-damage on miss" in effect:
                flag = "self_on_miss"
                return flag

            # Recoil/Endure (Ex: Endure 2 turns and recoil)
            elif "endure" in effect and "recoil" in effect:
                typewriter_print(f"{attacker.name} started to store energy!")
                attacker.bide_turns = 2

            # --- 11. TURN MANAGEMENT MESSAGES ---

            # Recharge (Ex: 1-turn recharge)
            elif "recharge" in effect:
                typewriter_print(f"{attacker.name} needs to recharge for this move!")
                attacker.is_recharging = True
                attacker.charge_turns = 2

            elif "2-turn" in effect:
                typewriter_print(f"{attacker.name} needs to prepare for this move!")
                attacker.is_preparing = True
                attacker.charge_turns = 2
                flag = "preparing"
                if "invulnerable" in effect:
                    attacker.is_hidden = True
                return flag
                    
            # Traps (Ex: Traps for 2-5 turns)
            elif "traps" in effect:
                trap_turns = random.randint(2, 5) 
                typewriter_print(f"{defender.name} is trapped and cannot switch!")
                if defender.trap_turns == 0: 
                    defender.trap_turns = trap_turns 


            # Disable/Disable last move
            #elif "disable" in effect:
            #    typewriter_print(f"{defender.name}'s last move was disabled!")

            #put effect that creates a decoy here (Ex: Creates a decoy that takes the next hit)

            # --- 12. SPECIAL DEFENSIVE/OFFENSIVE ---

            # Steals HP (Ex: Steals HP each turn)
            elif "steals hp" in effect:
                typewriter_print(f"{defender.name} is being seeded!")
                if defender.is_seeded == False: 
                    defender.is_seeded = True
                else:
                    typewriter_print(f"{defender.name} is already seeded!")     

            # Halve Special damage (Ex: Halve special damage)
            elif "halve special damage" in effect:
                flag = "halve_special"
                number_of_turns = 5 # Default to 5 turns if not specified
                if "for" in effect:
                    try:
                        number_of_turns = int(effect.split("for")[1].split("turn")[0].strip())
                    except: pass   
                return flag,number_of_turns
            
            # Halve Physical damage (Ex: Halve Physical damage)
            elif "halve physical damage" in effect:
                flag = "halve_physical"
                number_of_turns = 5 # Default to 5 turns if not specified
                if "for" in effect:
                    try:
                        number_of_turns = int(effect.split("for")[1].split("turn")[0].strip())
                    except: pass   
                return flag,number_of_turns

            elif "confuses user after" in effect:
                typewriter_print(f"{attacker.name} is confused!")
                attacker.status_conditions = "CONF"  



