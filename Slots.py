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
    
    def removeGame(self, game):
        self.size -= 1
        self.games.remove(game)
        
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
    
    def removePractice(self, practice):
        self.size -= 1
        self.practices.remove(practice)
    
    def getSize(self):
        return len(self.practices)