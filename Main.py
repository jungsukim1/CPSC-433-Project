from InputParser import parse_input_file
from Slots import GameSlot, PracticeSlot
import random
from collections import defaultdict

def create_game_and_practice_slots(game_slots, practice_slots):

    game_duplications = {
        "MO": ["WE", "FR"],
        "TU": ["TH"],
    }
    practice_duplications = {
        "MO": ["WE"],
        "TU": ["TH"],
    }

    # Function to create slots and apply duplications
    def duplicate_slots(slot_dict, slot_class, duplications):
        slot_objects = {}
        for slot_key, slot_data in slot_dict.items():
            day, time = slot_key.split()
            max_val = slot_data["max"]
            min_val = slot_data["min"]

            # Create the primary slot
            slot = slot_class(max_val, min_val, day, time)
            slot_objects[f"{day} {time}"] = slot

            # Create duplicate slots for specified days
            for new_day in duplications.get(day, []):
                duplicate_slot = slot_class(max_val, min_val, new_day, time)
                slot_objects[f"{new_day} {time}"] = duplicate_slot

        return slot_objects

    # Create and duplicate GameSlot objects
    game_slot_objects = duplicate_slots(game_slots, GameSlot, game_duplications)

    # Create and duplicate PracticeSlot objects
    practice_slot_objects = duplicate_slots(practice_slots, PracticeSlot, practice_duplications)

    return game_slot_objects, practice_slot_objects



# Parse the input file
(
    game_slots, practice_slots, games, practices, not_compatible,
    unwanted, preferences, pair, partial_assignments, wminfilled, 
    wpref, wpair, wsecdiff, pengamemin, penpracticemin,
    pennotpaired, pensection
) = parse_input_file()

# Create GameSlot and PracticeSlot objects
game_slot_objects, practice_slot_objects = create_game_and_practice_slots(game_slots, practice_slots)

slots_array = []

# Append all GameSlot objects to the array
for game_slot in game_slot_objects.values():
    slots_array.append(game_slot)

# Append all PracticeSlot objects to the array
for practice_slot in practice_slot_objects.values():
    slots_array.append(practice_slot)

for schedule in slots_array:
    key = f"{schedule.day} {schedule.startTime}"
    if key in partial_assignments and partial_assignments[key]:
        if "PRC" in partial_assignments[key][0] or "OPN" in partial_assignments[key][0]:
            schedule.addPractice(partial_assignments[key][0])
            if(partial_assignments[key][0] in practices):
                practices.remove(partial_assignments[key][0])
        else:
            schedule.addGame(partial_assignments[key][0])
            if(partial_assignments[key][0] in games):
                games.remove(partial_assignments[key][0])
        del partial_assignments[key]

fact = [slots_array]

# # Print created slots for verification
# print("Game Slots:")
# for slot_key, slot in game_slot_objects.items():
#     print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
#     print(slot.games)

# print("\nPractice Slots:")
# for slot_key, slot in practice_slot_objects.items():
#     print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
#     print(slot.practices)

# print("\nGames:")
# for game in games:
#     print(f"  {game}")

# print("\nPractices:")
# for practice in practices:
#     print(f"  {practice}")

# print("\nNot Compatible:")
# for pair in not_compatible:
#     print(f"  {pair}")

# print("\nUnwanted:")
# for key, identifiers in unwanted.items():
#     print(f"  {key} -> {', '.join(identifiers)}")

# print("\nPreferences:")
# for key, value in preferences.items():
#     print(f"  {key} -> {value}")

# print("\nPair:")
# for pair_value in pair:
#     print(f"  {pair_value}")

# print("\nPartial Assignments:")
# for key, identifiers in partial_assignments.items():
#     print(f"  {key} -> {', '.join(identifiers)}")

# # Print Weights and Penalty values
# print("\nWeights and Penalty values:")
# print(f"wminfilled: {wminfilled}")
# print(f"wpref: {wpref}")
# print(f"wpair: {wpair}")
# print(f"wsecdiff: {wsecdiff}")
# print(f"pengamemin: {pengamemin}")
# print(f"penpracticemin: {penpracticemin}")
# print(f"pennotpaired: {pennotpaired}")
# print(f"pensection: {pensection}")

#TODO: Gotta handle the case where there is already a schedule
#Meaning there is already a game/practice assigned to
def OrTree(fact, games, practices):
    availableGames = games
    availablePractice = practices

    if constr(fact):
        return fact, games, practices

    while not constr(fact):
        finished = False
        fullSlots = set()
        moGamesAdd = defaultdict(list)
        tuGamesAdd = defaultdict(list)
        moPracticesAdd = defaultdict(list)
        tuPracticesAdd = defaultdict(list)

        while (len(availableGames) + len(availablePractice) > 0) and not finished:
            # Randomly select a slot
            index = random.randint(0, len(fact) - 1)
            currentSlot = fact[index]

            # Skip full slots
            if currentSlot in fullSlots:
                continue

            # Handle GameSlots
            if isinstance(currentSlot, GameSlot):
                if currentSlot.day in {"MO", "TU"}:
                    if len(currentSlot.games) < currentSlot.max:
                        alreadyAssigned = set(currentSlot.games)

                        # Remove invalid games
                        invalidGames = [g for g in currentSlot.games if not partConstr(g, fact, currentSlot)]
                        for g in invalidGames:
                            currentSlot.games.remove(g)
                            availableGames.append(g)
                            if currentSlot.day == "MO":
                                moGamesAdd[currentSlot.startTime].remove(g)
                            else:
                                tuGamesAdd[currentSlot.startTime].remove(g)
                            alreadyAssigned.remove(g)

                        # Assign new games
                        newAvailableGames = [g for g in availableGames if g not in alreadyAssigned]
                        if newAvailableGames:
                            gameIndex = random.randint(0, len(newAvailableGames) - 1)
                            selectedGame = newAvailableGames[gameIndex]

                            if partConstr(selectedGame, fact, currentSlot):
                                currentSlot.addGame(selectedGame)
                                if currentSlot.day == "MO":
                                    moGamesAdd[currentSlot.startTime].append(selectedGame)
                                else:
                                    tuGamesAdd[currentSlot.startTime].append(selectedGame)
                                availableGames.remove(selectedGame)

                    # Mark as full if max reached
                    if len(currentSlot.games) >= currentSlot.max:
                        fullSlots.add(currentSlot)

            # Handle PracticeSlots
            elif isinstance(currentSlot, PracticeSlot):
                if currentSlot.day in {"MO", "TU", "FR"}:
                    if len(currentSlot.practices) < currentSlot.max:
                        alreadyAssigned = set(currentSlot.practices)

                        # Remove invalid practices
                        invalidPractices = [p for p in currentSlot.practices if not partConstr(p, fact, currentSlot)]
                        for p in invalidPractices:
                            currentSlot.practices.remove(p)
                            availablePractice.append(p)
                            if currentSlot.day == "MO":
                                moPracticesAdd[currentSlot.startTime].remove(p)
                            elif currentSlot.day == "TU":
                                tuPracticesAdd[currentSlot.startTime].remove(p)
                            alreadyAssigned.remove(p)

                        # Assign new practices
                        newAvailablePractice = [p for p in availablePractice if p not in alreadyAssigned]
                        if newAvailablePractice:
                            practiceIndex = random.randint(0, len(newAvailablePractice) - 1)
                            selectedPractice = newAvailablePractice[practiceIndex]

                            if partConstr(selectedPractice, fact, currentSlot):
                                currentSlot.addPractice(selectedPractice)
                                if currentSlot.day == "MO":
                                    moPracticesAdd[currentSlot.startTime].append(selectedPractice)
                                elif currentSlot.day == "TU":
                                    tuPracticesAdd[currentSlot.startTime].append(selectedPractice)
                                availablePractice.remove(selectedPractice)

                    # Mark as full if max reached
                    if len(currentSlot.practices) >= currentSlot.max:
                        fullSlots.add(currentSlot)

        # Update slots after processing
        for slot in fact:
            if isinstance(slot, GameSlot):
                if slot.day in {"WE", "FR"}:
                    for game in moGamesAdd[slot.startTime]:
                        if game not in slot.games:
                            slot.games.add(game)
                elif slot.day == "TH":
                    for game in tuGamesAdd[slot.startTime]:
                        if game not in slot.games:
                            slot.games.add(game)

                if len(slot.games) >= slot.max:
                    fullSlots.add(slot)

            elif isinstance(slot, PracticeSlot):
                if slot.day == "WE":
                    for practice in moPracticesAdd[slot.startTime]:
                        if practice not in slot.practices:
                            slot.practices.add(practice)
                elif slot.day == "TH":
                    for practice in tuPracticesAdd[slot.startTime]:
                        if practice not in slot.practices:
                            slot.practices.add(practice)

                if len(slot.practices) >= slot.max:
                    fullSlots.add(slot)

        if len(fullSlots) == len(fact):
            finished = True

    return fact, availableGames, availablePractice

def constr(fact):
    randomInt = random.randint(0, 1)
    if(randomInt == 1):
        return True
    return False

def partConstr(assignment, fact, slot):
    randomInt = random.randint(0, 4)
    if(randomInt == 1):
        return False
    return True

(newFact, games, practices) = OrTree(fact[0], games, practices)

for slot in newFact:
    if(isinstance(slot, GameSlot)):
        print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
        print(slot.games)
    else:
        print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
        print(slot.practices)