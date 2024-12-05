from Slots import GameSlot, PracticeSlot

class Schedule:
    def __init__(self):
        self.totalGames = 0
        self.totalPractices = 0
        self.gameslots = []
        self.practiceslots = []
        self.eval = 0
        
    def addGameSlot(self,gameslot):
        if not isinstance(gameslot, GameSlot):
            print("Error wrong data type Game")
            return
    
        self.totalGames += gameslot.size
        self.gameslots.append(gameslot)
    
    def addPracticeSlot(self,practiceslot):
        if not isinstance(practiceslot, PracticeSlot):
            print("Error wrong data type Practice")
            return
    
        self.totalPractices += practiceslot.size
        self.practiceslots.append(practiceslot)
        
    def getTotalGames(self):
        return self.totalGames
    
    def getTotalPractices(self):
        return self.totalPractices
    
    def removeGameSlot(self):
        self.totalGames -= 1
        return self.gameslots.pop()
        
    def removePracticeSlot(self):
        self.totalPractices -= 1
        return self.practiceslots.pop()
        
    def removeSpecificGameSlot(self,gameSlot):
        if not isinstance(gameSlot, GameSlot):
            print("Error wrong data type")
            return
        
        # if gameSlot in self.gameslots:
        self.gameslots.remove(gameSlot)
        self.totalGames -= 1
        
    def removeSpecficPracticeSlot(self,practiceSlot):
        if not isinstance(practiceSlot, PracticeSlot):
            print("Error wrong data type")
            return
        # if practiceSlot in self.practiceslots:
        self.practiceslots.remove(practiceSlot)
        self.totalPractices -= 1