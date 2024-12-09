from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random

def Mutation(schedule):
    # If there are no game slots, return the schedule without any modifications
    if (not schedule.gameslots):
        return schedule

    # Randomly swap games between two game slots, repeat 1 to 5 times
    for i in range(1, random.randint(1, 5)):
        gameSlot1 = random.choice(schedule.gameslots)  # Randomly select first game slot
        gameSlot2 = random.choice(schedule.gameslots)  # Randomly select second game slot
        tempGames = gameSlot1.games  # Store the games from the first slot temporarily
        gameSlot1.games = gameSlot2.games  # Swap the games
        gameSlot2.games = tempGames  # Assign the temporarily stored games to the second slot

    # If there are no practice slots, return the schedule without any modifications
    if (not schedule.practiceslots):
        return schedule

    # Randomly swap practices between two practice slots, repeat 1 to 5 times
    for i in range(1, random.randint(1, 5)):
        practiceSlot1 = random.choice(schedule.practiceslots)  # Randomly select first practice slot
        practiceSlot2 = random.choice(schedule.practiceslots)  # Randomly select second practice slot
        tempGames = practiceSlot1.practices  # Store the practices from the first slot temporarily
        practiceSlot1.practices = practiceSlot2.practices  # Swap the practices
        practiceSlot2.practices = tempGames  # Assign the temporarily stored practices to the second slot

    return schedule  # Return the modified schedule with updated game and practice slots