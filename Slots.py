class GameSlot:
    
    def __init__(self, max, min, day, startTime):
        self.max = max
        self.min = min
        self.day = day
        self.startTime = startTime
        self.games = set()

    def addGame(self, game):
        self.games.add(game)
    
    def removeGame(self, game):
        self.games.remove(game)
    
class PracticeSlot:
    
    def __init__(self, max, min, day, startTime):
        self.max = max
        self.min = min
        self.day = day
        self.startTime = startTime
        self.practices = set()

    def addPractice(self, practice):
        self.practices.add(practice)
    
    def removePractice(self, practice):
        self.practices.remove(practice)