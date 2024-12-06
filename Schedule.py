from Slots import GameSlot, PracticeSlot

class Schedule:
    def __init__(self,gameslots,practiceslots):
        self.gameslots = gameslots
        self.practiceslots = practiceslots
        self.eval = 0
    
    def getTotalGames(self):
        total = 0
        for slot in self.gameslots:
            total += slot.size
        return total
    
    def getTotalPractices(self):
        total = 0
        for slot in self.practiceslots:
            total += slot.size
        return total
    
    def addGameSlot(self,gameslot):
        if not isinstance(gameslot, GameSlot):
            print("Error wrong data type Game")
            return

        self.gameslots.append(gameslot)
    
    def addPracticeSlot(self,practiceslot):
        if not isinstance(practiceslot, PracticeSlot):
            print("Error wrong data type Practice")
            return
    
        self.practiceslots.append(practiceslot)
    
    def removeGameSlot(self):
        return self.gameslots.pop()
        
    def removePracticeSlot(self):
        return self.practiceslots.pop()
        
    def removeSpecificGameSlot(self,gameSlot):
        if not isinstance(gameSlot, GameSlot):
            print("Error wrong data type")
            return
        
        # if gameSlot in self.gameslots:
        self.gameslots.remove(gameSlot)
        
    def removeSpecficPracticeSlot(self,practiceSlot):
        if not isinstance(practiceSlot, PracticeSlot):
            print("Error wrong data type")
            return
        # if practiceSlot in self.practiceslots:
        self.practiceslots.remove(practiceSlot)

    def printSchedule(self):
        for i in range(0,len(self.gameslots)):
            print(self.gameslots[i].games, self.gameslots[i].day, self.gameslots[i].startTime)
            
        for i in range(0,len(self.practiceslots)):
            print(self.practiceslots[i].practices, self.practiceslots[i].day, self.practiceslots[i].startTime)
        