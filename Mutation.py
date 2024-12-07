from InputParser import parse_input_file
from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random


#fact - list of all selected games and practices in their slots
#games - all possible games
#practices - all possible practices
#TODO connect with ORTree and test that it works
def Mutation(schedule):
    if (not schedule.gameslots):
        return
    for i in range(1, random.randint(1, 5)):
        gameSlot1 = random.choice(schedule.gameslots)
        gameSlot2 = random.choice(schedule.gameslots)
        tempGames = gameSlot1.games
        gameSlot1.games = gameSlot2.games
        gameSlot2.games = tempGames
    if (not schedule.practiceslots):
        return
    for i in range(1, random.randint(1, 5)):
        practiceSlot1 = random.choice(schedule.practiceslots)
        practiceSlot2 = random.choice(schedule.practiceslots)
        tempGames = practiceSlot1.practices
        practiceSlot1.practices = practiceSlot2.practices
        practiceSlot2.practices = tempGames
    return schedule #return modified gameslots and practice slots 