from pokemon import Pokemon
from move import Move
from data_loader import MOVES_LIBRARY
from trainer import Trainer

def test_suite(GLOBAL_POKEMON_DATA, GLOBAL_MOVES_LIBRARY):
    print("\n--- Sample Trainer Creation ---")
    player1 = Trainer(name = "Manuel",
                      is_ai=False)
    
    print("\n--- Sample Pokemon Creation ---")
    
    # Create a sample Pokemon instances 
    pikachu = Pokemon(POKEMON_DATA=GLOBAL_POKEMON_DATA['Pikachu'], level=3, status_conditions=None)   
    print(f"\nCreated Pokemon: {pikachu.name}, Level: {pikachu.level}, HP: {pikachu.hp_current}/{pikachu.hp_max}")
    print(f"\n--- {pikachu.name} has {pikachu.xp_current} out of {pikachu.xp_max}")

    cartepie=Pokemon(POKEMON_DATA=GLOBAL_POKEMON_DATA['Caterpie'], level=3, status_conditions=None)   
    print(f"\nCreated Pokemon: {cartepie.name}, Level: {cartepie.level}, HP: {cartepie.hp_current}/{cartepie.hp_max}")

    gloom=Pokemon(POKEMON_DATA=GLOBAL_POKEMON_DATA['Gloom'], level=3, status_conditions=None)   
    print(f"\nCreated Pokemon: {gloom.name}, Level: {gloom.level}, HP: {gloom.hp_current}/{gloom.hp_max}")

    
    # Testing pokemon method by gaining enough XP, we test:
    # gain_xp, level_up, stats_calculator from pokemon class
    # learn_move_by_level_up, learn_move from move_manager class
    print("\n--- Pokemon gain XP ---")
    pikachu.gain_xp(27)

    print(f"\n--- {pikachu.name} has {pikachu.xp_current} out of {pikachu.xp_max}")

    # Last test for move_manager class
    print("\n--- Pokemon is being teach a non teachable TM ---")
    pikachu.move_manager.learn_teach_move("Earthquake")

    print("\n--- Pokemon is being teach a teachable TM ---")
    pikachu.move_manager.learn_teach_move("Surf")


    # Test for the trainer class, method:
    # add_pokemon,switch pokemon and move
    print(f"\n--- {pikachu.name} was caught by {player1.name} ---")
    player1.add_pokemon(pikachu)

    print(f"\n--- {cartepie.name} was caught by {player1.name} ---")
    player1.add_pokemon(cartepie)

    print(f"\n--- {gloom.name} was caught by {player1.name} ---")
    player1.add_pokemon(gloom)

    captured_names = ", ".join([p.name for p in player1.pokemons])
    print(f"\n{player1.name} has captured {captured_names}")

    print(f"\n--- {player1.name}'s first pokemon is {player1.get_active_pokemon().name} ---")

    player1.switch_pokemon()
    print(f"\n--- {player1.name}'s is switching his first pokemon to {player1.get_active_pokemon().name} ---")

    player1.choose_move()