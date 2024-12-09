import random

class GameSlot:
    # GameSlot represents a time slot where games are scheduled.
    
    def __init__(self, max, min, day, startTime):
        self.max = max  # Maximum number of games allowed in this slot
        self.min = min  # Minimum number of games required in this slot
        self.day = day  # Day of the week the game is scheduled (e.g., "Monday")
        self.startTime = startTime  # Start time of the game slot (e.g., "10:00")
        self.games = set()  # Set to store games scheduled in this slot
        self.size = 0  # Current number of games scheduled in this slot

    def addGame(self, game):
        # Add a game to this slot and increase the size
        self.size += 1
        self.games.add(game)
    
    def removeGame(self):
        # Remove a random game from the slot and decrease the size
        if self.size == 1:
            self.size -= 1
            return self.games.pop()  # If only one game, remove and return it
        
        element = random.choice(list(self.games))  # Select a random game to remove
        self.games.remove(element)  # Remove the selected game
        self.size -= 1  # Decrease the size
        return element  # Return the removed game
        
    def getSize(self):
        # Return the number of games currently in the slot
        return len(self.games)
    
    def getMin(self):
        # Return the minimum number of games required in the slot
        return self.min
    
class PracticeSlot:
    # PracticeSlot represents a time slot where practices are scheduled.
    
    def __init__(self, max, min, day, startTime):
        self.max = max  # Maximum number of practices allowed in this slot
        self.min = min  # Minimum number of practices required in this slot
        self.day = day  # Day of the week the practice is scheduled (e.g., "Monday")
        self.startTime = startTime  # Start time of the practice slot (e.g., "10:00")
        self.practices = set()  # Set to store practices scheduled in this slot
        self.size = 0  # Current number of practices scheduled in this slot

    def addPractice(self, practice):
        # Add a practice to this slot and increase the size
        self.size += 1
        self.practices.add(practice)
    
    def removePractice(self):
        # Remove a random practice from the slot and decrease the size
        if self.size == 1:
            self.size -= 1
            return self.practices.pop()  # If only one practice, remove and return it
        
        element = random.choice(list(self.practices))  # Select a random practice to remove
        self.practices.remove(element)  # Remove the selected practice
        self.size -= 1  # Decrease the size
        return element  # Return the removed practice
    
    def getSize(self):
        # Return the number of practices currently in the slot
        return len(self.practices)
    
    def getMin(self):
        # Return the minimum number of practices required in the slot
        return self.min