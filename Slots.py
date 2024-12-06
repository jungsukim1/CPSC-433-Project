import random
class GameSlot:
    
    def __init__(self, max, min, day, startTime):
        self.max = max
        self.min = min
        self.day = day
        self.startTime = startTime
        self.games = set()
        self.size = 0

    def addGame(self, game):
        self.size += 1
        self.games.add(game)
    
    def removeGame(self): #the purpose of the random popping is to make sure the game removed is random
        if self.size == 1:
            self.size -= 1
            return self.games.pop()
        
        element = random.choice(list(self.games))
        self.games.remove(element)
        self.size -= 1
        
        return element
        
    def getSize(self):
        return len(self.games)
    
    def getMin(self):
        return self.min
    
class PracticeSlot:
    
    def __init__(self, max, min, day, startTime):
        self.max = max
        self.min = min
        self.day = day
        self.startTime = startTime
        self.practices = set()
        self.size = 0

    def addPractice(self, practice):
        self.size += 1
        self.practices.add(practice)
    
    def removePractice(self):
        if self.size == 1:
            self.size -= 1
            return self.practices.pop()
        
        element = random.choice(list(self.practices))
        self.practices.remove(element)
        self.size -= 1
        
        return element
    
    def getSize(self):
        return len(self.practices)
    
    def getMin(self):
        return self.min