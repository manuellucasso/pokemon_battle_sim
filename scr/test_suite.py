from pokemon import Pokemon
from move import Move
from data_loader import MOVES_LIBRARY,typewriter_print
from trainer import Trainer
from battle import Battle

def test_suite(GLOBAL_POKEMON_DATA, GLOBAL_MOVES_LIBRARY):
    typewriter_print("\n--- Sample Trainer Creation ---")
    player1 = Trainer(name = "Manuel",
                      is_ai=False)
    
    typewriter_print("\n--- Sample Pokemon Creation ---")
    
    # Create a sample Pokemon instances 
    pikachu = Pokemon(POKEMON_DATA=GLOBAL_POKEMON_DATA['Pikachu'], level=3, status_conditions=None)   
    typewriter_print(f"\nCreated Pokemon: {pikachu.name}, Level: {pikachu.level}, HP: {pikachu.hp_current}/{pikachu.hp_max}")
    typewriter_print(f"\n--- {pikachu.name} has {pikachu.xp_current} out of {pikachu.xp_max}")

    cartepie=Pokemon(POKEMON_DATA=GLOBAL_POKEMON_DATA['Caterpie'], level=3, status_conditions=None)   
    typewriter_print(f"\nCreated Pokemon: {cartepie.name}, Level: {cartepie.level}, HP: {cartepie.hp_current}/{cartepie.hp_max}")

    gloom=Pokemon(POKEMON_DATA=GLOBAL_POKEMON_DATA['Gloom'], level=3, status_conditions=None)   
    typewriter_print(f"\nCreated Pokemon: {gloom.name}, Level: {gloom.level}, HP: {gloom.hp_current}/{gloom.hp_max}")

    
    # Testing pokemon method by gaining enough XP, we test:
    # gain_xp, level_up, stats_calculator from pokemon class
    # learn_move_by_level_up, learn_move from move_manager class
    typewriter_print("\n--- Pokemon gain XP ---")
    pikachu.gain_xp(27)

    typewriter_print(f"\n--- {pikachu.name} has {pikachu.xp_current} out of {pikachu.xp_max}")

    # Last test for move_manager class
    typewriter_print("\n--- Pokemon is being teach a non teachable TM ---")
    pikachu.move_manager.learn_teach_move("Earthquake")

    typewriter_print("\n--- Pokemon is being teach a teachable TM ---")
    pikachu.move_manager.learn_teach_move("Surf")


    # Test for the trainer class, method:
    # add_pokemon,switch pokemon and move
    typewriter_print(f"\n--- {pikachu.name} was caught by {player1.name} ---")
    player1.add_pokemon(pikachu)

    typewriter_print(f"\n--- {cartepie.name} was caught by {player1.name} ---")
    player1.add_pokemon(cartepie)

    typewriter_print(f"\n--- {gloom.name} was caught by {player1.name} ---")
    player1.add_pokemon(gloom)

    captured_names = ", ".join([p.name for p in player1.pokemons])
    typewriter_print(f"\n{player1.name} has captured {captured_names}")

    typewriter_print(f"\n--- {player1.name}'s first pokemon is {player1.get_active_pokemon().name} ---")

    player1.switch_pokemon()
    typewriter_print(f"\n--- {player1.name}'s is switching his first pokemon to {player1.get_active_pokemon().name} ---")

    player1.choose_move()

    # --- Testing Battle System ---
    typewriter_print("\n--- Opponent Trainer Creation ---")
    # We'll create a rival for Manuel to test the Battle class
    rival = Trainer(name="Rival Gary", is_ai=True)

    # Create a Pokemon for the rival
    # Let's give him a Squirtle to test Type Advantages (Electric vs Water)
    squirtle = Pokemon(POKEMON_DATA=GLOBAL_POKEMON_DATA['Squirtle'], level=5, status_conditions=None)
    rival.add_pokemon(squirtle)
    
    # Give him another one to test the handle_faint method
    pidgey = Pokemon(POKEMON_DATA=GLOBAL_POKEMON_DATA['Pidgey'], level=4, status_conditions=None)
    rival.add_pokemon(pidgey)

    typewriter_print(f"\n{rival.name} enters the battle with {squirtle.name} and {pidgey.name}!")
   
    typewriter_print("\n" + "="*30)
    typewriter_print("      STARTING BATTLE TEST")
    typewriter_print("="*30)
    
    # Initialize the battle instance
    poke_battle = Battle(trainer1=player1, trainer2=rival)
    
    # This will run the turn-based loop until someone wins
    # It will test: get_battle_action, run_turn, execute_attack, 
    # bonus_type (STAB/Effectiveness), and handle_faint.
    poke_battle.start()

    typewriter_print("\n--- Test Suite Completed Successfully ---")