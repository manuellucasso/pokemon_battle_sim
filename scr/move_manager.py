import random
import copy
from data_loader import MOVES_LIBRARY



class MoveManager:
    def __init__(self, pokemon_name, pokemon_level,pokemon_lvl_up_moves,pokemon_teach_moves):
        self.pokemon_name = pokemon_name
        self.pokemon_level = pokemon_level
        self.pokemon_lvl_up_moves = pokemon_lvl_up_moves
        self.pokemon_teach_moves = pokemon_teach_moves

        self.active_moves = []
        self.active_moves = self.initial_move_set()

        # Dynamic PP management using dictionaries
        self.max_pp = {name: int(MOVES_LIBRARY[name].pp) for name in self.active_moves if name in MOVES_LIBRARY}
        self.current_pp = {name: int(MOVES_LIBRARY[name].pp) for name in self.active_moves if name in MOVES_LIBRARY}

        
    def initial_move_set(self):
        """
        Initializes the Pokemon's move set based on its level and a provided move list.
        """

        # Available moves at the current level
        available_moves = [m['move_name'] for m in self.pokemon_lvl_up_moves if m['level'] is not None and m['level'] <= self.pokemon_level]
        
        # Get the 6th strongest moves from the available moves
        initial_moves = available_moves[-6:]

        # If there are more than 6 moves, randomly select 4 from the last 6
        if len(initial_moves) > 4:
            return random.sample(initial_moves, 4)          

        return initial_moves 


    def learn_move(self, move_name):
        """
        Handles move learning logic by lvl up, including the 4-move limit replacement.
        """
        if len(self.active_moves) < 4:
            self.active_moves.append(move_name)
            print(f"\n{self.pokemon_name} learned {move_name}!")
        else:
            print(f"\n{self.pokemon_name} can't learn {move_name} because it already knows 4 moves.")
            print(f"\n{self.pokemon_name} may forget a move to learn {move_name}.")
            print("\nDo you want to forget a move? (yes/no)")
            
            choice = input().lower()
            if choice == 'yes':
                print("Which move do you want to forget (1-4)?")
                for i, m in enumerate(self.active_moves, 1):
                    print(f"[{i}] {m}")

                move_to_forget = int(input()) - 1

                if 0 <= move_to_forget < len(self.active_moves):
                    forgotten_move = self.active_moves.pop(move_to_forget)
                    del self.max_pp[forgotten_move] # Remove the forgotten move from PP dict
                    del self.current_pp[forgotten_move]
                    self.active_moves.insert(move_to_forget, move_name)
                    print(f"1, 2, 3 and... Done! {self.pokemon_name} forgot {forgotten_move} and learned {move_name}!")    
                else:
                    print("Invalid choice. No move was forgotten.") 
            else:
                print(f"\n{self.pokemon_name} didn't learn {move_name}") 

        # Update the dictionary of pp    
        self.max_pp[move_name] = int(MOVES_LIBRARY[move_name].pp)
        self.current_pp[move_name] = int(MOVES_LIBRARY[move_name].pp)                    


    def learn_teach_move(self, move_name):
        """
        Handles move learning logic by TM/HM teaching, including the 4-move limit replacement.
        """
        
        if move_name not in self.pokemon_teach_moves:
            print(f"\n{self.pokemon_name} cannot learn {move_name} because it's not in the teachable move list.")
            return  
        else:
            self.learn_move(move_name)


    def learn_move_by_level_up(self, new_level):
        """
        Checks for new moves available at the new level and handles learning them.
        """
        self.pokemon_level = new_level
        for move in self.pokemon_lvl_up_moves:
            if move['level'] == new_level:
                self.learn_move(move['move_name'])


    def spend_pp(self, move_name):
        """
        Decrements the current PP of a specific move.
        Returns True if the move was used successfully, 
        False if there was no PP left.
        """
        if move_name in self.current_pp:
            if self.current_pp[move_name] > 0:
                self.current_pp[move_name] -= 1
                return True
            else:
                print(f"{move_name} has no PP left!")
                return False
        else:
            print(f"Error: {self.pokemon_name} does not know {move_name}.")
            return False            