from Slots import GameSlot, PracticeSlot

class Schedule:
    def __init__(self):
        self.totalGames = 0
        self.totalPractices = 0
        self.gameslots = []
        self.practiceslots = []
        
    def addGameSlot(self,gameslot):
        if gameslot is not GameSlot:
            print("Error wrong data type")
            return
    
        self.totalGames += gameslot.size
        self.gameslots.append(gameslot)
    
    def addPracticeSlot(self,practiceslot):
        if practiceslot is not PracticeSlot:
            print("Error wrong data type")
            return
    
        self.totalPractices += practiceslot.size
        self.gameslots.append(practiceslot)
        
    def getTotalGames(self):
        return self.totalGames
    
    def getTotalPractices(self):
        return self.totalPractices
    
    def removeGameSlot(self):
        self.gameslots.pop()
        self.totalGames -= 1
        
    def removePracticeSlot(self):
        self.practiceslots.pop()
        self.totalPractices -= 1
        
    def removeSpecificGameSlot(self,gameSlot):
        if gameSlot is not GameSlot:
            print("Error wrong data type")
            return
        
        self.gameslots.remove(gameSlot)
        self.totalGames -= 1
        
    def removeSpecficPracticeSlot(self,practiceSlot):
        if practiceSlot is not PracticeSlot:
            print("Error wrong data type")
            return
        self.practiceslots.remove(practiceSlot)
        self.totalPractices -= 1