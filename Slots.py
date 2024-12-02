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
    
    def removeGame(self, game):
        self.size -= 1
        self.games.remove(game)
        
    def getSize(self):
        return self.size
    
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
    
    def removePractice(self, practice):
        self.size -= 1
        self.practices.remove(practice)
    
    def getSize(self):
        return self.size