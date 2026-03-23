import random
from data_loader import MOVES_LIBRARY, typewriter_print

class BattleEffectsMixin:
    def attack_effect(self, move_data, attacker, defender,final_damage):
            """
            Comprehensive effect interpreter for the move_set.csv database.
            """
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
            if "halves current HP" in effect:
                try:
                    defender.hp_current = int(defender.hp_current/2)
                    typewriter_print(f"It dealt a half HP damage!")
                except ValueError: pass

            if "fixed" in effect and "damage" in effect:
                # Extract number from string like "fixed 40 damage"
                try:
                    fixed_dmg = int(''.join(filter(str.isdigit, effect)))
                    defender.hp_current = max(0, defender.hp_current - fixed_dmg)
                    typewriter_print(f"It dealt a fixed {fixed_dmg} damage!")
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
                typewriter_print(f"Hit {hits} times!")
                return hits

            # --- 3. RECOIL & SELF-DAMAGE (Ex: User takes recoil, Recoil damage) ---
            elif "recoil" or "self-damage"in effect:
                # Usually 1/4 or 1/3 of damage dealt, let's use a flat 15% for now
                recoil = attacker.hp_max // 6 
                attacker.hp_current = max(0, attacker.hp_current - recoil)
                typewriter_print(f"{attacker.name} was hit with recoil damage!")

            elif "faints" in effect:
                # attacker faints
                attacker.hp_current = 0
                typewriter_print(f"{attacker.name} fainted!")    

            # --- 4. ONE-HIT KO (Ex: One-hit KO) ---
            elif "one-hit ko" in effect:
                # Accuracy check usually handled before, but if it hits:
                defender.hp_current = 0
                typewriter_print("It's a One-Hit KO!")

            # --- 5. STAT SHARP CHANGES (Ex: Sharply raise Defense) ---
            elif "sharply" in effect:
                stat = ""
                if "attack" in effect: stat = "Attack"
                elif "defense" in effect: stat = "Defense"
                elif "speed" in effect: stat = "Speed"
                elif "special" in effect: stat = "Special"
                
                if "raise" in effect:
                    attacker.stats[stat] = int(attacker.stats[stat] * 2.0)
                    typewriter_print(f"{attacker.name}'s {stat} rose sharply!")
                elif "lower" in effect:
                    defender.stats[stat] = int(defender.stats[stat] * 0.5)
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
                            attacker.stats[stat] = int(attacker.stats[stat] * 1.5)
                        typewriter_print(f"{attacker.name}'s {stat} rose!")
                        
                    elif "lower" in effect:
                        if stat in defender.stats:
                            defender.stats[stat] = int(defender.stats[stat] * 0.75)
                        typewriter_print(f"{defender.name}'s {stat} fell!")
                
                # Handle Accuracy and Evasion using your Flag System
                elif stat in ["Accuracy", "Evasion"]:
                    if "raise" in effect:
                        typewriter_print(f"{attacker.name}'s {stat} rose!")
                        flag = f"raise_{stat.lower()}"
                        return flag, 1.1 
                    
                    elif "lower" in effect:
                        typewriter_print(f"{defender.name}'s {stat} fell!")
                        flag = f"lower_{stat.lower()}"
                        return flag, 0.9        

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
                                    defender.stats[stat_name] = int(defender.stats[stat_name] * 0.8)
                                    typewriter_print(f"{defender.name}'s {stat_name} fell!")
                        elif "flinch" in effect:
                            typewriter_print(f"{defender.name} flinched!")
                            # You'll need a 'flinched' flag in your Battle turn logic
                            flag = "flinch"
                            return flag


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
                heal = final_damage*0.5
                attacker.hp_current = min(attacker.hp_max, attacker.hp_current + heal)
                typewriter_print(f"{attacker.name} absorbed energy!")


            # --- 9. UNIQUE BATTLE UTILITY ---
            
            # Never misses (Ex: Never misses)
            if "never misses" in effect:
                typewriter_print(f"{attacker.name}'s attack cannot be evaded!")

            # Force switch (Ex: Force switch)
            elif "force switch" in effect:
                typewriter_print(f"{defender.name} was forced to flee!")
                self.handle_faint(self.t2 if defender == self.t2.get_active_pokemon() else self.t1)

            # Reset stats (Ex: Reset stats)
            elif "reset stats" in effect:
                # We would need to store base_stats, for now we reset to current dictionary's base
                attacker.stats = attacker.stats_calculator(attacker.level, attacker.initial_stats)
                defender.stats = defender.stats_calculator(defender.level, defender.initial_stats)
                typewriter_print("All stat changes were eliminated!")

            # Protects stats (Ex: Protects stats)
            elif "protects stats" in effect:
                typewriter_print(f"{attacker.name} is protected from stat reduction!")

            # Changes user type (Ex: Changes user type to target)
            elif "changes user type" in effect:
                attacker.types = defender.types.copy()
                typewriter_print(f"{attacker.name} transformed into {defender.types} type!")

            # --- 10. ADVANCED DAMAGE LOGIC ---

            # High critical ratio (Ex: High critical ratio)
            if "high critical ratio" in effect:
                typewriter_print("It has a high critical hit ratio!")
                flag="highCrit"
                return flag

            # Fixed Damage (Ex: Fixed level damage)
            elif "fixed level damage" in effect:
                dmg = attacker.level
                defender.hp_current = max(0, defender.hp_current - dmg)
                typewriter_print(f"It dealt {dmg} damage based on level!")
                flag="fixed_damage"
                return flag

            # Variable damage (Ex: Variable damage)
            elif "variable damage" in effect:
                typewriter_print("The power of this move fluctuates!")
                flag = "variable_damage"
                return flag
            
            elif "double damage if hit" in effect:
                flag = "double_at_hit"
                return flag

            # Self-damage on miss (Ex: Self-damage on miss)
            elif "self-damage on miss" in effect:
                typewriter_print("If this move misses, the user will take damage!")
                flag = "self_on_miss"
                return flag

            # Recoil/Endure (Ex: Endure 2 turns and recoil)
            elif "endure" in effect and "recoil" in effect:
                typewriter_print(f"{attacker.name} is enduring the hit but took recoil!")
                attacker.hp_current = max(1, attacker.hp_current - (attacker.hp_max // 4))

            # --- 11. TURN MANAGEMENT MESSAGES ---

            # Recharge/2-Turn (Ex: 1-turn recharge, 2-turn move)
            if "recharge" in effect or "2-turn" in effect:
                typewriter_print(f"{attacker.name} needs to prepare or recharge for this move!")
                flag = "TurnCharge"
                return flag,2

            # Traps (Ex: Traps for 2-5 turns)
            elif "traps" in effect:
                trap_turns = random.randint(2, 5) 
                flag = "is_traped"
                typewriter_print(f"{defender.name} is trapped and cannot switch!")
                return flag,trap_turns


            # Disable/Disable last move
            elif "disable" in effect:
                typewriter_print(f"{defender.name}'s last move was disabled!")

            # --- 12. SPECIAL DEFENSIVE/OFFENSIVE ---

            # Steals HP (Ex: Steals HP each turn)
            if "steals hp" in effect:
                flag = "stealsHP"
                typewriter_print(f"{defender.name} is being seeded!")
                return flag

            # Halve Special damage (Ex: Halve special damage)
            elif "halve special damage" in effect:
                typewriter_print("A special barrier protects the team!")
                flag = "halve_special"
                return flag
            
            # Halve Physical damage (Ex: Halve Physical damage)
            elif "halve physical damage" in effect:
                typewriter_print("A special barrier protects the team!")
                flag = "halve_physical"
                return flag

            # Random/Copy Move (Ex: Uses random move, Copies last move)
            elif "random move" in effect:
                typewriter_print(f"{attacker.name} is attempting a random effect!")
                flag = "random_move" 
                return flag
            
            elif "copies last" in effect:
                typewriter_print(f"{attacker.name} is attempting to copy the move!")
                flag = "copy_move"  
                return flag 

            elif "confuses user after" in effect:
                typewriter_print(f"{attacker.name} is confused!")
                attacker.status_conditions = "CONF"  
