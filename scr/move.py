import csv
import os

class Move:
    """
    Represents a combat move with specific properties for damage calculation and battle mechanics.
    """
    def __init__(self, name, move_type, power, accuracy, pp, category,effect):
        """
        Initializes a Move instance.
        
        Args:
            name (str): The name of the move.
            move_type (str): Elemental type (e.g., 'Fire', 'Water').
            power (int): Base damage value.
            accuracy (int): Chance to hit (0-100).
            pp (int): Power Points (number of times the move can be used).
            category (str): Damage category ('Physical' or 'Special').
            effect (str): The effect of the move (e.g., 'Burn', 'Paralyze').
        """
        self.name = name
        self.type = move_type
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.category = category
        self.effect = effect

    @staticmethod      
    def get_all_moves(data_dir):    
        """
        Retrieves all moves from the provided library.
        """
        
        moves_file = os.path.join(data_dir, 'move_set.csv')
        moves_dict = {}
        try:
            with open(moves_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Instantiate a Move object for each entry in the CSV
                    new_move = Move(
                        name=row['move_name'],
                        move_type=row['type'],
                        power=row['power'],
                        accuracy=row['accuracy'],
                        pp=row['pp'],
                        category=row['category'],
                        effect=row['effect']
                    )

                    # Store the move object in the dictionary for quick access
                    moves_dict[row['move_name']] = new_move
        except FileNotFoundError:
            print("Error: move_set.csv not found.")
            
        return moves_dict