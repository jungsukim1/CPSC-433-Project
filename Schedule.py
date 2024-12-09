from Slots import GameSlot, PracticeSlot

class Schedule:
    # Schedule represents a collection of game and practice slots.

    def __init__(self, gameslots, practiceslots):
        # Initialize with a list of game slots and practice slots.
        self.gameslots = gameslots
        self.practiceslots = practiceslots
        self.eval = 0  # Evaluation score (not yet calculated here)
    
    def getTotalGames(self):
        # Returns the total number of games scheduled in the game slots.
        total = 0
        for slot in self.gameslots:
            total += slot.size  # Sum the number of games in each game slot
        return total
    
    def getTotalPractices(self):
        # Returns the total number of practices scheduled in the practice slots.
        total = 0
        for slot in self.practiceslots:
            total += slot.size  # Sum the number of practices in each practice slot
        return total
    
    def addGameSlot(self, gameslot):
        # Add a game slot to the schedule if it's a valid GameSlot instance.
        if not isinstance(gameslot, GameSlot):
            print("Error wrong data type Game")
            return
        self.gameslots.append(gameslot)  # Add the game slot to the list
    
    def addPracticeSlot(self, practiceslot):
        # Add a practice slot to the schedule if it's a valid PracticeSlot instance.
        if not isinstance(practiceslot, PracticeSlot):
            print("Error wrong data type Practice")
            return
        self.practiceslots.append(practiceslot)  # Add the practice slot to the list
    
    def removeGameSlot(self):
        # Remove the most recently added game slot.
        return self.gameslots.pop()  # Removes and returns the last game slot in the list
        
    def removePracticeSlot(self):
        # Remove the most recently added practice slot.
        return self.practiceslots.pop()  # Removes and returns the last practice slot in the list
        
    def removeSpecificGameSlot(self, gameSlot):
        # Remove a specific game slot if it's found in the list.
        if not isinstance(gameSlot, GameSlot):
            print("Error wrong data type")
            return
        
        self.gameslots.remove(gameSlot)  # Remove the specified game slot
        
    def removeSpecificPracticeSlot(self, practiceSlot):
        # Remove a specific practice slot if it's found in the list.
        if not isinstance(practiceSlot, PracticeSlot):
            print("Error wrong data type")
            return
        self.practiceslots.remove(practiceSlot)  # Remove the specified practice slot

    def printSchedule(self):
        # Print all the game and practice slots in the schedule.
        for i in range(len(self.gameslots)):
            # Print the games, day, and start time for each game slot
            print(self.gameslots[i].games, self.gameslots[i].day, self.gameslots[i].startTime)
            
        for i in range(len(self.practiceslots)):
            # Print the practices, day, and start time for each practice slot
            print(self.practiceslots[i].practices, self.practiceslots[i].day, self.practiceslots[i].startTime)