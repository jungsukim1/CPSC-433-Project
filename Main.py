from InputParser import parse_input_file
from collections import defaultdict
from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random
import copy
from Mutation import Mutation
from Cross import Cross
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


def OrTree(fact, games, practices):
    timeout = 3  # Timeout duration in seconds
    timedOut = False

    # Return the fact if it already satisfies constraints
    if constr(fact):
        return fact

    start_time = time.time()  # Start the timer for this iteration

    while True:
        # Check for timeout
        if time.time() - start_time > timeout:
            print("Timeout occurred. Resetting fact to DEFAULTFACT.")
            fact = DEFAULTFACT  # Reset fact to DEFAULTFACT
            timedOut = True
            break

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
            break  # Exit inner loop if constraints are satisfied

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

    if timedOut:
        return timedOut

    return newFact


def partConstr(assignment, fact, slot):

    if isinstance(slot, GameSlot):
        if len(slot.games) > slot.max:
            return False
    else:
        if len(slot.practices) > slot.max:
            return False


    team_dict = {}
    for slot in fact.gameslots + fact.practiceslots:
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
        # print(f"Time Slot: {time_slot}, Games: {teams['games']}, Practices: {teams['practices']}")
        day, time = time_slot.split(" ")
        hour, minute = time.split(":")
        hour = int(hour)
        minute = int(minute)

        # DIV 9 are all evening (DONE)
        if hour <= 18:
            div9_exists = [name for name in combined_teams if 'DIV 09' in name]
            if div9_exists:
                #print(f"DIV 09 team(s) {div9_exists} scheduled in inappropriate slot {time_slot}")
                return False

        # No games Tuesday 11-12:30 (DONE)
        if day == "TU" and "11:00" <= time <= "12:30":
            tuesday_games = teams["games"]
            if tuesday_games:
                #print(f"Tuesday game not allowed in slot {time_slot}: {', '.join(tuesday_games)}")
                return False

        # Check not compatible set (DONE)
        for sets in not_compatible:
            if all(team in teams["games"] for team in sets):
                #print(f"Incompatible teams {', '.join(sets)} scheduled together on {time_slot}")
                return False
            if all(team in teams["practices"] for team in sets):
                #print(f"Incompatible teams {', '.join(sets)} scheduled together on {time_slot}")
                return False

        # Same team assigned game and practice on same day and time (DONE)
        if overlap:
            #print(f"Team(s): {', '.join(overlap)} have both game and practice at {time_slot}")
            return False

        # Check unwanted set (DONE)
        if time_slot in unwanted:
            unwanted_overlap = combined_teams.intersection(unwanted[time_slot])
            if unwanted_overlap:
                #print(f"Unwanted constraint violated: {', '.join(unwanted_overlap)} scheduled at {time_slot}")
                return False
    
        # U15/U16/U17/U19 cant be in same game slots (DONE)
        keywords = {"U15", "U16", "U17", "U19"}
        keyword_overlap = [team for team in teams["games"] if any(keyword in team for keyword in keywords)]
        if len(keyword_overlap) > 1:
            #print(f"Multiple age groups {', '.join(keyword_overlap)} scheduled in the same slot {time_slot}")
            return False
    
        #CMSA U12 T1S and CMSA U13 T1S must be scheduled for pracice on tues thurs 6-7
        if special_game_bookings_exists:
            if special_practice_bookings_exists:
                u13_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u13_pair)]
                u12_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u12_pair)]
                special_practices_in_this_slot= [team for team in teams["practices"] if any(keyword in team for keyword in special_practice_bookings)]     
                if (day == "TU" or day == "TH") and (hour == 18 and minute == 0):
                    if len(special_practices_in_this_slot) == 0:
                        #print(f"Missing special practice bookings in required slot {time_slot}. Teams: {', '.join(special_practice_bookings)}")
                        return False
                else:
                    if len(special_practices_in_this_slot) > 0:
                        #print(f"Special practice incorrectly scheduled in slot {time_slot}. Teams: {', '.join(special_practices_in_this_slot)}")
                        return False
                #CMSA U12T1S cant be in the same slot with CMSA U12T1 (DONE)
                if len(u12_matching) > 1:
                    #print(f"Conflict: CMSA U12 T1S and U12 T1 both scheduled in slot {time_slot}. Teams: {', '.join(u12_matching)}")
                    return False
                #CMSA U13T1S cant be in the same slot with CMSA U13T1 (DONE)
                if len(u13_matching) > 1:
                    #print(f"Conflict: CMSA U13 T1S and U13 T1 both scheduled in slot {time_slot}. Teams: {', '.join(u13_matching)}")
                    return False
    #print("TEST PASSED")

    return True

def constr(fact):
    team_dict = {}
    isEmpty = True

    if fact == DEFAULTFACT:
        return False

    #check gamesmax and practicemax (DONE)
    for slot in fact.gameslots + fact.practiceslots:
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
    

    # #Special practice and special games for last hard constraint for city of calgary
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
                #print(f"DIV 09 team(s) {div9_exists} scheduled in inappropriate slot {time_slot}")
                return False

        # No games Tuesday 11-12:30 (DONE)
        if day == "TU" and "11:00" <= time < "12:30":
            tuesday_games = teams["games"]
            if tuesday_games:
                #print(f"Tuesday game not allowed in slot {time_slot}: {', '.join(tuesday_games)}")
                return False

        # Check not compatible set (DONE)
        for sets in not_compatible:
            if all(team in teams["games"] for team in sets):
                #print(f"Incompatible teams {', '.join(sets)} scheduled together on {time_slot}")
                return False
            if all(team in teams["practices"] for team in sets):
                #print(f"Incompatible teams {', '.join(sets)} scheduled together on {time_slot}")
                return False

        # Same team assigned game and practice on same day and time (DONE)
        if overlap:
            #print(f"Team(s): {', '.join(overlap)} have both game and practice at {time_slot}")
            return False

        # Check unwanted set (DONE)
        if time_slot in unwanted:
            unwanted_overlap = combined_teams.intersection(unwanted[time_slot])
            if unwanted_overlap:
                #print(f"Unwanted constraint violated: {', '.join(unwanted_overlap)} scheduled at {time_slot}")
                return False
    
        # U15/U16/U17/U19 cant be in same game slots (DONE)
        keywords = {"U15", "U16", "U17", "U19"}
        keyword_overlap = [team for team in teams["games"] if any(keyword in team for keyword in keywords)]
        if len(keyword_overlap) > 1:
            #print(f"Multiple age groups {', '.join(keyword_overlap)} scheduled in the same slot {time_slot}")
            return False
    
        #CMSA U12 T1S and CMSA U13 T1S must be scheduled for pracice on tues thurs 6-7
        if special_game_bookings_exists:
            if special_practice_bookings_exists:
                u13_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u13_pair)]
                u12_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u12_pair)]
                special_practices_in_this_slot= [team for team in teams["practices"] if any(keyword in team for keyword in special_practice_bookings)]     
                if (day == "TU" or day == "TH") and (hour == 18 and minute == 0):
                    if len(special_practices_in_this_slot) == 0:
                        #print(f"Missing special practice bookings in required slot {time_slot}. Teams: {', '.join(special_practice_bookings)}")
                        return False
                else:
                    if len(special_practices_in_this_slot) > 0:
                        #print(f"Special practice incorrectly scheduled in slot {time_slot}. Teams: {', '.join(special_practices_in_this_slot)}")
                        return False
                #CMSA U12T1S cant be in the same slot with CMSA U12T1 (DONE)
                if len(u12_matching) > 1:
                    #print(f"Conflict: CMSA U12 T1S and U12 T1 both scheduled in slot {time_slot}. Teams: {', '.join(u12_matching)}")
                    return False
                #CMSA U13T1S cant be in the same slot with CMSA U13T1 (DONE)
                if len(u13_matching) > 1:
                    #print(f"Conflict: CMSA U13 T1S and U13 T1 both scheduled in slot {time_slot}. Teams: {', '.join(u13_matching)}")
                    return False
    #print("TEST PASSED")
    return True

newFact = OrTree(FACTS[0], games, practices)


# for slot in newFact:
#     if(isinstance(slot, GameSlot)):
#         print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
#         print(slot.games)
#     else:
#         print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
#         print(slot.practices)

FACTS.append(newFact)
# print(constr(mutatedFact))
# print("Mutated")
# for slot in mutatedFact.gameslots + mutatedFact.practiceslots:
#     if(isinstance(slot, GameSlot)):
#         print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
#         print(slot.games)
#     else:
#         print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
#         print(slot.practices)
# Timeout and retry logic

mutatedFact = Mutation(FACTS[1], games, practices)
fixedMutatedFact = OrTree(mutatedFact, games, practices)
if fixedMutatedFact == True:
    fixedMutatedFact = OrTree(DEFAULTFACT, games, practices)
# for slot in fixedMutatedFact.gameslots + fixedMutatedFact.practiceslots:
#     if(isinstance(slot, GameSlot)):
#         print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
#         print(slot.games)
#     else:
#         print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
#         print(slot.practices)
    

FACTS.append(fixedMutatedFact)



# crossFact = Cross(FACTS[1], FACTS[2])