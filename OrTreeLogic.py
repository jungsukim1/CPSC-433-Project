from Slots import GameSlot, PracticeSlot
import random
from Schedule import Schedule
from collections import defaultdict
from Contraints import constr, partConstr

def OrTree(fact, games, practices):
    if constr(fact):
        return fact

    while True:
        # Create shallow copies of gameslots and practiceslots
        tempFact = fact
        
        newFact = Schedule()  # Reset newFact as an empty Schedule object
        assignedGames = set()  # Reset the set of assigned games
        assignedPractice = set()  # Reset the set of assigned practices
        moGamesAssigned = defaultdict(list)
        tuGamesAssigned = defaultdict(list)
        moPracticesAssigned = defaultdict(list)
        tuPracticesAssigned = defaultdict(list)

        while tempFact.gameslots or tempFact.practiceslots:  # Process all slots in tempFact
            # Combine both gameslots and practiceslots into one list
            combined_slots = tempFact.gameslots + tempFact.practiceslots
            slot = random.choice(combined_slots)  # Select a random slot
            
            if isinstance(slot, GameSlot):  # Check if it's a game slot
                tempFact.removeSpecificGameSlot(slot)
                if slot not in newFact.gameslots:
                    newFact.addGameSlot(slot)
            else:  # It's a practice slot
                tempFact.removeSpecficPracticeSlot(slot)
                if slot not in newFact.practiceslots:
                    newFact.addPracticeSlot(slot)
            
            # Add the slot to newFact to ensure it is not lost
                
            if isinstance(slot, GameSlot):  # Handle game slots
                if (slot.day == "MO") or (slot.day == "TU" and slot.startTime != "11:00") or (slot.day == "TH" and slot.startTime == "12:30"):
                    # Remove games that fail partial constraints
                    for game in list(slot.games):
                        if not partConstr(game, newFact, slot):
                            assignedGames.discard(game)
                            slot.games.discard(game)
                            if slot.day == "MO" and game in moGamesAssigned[slot.startTime]:
                                moGamesAssigned[slot.startTime].remove(game)
                            elif slot.day == "TU" and game in tuGamesAssigned[slot.startTime]:
                                tuGamesAssigned[slot.startTime].remove(game)
                        else:
                            if slot.day == "MO" and game not in moGamesAssigned[slot.startTime]:
                                moGamesAssigned[slot.startTime].append(game)
                            elif slot.day == "TU" and game not in tuGamesAssigned[slot.startTime]:
                                tuGamesAssigned[slot.startTime].append(game)
                    
                    # Assign available games to the slot
                    availableGames = [g for g in games if g not in assignedGames]
                    while slot.getSize() < slot.max and availableGames:
                        ranGame = random.choice(availableGames)
                        slot.addGame(ranGame)
                        if partConstr(ranGame, newFact, slot):
                            assignedGames.add(ranGame)
                            if slot.day == "MO" and ranGame not in moGamesAssigned[slot.startTime]:
                                moGamesAssigned[slot.startTime].append(ranGame)
                            elif slot.day == "TU" and ranGame not in tuGamesAssigned[slot.startTime]:
                                tuGamesAssigned[slot.startTime].append(ranGame)
                        else:
                            slot.games.discard(ranGame)
                            assignedGames.discard(ranGame)
                        availableGames.remove(ranGame)

            else:  # Handle practice slots
                if slot.day in {"MO", "TU", "FR"}:
                    # Remove practices that fail partial constraints
                    for practice in list(slot.practices):
                        if not partConstr(practice, newFact, slot):
                            assignedPractice.discard(practice)
                            slot.practices.discard(practice)
                            if slot.day == "MO" and practice in moPracticesAssigned[slot.startTime]:
                                moPracticesAssigned[slot.startTime].remove(practice)
                            elif slot.day == "TU" and practice in tuPracticesAssigned[slot.startTime]:
                                tuPracticesAssigned[slot.startTime].remove(practice)
                        else:
                            if slot.day == "MO" and practice not in moPracticesAssigned[slot.startTime]:
                                moPracticesAssigned[slot.startTime].append(practice)
                            elif slot.day == "TU" and practice not in tuPracticesAssigned[slot.startTime]:
                                tuPracticesAssigned[slot.startTime].append(practice)

                    # Assign available practices to the slot
                    availablePractice = [p for p in practices if p not in assignedPractice]
                    while slot.getSize() < slot.max and availablePractice:
                        ranPractice = random.choice(availablePractice)
                        slot.addPractice(ranPractice)
                        if partConstr(ranPractice, newFact, slot):
                            assignedPractice.add(ranPractice)
                            if slot.day == "MO" and ranPractice not in moPracticesAssigned[slot.startTime]:
                                moPracticesAssigned[slot.startTime].append(ranPractice)
                            elif slot.day == "TU" and ranPractice not in tuPracticesAssigned[slot.startTime]:
                                tuPracticesAssigned[slot.startTime].append(ranPractice)
                        else:
                            slot.practices.discard(ranPractice)
                            assignedPractice.discard(ranPractice)
                        availablePractice.remove(ranPractice)

        if constr(newFact):
            break
    
    for slot in newFact.gameslots + newFact.practiceslots:
        if isinstance(slot, GameSlot):
            if slot.day in {"WE", "FR"}:
                for game in moGamesAssigned[slot.startTime]:
                    slot.addGame(game)
            elif slot.day == "TH":
                for game in tuGamesAssigned[slot.startTime]:
                    slot.addGame(game)
        else:
            if slot.day == "WE":
                for practice in moPracticesAssigned[slot.startTime]:
                    slot.addPractice(practice)
            elif slot.day == "TH":
                for practice in tuPracticesAssigned[slot.startTime]:
                    slot.addPractice(practice)

    return newFact