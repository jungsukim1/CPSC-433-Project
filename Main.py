from InputParser import parse_input_file
from Slots import GameSlot, PracticeSlot
import random
from Schedule import Schedule
from OrTreeLogic import OrTree
import copy

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


DEFAULTFACT = Schedule()

# Append all GameSlot objects to the array
for game_slot in game_slot_objects.values():
    DEFAULTFACT.addGameSlot(game_slot)

# Append all PracticeSlot objects to the array
for practice_slot in practice_slot_objects.values():
    DEFAULTFACT.addPracticeSlot(practice_slot)

for schedule in DEFAULTFACT.gameslots + DEFAULTFACT.practiceslots:
    key = f"{schedule.day} {schedule.startTime}"
    if key in partial_assignments and partial_assignments[key]:
        if "PRC" in partial_assignments[key][0] or "OPN" in partial_assignments[key][0]:
            schedule.addPractice(partial_assignments[key][0])
            if partial_assignments[key][0] in practices:
                practices.remove(partial_assignments[key][0])
        else:
            schedule.addGame(partial_assignments[key][0])
            if partial_assignments[key][0] in games:
                games.remove(partial_assignments[key][0])
        del partial_assignments[key]

    if (schedule.day == "TU" and schedule.startTime == "18:00" and isinstance(schedule, PracticeSlot) or
        schedule.day == "TH" and schedule.startTime == "18:00" and isinstance(schedule, PracticeSlot)):
        if any('CMSA U12T1' in game for game in games):
            schedule.addPractice('CMSA U12T1S')
        if any('CMSA U13T1' in game for game in games):
            schedule.addPractice('CMSA U13T1S')

FACTS = []

FACTS.append(DEFAULTFACT)

newFact = OrTree(FACTS[0], games, practices)


# for slot in newFact:
#     if(isinstance(slot, GameSlot)):
#         print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
#         print(slot.games)
#     else:
#         print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
#         print(slot.practices)

FACTS.append(newFact)

secondFact = copy.deepcopy(FACTS[1])
slot = random.choice(secondFact.gameslots + secondFact.practiceslots)

# print(slot.day, slot.startTime)
if isinstance(slot, GameSlot):
    slot.addGame(games[10])
    print(slot.games)
else:
    slot.addPractice(practices[10])
    print(slot.practices)

newSecondFact = OrTree(secondFact, games, practices)

for slot in newSecondFact.gameslots + newSecondFact.practiceslots:
    if(isinstance(slot, GameSlot)):
        print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
        print(slot.games)
    else:
        print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
        print(slot.practices)

print(len(newSecondFact.gameslots) + len(newSecondFact.practiceslots))