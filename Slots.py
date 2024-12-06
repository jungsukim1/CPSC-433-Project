import random
class GameSlot:
    
    def __init__(self, max, min, day, startTime):
        self.max = max
        self.min = min
        self.day = day
        self.startTime = startTime
        self.games = set()
        self.size = 0
        self.triedGames = set()

    def addGame(self, game):
        self.size += 1
        self.games.add(game)
    
    def removeGame(self): #the purpose of the random popping is to make sure the game removed is random
        if self.size == 1:
            self.size -= 1
            return self.games.pop()
        
        for x in range(random.randint(1,self.size)):
            temp = self.games.pop()
            self.games.add(temp)
        self.size -= 1
        return self.games.pop()
        
    def getSize(self):
        return len(self.games)
    
class PracticeSlot:
    
    def __init__(self, max, min, day, startTime):
        self.max = max
        self.min = min
        self.day = day
        self.startTime = startTime
        self.practices = set()
        self.size = 0
        self.triedPractices = set()

    def addPractice(self, practice):
        self.size += 1
        self.practices.add(practice)
    
    def removePractice(self):
        if self.size == 1:
            self.size -= 1
            return self.practices.pop()
        
        for x in range(random.randint(1,self.size)):
            temp = self.practices.pop()
            self.practices.add(temp)
        self.size -= 1
        return self.practices.pop()
    
    def getSize(self):
        return len(self.practices)