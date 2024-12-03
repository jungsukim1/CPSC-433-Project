from InputParser import parse_input_file
from Slots import GameSlot, PracticeSlot
import random
from collections import defaultdict
import time

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

    start_time = time.time()  # Record the start time
    while not constr(fact):  # Check if 30 seconds have passed
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
            moTriedGames = defaultdict(set)
            tuTriedGames = defaultdict(set)
            moTriedPrac = defaultdict(set)
            tuTriedPrac = defaultdict(set)
            frTriedPrac = defaultdict(set)

            # Skip full slots
            if currentSlot in fullSlots:
                continue

            # Handle GameSlots
            if isinstance(currentSlot, GameSlot):
                if ((currentSlot.day == "TU" and currentSlot.startTime == "11:00") or
                    (currentSlot.day == "TU" and currentSlot.startTime == "12:30")):
                    continue
                if currentSlot.day in {"MO", "TU"}:
                    if len(currentSlot.games) < currentSlot.max:
                        alreadyAssigned = set(currentSlot.games)

                        # Remove invalid games
                        invalidGames = [g for g in currentSlot.games if not partConstr(g, fact, currentSlot)]
                        for g in invalidGames:
                            currentSlot.games.remove(g)
                            availableGames.append(g)
                            if currentSlot.day == "MO":
                                if g in moGamesAdd[currentSlot.startTime]:
                                    moGamesAdd[currentSlot.startTime].remove(g)
                                moTriedGames[f"{currentSlot.day} {currentSlot.startTime}"].add(g)
                            else:
                                if g in tuGamesAdd[currentSlot.startTime]:
                                    tuGamesAdd[currentSlot.startTime].remove(g)
                                tuTriedGames[f"{currentSlot.day} {currentSlot.startTime}"].add(g)

                        # Assign new games
                        newAvailableGames = None
                        if(currentSlot.day == "MO"):
                            newAvailableGames = [g for g in availableGames if g not in alreadyAssigned and g not in moTriedGames[f"{currentSlot.day} {currentSlot.startTime}"]]
                        else:
                            newAvailableGames = [g for g in availableGames if g not in alreadyAssigned and g not in tuTriedGames[f"{currentSlot.day} {currentSlot.startTime}"]]

                        if newAvailableGames:
                            gameIndex = random.randint(0, len(newAvailableGames) - 1)
                            selectedGame = newAvailableGames[gameIndex]

                            if partConstr(selectedGame, fact, currentSlot):
                                currentSlot.addGame(selectedGame)
                                if currentSlot.day == "MO":
                                    moGamesAdd[currentSlot.startTime].append(selectedGame)
                                    moTriedGames[f"{currentSlot.day} {currentSlot.startTime}"].add(selectedGame)
                                else:
                                    tuGamesAdd[currentSlot.startTime].append(selectedGame)
                                    tuTriedGames[f"{currentSlot.day} {currentSlot.startTime}"].add(selectedGame)
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
                                if p in moPracticesAdd[currentSlot.startTime]:
                                    moPracticesAdd[currentSlot.startTime].remove(p)
                                    moTriedPrac[f"{currentSlot.day} {currentSlot.startTime}"].add(p)
                            elif currentSlot.day == "TU":
                                if p in tuPracticesAdd[currentSlot.startTime]:
                                    tuPracticesAdd[currentSlot.startTime].remove(p)
                                    tuTriedPrac[f"{currentSlot.day} {currentSlot.startTime}"].add(p)
                            elif currentSlot.day == "FR":
                                frTriedPrac[f"{currentSlot.day} {currentSlot.startTime}"].add(p)

                        # Assign new practices
                        newAvailableGames = None
                        if(currentSlot.day == "MO"):
                            newAvailablePractice = [p for p in availablePractice if p not in alreadyAssigned and p not in moTriedPrac[f"{currentSlot.day} {currentSlot.startTime}"]]
                        elif(currentSlot.day == "TU"):
                            newAvailablePractice = [p for p in availablePractice if p not in alreadyAssigned and p not in tuTriedPrac[f"{currentSlot.day} {currentSlot.startTime}"]]
                        elif(currentSlot.day == "FR"):
                            newAvailablePractice = [p for p in availablePractice if p not in alreadyAssigned and p not in frTriedPrac[f"{currentSlot.day} {currentSlot.startTime}"]]
                        

                        if newAvailablePractice:
                            practiceIndex = random.randint(0, len(newAvailablePractice) - 1)
                            selectedPractice = newAvailablePractice[practiceIndex]
                            if partConstr(selectedPractice, fact, currentSlot):
                                currentSlot.addPractice(selectedPractice)
                                if currentSlot.day == "MO":
                                    moPracticesAdd[currentSlot.startTime].append(selectedPractice)
                                    moTriedPrac[f"{currentSlot.day} {currentSlot.startTime}"].add(selectedPractice)
                                elif currentSlot.day == "TU":
                                    tuPracticesAdd[currentSlot.startTime].append(selectedPractice)
                                    tuTriedPrac[f"{currentSlot.day} {currentSlot.startTime}"].add(selectedPractice)
                                elif currentSlot.day == "FR":
                                    frTriedPrac[f"{currentSlot.day} {currentSlot.startTime}"].add(selectedPractice)
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


def partConstr(assignment, fact, slot):
    tempFact = fact
    for time_slot in tempFact:
        if(isinstance(slot, GameSlot) and
           isinstance(time_slot, GameSlot)):
            if(time_slot.day == slot.day and
               time_slot.startTime == slot.startTime):
                time_slot.addGame(assignment)
        elif(isinstance(slot, PracticeSlot) and
             isinstance(time_slot, PracticeSlot)):
            if(time_slot.day == slot.day and
               time_slot.startTime == slot.startTime):
                time_slot.addPractice(assignment)

    team_dict = {}
    for slot in tempFact:
        time_slot = f"{slot.day} {slot.startTime}"
        if (isinstance(slot, GameSlot)):
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["games"].update(slot.games)
        elif (isinstance(slot, PracticeSlot)):
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["practices"].update(slot.practices)

    #Special practice and special games for last hard constraint for city of calgary
    special_game_bookings = {'CMSA U12T1', 'CMSA U13T1'}
    special_game_bookings_exists = any(any(game.startswith(base) for base in special_game_bookings) for _, activities in team_dict.items() for game in activities['practices'] | activities['games'])
    
    special_practice_bookings = {"CMSA U12T1S", "CMSA U13T1S"}
    u13_pair = {"CMSA U13T1S", "CMSA U13T1"}
    u12_pair = {"CMSA U12T1S", "CMSA U12T1"}
    special_practice_bookings_exists = any(any(game.startswith(base) for base in special_practice_bookings) for _, activities in team_dict.items() for game in activities['practices'] | activities['games'])

    for time_slot, teams in team_dict.items():
        overlap = teams["games"].intersection(teams["practices"])
        combined_teams = teams["games"].union(teams["practices"])
        day, time = time_slot.split(" ")
        hour, minute = time.split(":")
        hour = int(hour)
        minute = int(minute)

        # DIV 9 are all evening (DONE)
        if hour <= 18:
            div9_exists = [name for name in combined_teams if 'DIV 09' in name]
            if div9_exists:
                print(f"DIV 09 team(s) {div9_exists} scheduled in inappropriate slot {time_slot}")
                return False

        # No games Tuesday 11-12:30 (DONE)
        if day == "TU" and "11:00" <= time < "12:30":
            tuesday_games = teams["games"]
            if tuesday_games:
                print(f"Tuesday game not allowed in slot {time_slot}: {', '.join(tuesday_games)}")
                return False

        # Check not compatible set (DONE)
        for sets in not_compatible:
            if all(team in combined_teams for team in sets):
                print(f"Incompatible teams {', '.join(sets)} scheduled together on {time_slot}")
                return False

        # Same team assigned game and practice on same day and time (DONE)
        if overlap:
            print(f"Team(s): {', '.join(overlap)} have both game and practice at {time_slot}")
            return False

        # Check unwanted set (DONE)
        if time_slot in unwanted:
            unwanted_overlap = combined_teams.intersection(unwanted[time_slot])
            if unwanted_overlap:
                print(f"Unwanted constraint violated: {', '.join(unwanted_overlap)} scheduled at {time_slot}")
                return False
    
        # U15/U16/U17/U19 cant be in same game slots (DONE)
        keywords = {"U15", "U16", "U17", "U19"}
        keyword_overlap = [team for team in teams["games"] if any(keyword in team for keyword in keywords)]
        if len(keyword_overlap) > 1:
            print(f"Multiple age groups {', '.join(keyword_overlap)} scheduled in the same slot {time_slot}")
            return False
    
        #CMSA U12 T1S and CMSA U13 T1S must be scheduled for pracice on tues thurs 6-7
        if special_game_bookings_exists:
            if special_practice_bookings_exists:
                u13_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u13_pair)]
                u12_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u12_pair)]
                special_practices_in_this_slot= [team for team in teams["practices"] if any(keyword in team for keyword in special_practice_bookings)]     
                if (day == "TU" or day == "TH") and (hour == 18 and minute == 0):
                    if len(special_practices_in_this_slot) == 0:
                        print(f"Missing special practice bookings in required slot {time_slot}. Teams: {', '.join(special_practice_bookings)}")
                        return False
                else:
                    if len(special_practices_in_this_slot) > 0:
                        print(f"Special practice incorrectly scheduled in slot {time_slot}. Teams: {', '.join(special_practices_in_this_slot)}")
                        return False
                #CMSA U12T1S cant be in the same slot with CMSA U12T1 (DONE)
                if len(u12_matching) > 1:
                    print(f"Conflict: CMSA U12 T1S and U12 T1 both scheduled in slot {time_slot}. Teams: {', '.join(u12_matching)}")
                    return False
                #CMSA U13T1S cant be in the same slot with CMSA U13T1 (DONE)
                if len(u13_matching) > 1:
                    print(f"Conflict: CMSA U13 T1S and U13 T1 both scheduled in slot {time_slot}. Teams: {', '.join(u13_matching)}")
                    return False
    print("TEST PASSED")
    return True

def constr(fact):
    team_dict = {}
    isEmpty = True

    #check gamesmax and practicemax (DONE)
    for slot in fact:
        time_slot = f"{slot.day} {slot.startTime}"
        if (isinstance(slot, GameSlot)):
            if (slot.getSize() > slot.max):
                print(f"OVER GAME MAX: {slot.day} {slot.startTime}")
                return False
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["games"].update(slot.games)
        elif (isinstance(slot, PracticeSlot)):
            if (slot.getSize() > slot.max):
                print(f"OVER PRACTICE MAX: {slot.day} {slot.startTime}")
                return False
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["practices"].update(slot.practices)
        if(slot.getSize() > 0):
            isEmpty = False
    
    if(isEmpty):
        return False

    #Special practice and special games for last hard constraint for city of calgary
    special_game_bookings = {'CMSA U12T1', 'CMSA U13T1'}
    special_game_bookings_exists = any(any(game.startswith(base) for base in special_game_bookings) for _, activities in team_dict.items() for game in activities['practices'] | activities['games'])
    
    special_practice_bookings = {"CMSA U12T1S", "CMSA U13T1S"}
    u13_pair = {"CMSA U13T1S", "CMSA U13T1"}
    u12_pair = {"CMSA U12T1S", "CMSA U12T1"}
    special_practice_bookings_exists = any(any(game.startswith(base) for base in special_practice_bookings) for _, activities in team_dict.items() for game in activities['practices'] | activities['games'])

    for time_slot, teams in team_dict.items():
        overlap = teams["games"].intersection(teams["practices"])
        combined_teams = teams["games"].union(teams["practices"])
        day, time = time_slot.split(" ")
        hour, minute = time.split(":")
        hour = int(hour)
        minute = int(minute)

        # DIV 9 are all evening (DONE)
        if hour <= 18:
            div9_exists = [name for name in combined_teams if 'DIV 09' in name]
            if div9_exists:
                print(f"DIV 09 team(s) {div9_exists} scheduled in inappropriate slot {time_slot}")
                return False

        # No games Tuesday 11-12:30 (DONE)
        if day == "TU" and "11:00" <= time < "12:30":
            tuesday_games = teams["games"]
            if tuesday_games:
                print(f"Tuesday game not allowed in slot {time_slot}: {', '.join(tuesday_games)}")
                return False

        # Check not compatible set (DONE)
        for sets in not_compatible:
            if all(team in combined_teams for team in sets):
                print(f"Incompatible teams {', '.join(sets)} scheduled together on {time_slot}")
                return False

        # Same team assigned game and practice on same day and time (DONE)
        if overlap:
            print(f"Team(s): {', '.join(overlap)} have both game and practice at {time_slot}")
            return False

        # Check unwanted set (DONE)
        if time_slot in unwanted:
            unwanted_overlap = combined_teams.intersection(unwanted[time_slot])
            if unwanted_overlap:
                print(f"Unwanted constraint violated: {', '.join(unwanted_overlap)} scheduled at {time_slot}")
                return False
    
        # U15/U16/U17/U19 cant be in same game slots (DONE)
        keywords = {"U15", "U16", "U17", "U19"}
        keyword_overlap = [team for team in teams["games"] if any(keyword in team for keyword in keywords)]
        if len(keyword_overlap) > 1:
            print(f"Multiple age groups {', '.join(keyword_overlap)} scheduled in the same slot {time_slot}")
            return False
    
        #CMSA U12 T1S and CMSA U13 T1S must be scheduled for pracice on tues thurs 6-7
        if special_game_bookings_exists:
            if special_practice_bookings_exists:
                u13_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u13_pair)]
                u12_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u12_pair)]
                special_practices_in_this_slot= [team for team in teams["practices"] if any(keyword in team for keyword in special_practice_bookings)]     
                if (day == "TU" or day == "TH") and (hour == 18 and minute == 0):
                    if len(special_practices_in_this_slot) == 0:
                        print(f"Missing special practice bookings in required slot {time_slot}. Teams: {', '.join(special_practice_bookings)}")
                        return False
                else:
                    if len(special_practices_in_this_slot) > 0:
                        print(f"Special practice incorrectly scheduled in slot {time_slot}. Teams: {', '.join(special_practices_in_this_slot)}")
                        return False
                #CMSA U12T1S cant be in the same slot with CMSA U12T1 (DONE)
                if len(u12_matching) > 1:
                    print(f"Conflict: CMSA U12 T1S and U12 T1 both scheduled in slot {time_slot}. Teams: {', '.join(u12_matching)}")
                    return False
                #CMSA U13T1S cant be in the same slot with CMSA U13T1 (DONE)
                if len(u13_matching) > 1:
                    print(f"Conflict: CMSA U13 T1S and U13 T1 both scheduled in slot {time_slot}. Teams: {', '.join(u13_matching)}")
                    return False
    print("TEST PASSED")
    return True


(newFact, games, practices) = OrTree(fact[0], games, practices)

for slot in newFact:
    if(isinstance(slot, GameSlot)):
        print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
        print(slot.games)
    else:
        print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
        print(slot.practices)

