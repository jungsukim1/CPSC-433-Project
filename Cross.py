from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random

def Cross(scheduleA, scheduleB):
    # Define a mapping for the days to sort by order
    day_order = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4}

    # If neither schedule has game slots, return early
    if (not scheduleA.gameslots and not scheduleB.gameslots):
        return

    # Sort game slots in both schedules by day and start time
    scheduleA.gameslots.sort(key=lambda slot: (day_order[slot.day], slot.startTime))
    scheduleB.gameslots.sort(key=lambda slot: (day_order[slot.day], slot.startTime))

    # Random number of game slots to swap
    gameSwapRanger = random.randint(2, 5)
    randomStartIndex = random.randint(0, len(scheduleA.gameslots) - 6)

    # Perform the swap operation for the selected game slots
    while gameSwapRanger > 0:
        gameSlot1 = scheduleA.gameslots[randomStartIndex]
        gameSlot2 = scheduleB.gameslots[randomStartIndex]
        tempSlot = gameSlot1.games
        gameSlot1.games = gameSlot2.games
        gameSlot2.games = tempSlot
        gameSwapRanger -= 1
        randomStartIndex += 1

    # If neither schedule has practice slots, return early
    if (not scheduleA.practiceslots and not scheduleB.practiceslots):
        return

    # Sort practice slots in both schedules by day and start time
    scheduleA.practiceslots.sort(key=lambda slot: (day_order[slot.day], slot.startTime))
    scheduleB.practiceslots.sort(key=lambda slot: (day_order[slot.day], slot.startTime))

    # Random number of practice slots to swap
    practiceSwapRanger = random.randint(2, 5)
    randomStartIndex = random.randint(0, len(scheduleA.practiceslots) - 6)

    # Perform the swap operation for the selected practice slots
    while practiceSwapRanger > 0:
        practiceSlot1 = scheduleA.practiceslots[randomStartIndex]
        practiceSlot2 = scheduleB.practiceslots[randomStartIndex]
        tempSlot = practiceSlot1.practices
        practiceSlot1.practices = practiceSlot2.practices
        practiceSlot2.practices = tempSlot
        practiceSwapRanger -= 1
        randomStartIndex += 1

    # Return the modified schedules after the cross operation
    return (scheduleA, scheduleB)