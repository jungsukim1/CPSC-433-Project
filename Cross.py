from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random
import math

def Cross(scheduleA,scheduleB):
    day_order = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4}
    scheduleA.gameslots.sort(key=lambda slot: (day_order[slot.day], slot.startTime))
    scheduleB.gameslots.sort(key=lambda slot: (day_order[slot.day], slot.startTime))
    gameSwapRanger = random.randint(2, 5)
    randomStartIndex = random.randint(0, len(scheduleA.gameslots) - 6)
    while gameSwapRanger > 0:
        gameSlot1 = scheduleA.gameslots[randomStartIndex]
        gameSlot2 = scheduleB.gameslots[randomStartIndex]
        tempSlot = gameSlot1.games
        gameSlot1.games = gameSlot2.games
        gameSlot2.games = tempSlot
        gameSwapRanger -= 1
        randomStartIndex += 1
    
    scheduleA.practiceslots.sort(key=lambda slot: (day_order[slot.day], slot.startTime))
    scheduleB.practiceslots.sort(key=lambda slot: (day_order[slot.day], slot.startTime))
    practiceSwapRanger = random.randint(2, 5)
    randomStartIndex = random.randint(0, len(scheduleA.practiceslots) - 6)
    while practiceSwapRanger > 0:
        practiceSlot1 = scheduleA.practiceslots[randomStartIndex]
        practiceSlot2 = scheduleB.practiceslots[randomStartIndex]
        print(practiceSlot1.practices)
        print(practiceSlot2.practices)
        tempSlot = practiceSlot1.practices
        practiceSlot1.practices = practiceSlot2.practices
        practiceSlot2.practices = tempSlot
        practiceSwapRanger -= 1
        randomStartIndex += 1

    return (scheduleA,scheduleB)
    