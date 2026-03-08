import csv

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
    def get_move_set_for_pokemon(pokemon_name, moves_library):    
        """
        Retrieves moves for a specific Pokemon by looking up pre-loaded 
        move objects from the provided library.
        """
        move_set = []
        try:
            with open('pokemon_learnsets.csv', mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['pokemon'] == pokemon_name:
                        move_name = row['move_name']
                        
                        # Get the object from the library (pre-loaded in memory)
                        if move_name in moves_library:
                            m = moves_library[move_name]
                            lvl = int(row['level']) if row['level'] else None
                            move_set.append({'level': lvl, 'move': m})
        except FileNotFoundError:
            print("Error: pokemon_learnsets.csv not found.")
            
        return move_set
    

    @staticmethod      
    def get_all_moves(moves_library):    
        """
        Retrieves all moves from the provided library.
        """
        moves_dict = {}
        try:
            with open('move_set.csv', mode='r', encoding='utf-8') as f:
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