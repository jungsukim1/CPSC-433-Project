from InputParser import parse_input_file
from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random
import copy
from Eval import Eval
from Mutation import Mutation
from Cross import Cross
from collections import defaultdict
import re
from Delete import Delete
import time

def create_game_and_practice_slots(game_slots, practice_slots):

    # game_duplications = {
    #     "MO": ["WE", "FR"],
    #     "TU": ["TH"],
    # }
    # practice_duplications = {
    #     "MO": ["WE"],
    #     "TU": ["TH"],
    # }

    # Function to create slots and apply duplications
    def duplicate_slots(slot_dict, slot_class):
        slot_objects = {}
        for slot_key, slot_data in slot_dict.items():
            day, time = slot_key.split()
            max_val = slot_data["max"]
            min_val = slot_data["min"]

            # Create the primary slot
            slot = slot_class(max_val, min_val, day, time)
            slot_objects[f"{day} {time}"] = slot

        return slot_objects

    # Create and duplicate GameSlot objects
    game_slot_objects = duplicate_slots(game_slots, GameSlot)

    # Create and duplicate PracticeSlot objects
    practice_slot_objects = duplicate_slots(practice_slots, PracticeSlot)


    return game_slot_objects, practice_slot_objects



# Parse the input file
(
    game_slots, practice_slots, games, practices, not_compatible,
    unwanted, preferences, pair, partial_assignments, wminfilled, 
    wpref, wpair, wsecdiff, pengamemin, penpracticemin,
    pennotpaired, pensection
) = parse_input_file()


def verifyInput():
    gamesTotal = 0
    practiceTotal = 0

    for slot in game_slots:
        gamesTotal += game_slots[slot]['max']
    for slot in practice_slots:
        practiceTotal += practice_slots[slot]['max']

    if not games and not practices:
        print("No games and practices")
        return False
    if not game_slots and practice_slots:
        print("No game slots and practice slots")
        return False
    if games and not game_slots:
        print("Games exist but no slots")
        return False
    if practices and not practice_slots:
        print("Practice exist but no slots")
        return False
    if any('CMSA U12T1' in game for game in games) or any('CMSA U13T1' in game for game in games):
        if not any(
            schedule.day == "TU" and schedule.startTime == "18:00" and isinstance(schedule, PracticeSlot)
            for schedule in DEFAULTFACT.practiceslots
        ):
            print("No Special Team Slot Exist!")
            return False
    
    if len(games) > gamesTotal:
        print("Not enough Game slots")
        return False
    if len(practices) > practiceTotal:
        print("Not enough Practice slots")
        return False
    return True




# Create GameSlot and PracticeSlot objects
game_slot_objects, practice_slot_objects = create_game_and_practice_slots(game_slots, practice_slots)


DEFAULTFACT = Schedule([], [])

PARTIAL_ASSIGNMENTS = []

# Append all GameSlot objects to the array
for game_slot in game_slot_objects.values():
    DEFAULTFACT.addGameSlot(game_slot)

# Append all PracticeSlot objects to the array
for practice_slot in practice_slot_objects.values():
    DEFAULTFACT.addPracticeSlot(practice_slot)

def addPartialAssign():
                
    gamesTotal = 0
    practiceTotal = 0
    assignedSpectial = False

    for schedule in DEFAULTFACT.gameslots + DEFAULTFACT.practiceslots:
        key = f"{schedule.day} {schedule.startTime}"
        
        if isinstance(schedule, PracticeSlot):
            practiceTotal += schedule.max
            if key in partial_assignments and partial_assignments[key]:
                if "PRC" in partial_assignments[key][0] or "OPN" in partial_assignments[key][0]:
                    schedule.addPractice(partial_assignments[key][0])
                    if partial_assignments[key][0] not in PARTIAL_ASSIGNMENTS:
                        PARTIAL_ASSIGNMENTS.append(partial_assignments[key][0])
                    # if partial_assignments[key][0] in practices:
                    #     practices.remove(partial_assignments[key][0])
                    del partial_assignments[key]
        else:
            gamesTotal += schedule.max
            if key in partial_assignments and partial_assignments[key]:
                if "PRC" not in partial_assignments[key][0] or "OPN" not in partial_assignments[key][0]:
                    schedule.addGame(partial_assignments[key][0])
                    if partial_assignments[key][0] not in PARTIAL_ASSIGNMENTS:
                        PARTIAL_ASSIGNMENTS.append(partial_assignments[key][0])
                    # if partial_assignments[key][0] in games:
                    #     games.remove(partial_assignments[key][0])
                    del partial_assignments[key]
        if (schedule.day == "TU" and schedule.startTime == "18:00" and isinstance(schedule, PracticeSlot)):
            if any('CMSA U12T1' in game for game in games):
                if 'CMSA U12T1S' not in PARTIAL_ASSIGNMENTS:
                    PARTIAL_ASSIGNMENTS.append('CMSA U12T1S')
                schedule.addPractice('CMSA U12T1S')
            if any('CMSA U13T1' in game for game in games):
                if 'CMSA U13T1S' not in PARTIAL_ASSIGNMENTS:
                    PARTIAL_ASSIGNMENTS.append('CMSA U13T1S')
                schedule.addPractice('CMSA U13T1S')
    
    return True

def OrTree(fact, games, practices):
    if fact == None:
        fact = DEFAULTFACT

    games = [game for game in games if game not in PARTIAL_ASSIGNMENTS]
    practices = [practice for practice in practices if practice not in PARTIAL_ASSIGNMENTS]

    if constr(fact):
        return fact

    startTime = time.time()
    while True:
        # Create shallow copies of gameslots and practiceslots 
        tempFact = copy.deepcopy(fact)
        newFact = Schedule([], [])  # Reset newFact as an empty Schedule object
        assignedGames = set()  # Reset the set of assigned games
        assignedPractice = set()  # Reset the set of assigned practices
        moGamesAssigned = defaultdict(list)
        tuGamesAssigned = defaultdict(list)
        moPracticesAssigned = defaultdict(list)
        tuPracticesAssigned = defaultdict(list)
        # if time.time() - startTime > 5:
        #     print("No Valid Schedule Found")
        #     break

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
                if (slot.day == "MO") or (slot.day == "TU" and slot.startTime != "11:00"):
                    # Remove games that fail partial constraints
                    for game in list(slot.games):
                        if not partConstr(newFact, slot):
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
                        if partConstr(newFact, slot):
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
                        if not partConstr(newFact, slot):
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
                        if partConstr(newFact, slot):
                            assignedPractice.add(ranPractice)
                            if slot.day == "MO" and ranPractice not in moPracticesAssigned[slot.startTime]:
                                moPracticesAssigned[slot.startTime].append(ranPractice)
                            elif slot.day == "TU" and ranPractice not in tuPracticesAssigned[slot.startTime]:
                                tuPracticesAssigned[slot.startTime].append(ranPractice)
                        else:
                            slot.practices.discard(ranPractice)
                            assignedPractice.discard(ranPractice)
                        availablePractice.remove(ranPractice)
            
        # for slot in newFact.gameslots + newFact.practiceslots:
        #     if(isinstance(slot, GameSlot)):
        #         print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
        #         print(slot.games)
        #     else:
        #         print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")
        #         print(slot.practices)
        if constr(newFact):
            break  # Exit inner loop if constraints are satisfied
        else:
            # If constraints are not satisfied, reset 'fact' to DEFAULTFACT and retry
            fact = DEFAULTFACT

    # for slot in newFact.gameslots + newFact.practiceslots:
    #     if isinstance(slot, GameSlot):
    #         if slot.day in {"WE", "FR"}:
    #             for game in moGamesAssigned[slot.startTime]:
    #                 slot.addGame(game)
    #         elif slot.day == "TH":
    #             for game in tuGamesAssigned[slot.startTime]:
    #                 slot.addGame(game)
    #     else:
    #         if slot.day == "WE":
    #             for practice in moPracticesAssigned[slot.startTime]:
    #                 slot.addPractice(practice)
    #         elif slot.day == "TH":
    #             for practice in tuPracticesAssigned[slot.startTime]:
    #                 slot.addPractice(practice)

    return newFact

#regex to have practices and games have the same team name to find overlap easier
def normalize_set(slot_set):
    return {re.sub(r"(PRC|OPN) (0[1-9]|[1-9][0-9])", "", item).strip() for item in slot_set}


def specialBookingsChecker(team_dict, isPractice):
    special_game_bookings = {'CMSA U12T1', 'CMSA U13T1'}
    special_practice_bookings = {"CMSA U12T1S", "CMSA U13T1S"}

    keyWords = special_game_bookings

    if isPractice:
        keyWords = special_practice_bookings

    for slots, teams in team_dict.items():
        combined_teams = teams["games"].union(teams["practices"])
        for team in combined_teams:
            for special_teams in keyWords:
                if team in special_teams:
                    return True
                
    return False

def partConstr(fact, slot):    
    #Checking if game max or practice max has been reached
    if isinstance(slot, GameSlot):
        if len(slot.games) > slot.max:
            return False
    else:
        if len(slot.practices) > slot.max:
            return False

    #Dictionary where key is a timeslot so that we can look at practices as well as games for a given slot
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
    special_game_bookings_exists = specialBookingsChecker(team_dict, False)
    special_practice_bookings_exists = specialBookingsChecker(team_dict, True)
    u13_pair = {"CMSA U13T1S", "CMSA U13T1"}
    u12_pair = {"CMSA U12T1S", "CMSA U12T1"}

    #iterating through every time slot and seeing what practices and games are inside
    #checking which hard constraints will fail
    for time_slot, teams in team_dict.items():
        #removing extras from the team names such as prc 01 and opn 01 so that we can find overlap between games and practices
        overlap = normalize_set(teams["games"]).intersection(normalize_set(teams["practices"]))
        combined_teams = teams["games"].union(teams["practices"])
        day, time = time_slot.split(" ")

        # DIV 9 are all evening
        if  [name for name in combined_teams if re.search(r'\bDIV 9\d+\b', name)]:
            if time > "18:00":
                #print("Part Evening")
                return False

        # No games Tuesday 11-12:30
        if day == "TU" and "11:00" <= time <= "12:30":
            if teams["games"]:
                #print("Part Game on Tues 11")
                return False

        # Check not compatible set
        for sets in not_compatible:
            if all(team in teams["games"] for team in sets) or all(team in teams["practices"] for team in sets):
                #print("Part Not Compatible")
                return False

        # Same team assigned game and practice on same day and time
        if overlap:
            #print("Part Overlap")
            return False

        # Check unwanted set
        if time_slot in unwanted:
            if combined_teams.intersection(unwanted[time_slot]):
                #print("Part Unwanted")
                return False
    
        # U15/U16/U17/U19 cant be in same game slots
        keywords = {"U15", "U16", "U17", "U19"}
        keyword_overlap = [team for team in teams["games"] if any(keyword in team for keyword in keywords)]
        if len(keyword_overlap) > 1:
            #print("Part U15..")
            return False
    
        #CMSA U12 T1S and CMSA U13 T1S must be scheduled for pracice on tues thurs 6-7
        if special_game_bookings_exists:
            if special_practice_bookings_exists:
                u13_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u13_pair)]
                u12_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u12_pair)]
                special_practices_in_this_slot= [team for team in teams["practices"] if any(keyword in team for keyword in {"CMSA U12T1S", "CMSA U13T1S"})]     
                if (day == "TU" or day == "TH") and (time == "18:00"):
                    if len(special_practices_in_this_slot) == 0:
                        #print("Part Special")
                        return False
                else:
                    if len(special_practices_in_this_slot) > 0:
                        #print("Part Special")
                        return False
                    
                if len(u12_matching) > 1 or len(u13_matching) > 1:
                    #print("Part Special")
                    return False
    
    #print("Part Passed")
    return True

def constr(fact):
    team_dict = {}
    gamesAssigned = set()
    practiceAssigned = set()

    if not fact:
        return False

    #check gamesmax and practicemax
    for slot in fact.gameslots + fact.practiceslots:
        time_slot = f"{slot.day} {slot.startTime}"
        if (isinstance(slot, GameSlot)):
            if (slot.getSize() > slot.max):
                #print("Full Game max")
                return False
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["games"].update(slot.games)
            for game in slot.games:
                if game not in gamesAssigned:
                    gamesAssigned.add(game)
                else:
                    #print("Full Unique")
                    return False
        elif (isinstance(slot, PracticeSlot)):
            if (slot.getSize() > slot.max):
                #print("Full Practice Max")
                return False
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["practices"].update(slot.practices)
            for practice in slot.practices:
                if practice not in practiceAssigned:
                    practiceAssigned.add(practice)
                else:
                    #print("Full Unique")
                    return False

    missingGames = set(games) - gamesAssigned
    missingPractice  = set(practices) - practiceAssigned
    if missingGames or missingPractice:
        # print("Full Not all games or practices assigned")
        # print("Missing Games", missingGames)
        # print("Missing Practices", missingPractice)
        return False
    
    #Special practice and special games for last hard constraint for city of calgary
    special_game_bookings_exists = specialBookingsChecker(team_dict, False)
    special_practice_bookings_exists = specialBookingsChecker(team_dict, True)
    u13_pair = {"CMSA U13T1S", "CMSA U13T1"}
    u12_pair = {"CMSA U12T1S", "CMSA U12T1"}

    #iterating through every time slot and seeing what practices and games are inside
    #checking which hard constraints will fail
    for time_slot, teams in team_dict.items():
        #removing extras from the team names such as prc 01 and opn 01 so that we can find overlap between games and practices
        overlap = normalize_set(teams["games"]).intersection(normalize_set(teams["practices"]))
        combined_teams = teams["games"].union(teams["practices"])
        day, time = time_slot.split(" ")

        # DIV 9 are all evening
        if  [name for name in combined_teams if re.search(r'\bDIV 9\d+\b', name)]:
            if time > "18:00":
                #print("Full evening")
                return False

        # No games Tuesday 11-12:30
        if day == "TU" and "11:00" <= time <= "12:30":
            if teams["games"]:
                #print("Full game Tues")
                return False

        # Check not compatible set
        for sets in not_compatible:
            if all(team in teams["games"] for team in sets) or all(team in teams["practices"] for team in sets):
                #print("Full not comp") 
                return False

        # Same team assigned game and practice on same day and time
        if overlap:
            #print("Full overlap")
            return False

        # Check unwanted set
        if time_slot in unwanted:
            if combined_teams.intersection(unwanted[time_slot]):
                #print("Full unwanted")
                return False
    
        # U15/U16/U17/U19 cant be in same game slots
        keywords = {"U15", "U16", "U17", "U19"}
        keyword_overlap = [team for team in teams["games"] if any(keyword in team for keyword in keywords)]
        if len(keyword_overlap) > 1:
            #print("Full U15...")
            return False
    
        #CMSA U12 T1S and CMSA U13 T1S must be scheduled for pracice on tues thurs 6-7
        if special_game_bookings_exists:
            if special_practice_bookings_exists:
                u13_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u13_pair)]
                u12_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u12_pair)]
                special_practices_in_this_slot= [team for team in teams["practices"] if any(keyword in team for keyword in {"CMSA U12T1S", "CMSA U13T1S"})]     
                if (day == "TU" or day == "TH") and (time == "18:00"):
                    if len(special_practices_in_this_slot) == 0:
                        #print("Full Special")
                        return False
                else:
                    if len(special_practices_in_this_slot) > 0:
                        #print("Full Special")
                        return False
                    
                if len(u12_matching) > 1 or len(u13_matching) > 1:
                    #print("Full Special")
                    return False
    #print("Full Passed")
    return True

def SetbasedAI():
    FACTS = []
    keeps = 5
    numGen = 10
    generation = 0
    initialScheduleCount = 20

    if not verifyInput():
        return
    if not addPartialAssign():
        return
    
    #rng creating schedules and keeping the 5 best
    for i in range(initialScheduleCount):
        test = OrTree(DEFAULTFACT, games, practices)
        test.eval = Eval(test, wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin, preferences, pair, pennotpaired, pensection)
        FACTS.append(test)
        print(test.eval)
    FACTS.sort(key=lambda x: x.eval)
    Delete(FACTS, keeps)

    while generation < numGen:
        print(f"Generations: {generation}/{numGen}")
        #go through each schedule that was kept and mutate or cross all of them
        #only keep the 5 best for the next generation
        for i in range(len(FACTS)):
            mutOrCross = random.randint(0, 1)
            if mutOrCross == 0:
                mutFact = Mutation(FACTS[i])
                fixedMutFact = OrTree(mutFact, games, practices)
                fixedMutFact.eval = Eval(fixedMutFact, wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin, preferences, pair, pennotpaired, pensection)
                print(fixedMutFact.eval)
                FACTS.append(fixedMutFact)
            else:
                #cross the current schedule with the best schedule
                if i == 0:
                    crossFact1, crossFact2 = Cross(FACTS[0], random.choice(FACTS))
                else:
                    crossFact1, crossFact2 = Cross(FACTS[i], FACTS[0])

                fixedCrossFact1 = OrTree(crossFact1, games, practices)
                fixedCrossFact2 = OrTree(crossFact2, games, practices)
                fixedCrossFact1.eval = Eval(fixedCrossFact1, wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin, preferences, pair, pennotpaired, pensection)
                fixedCrossFact2.eval = Eval(fixedCrossFact2, wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin, preferences, pair, pennotpaired, pensection)
                print(fixedCrossFact2.eval, fixedCrossFact1.eval)
                FACTS.append(fixedCrossFact1)
                FACTS.append(fixedCrossFact2)
        FACTS.sort(key=lambda x: x.eval)
        if len(FACTS) > keeps:
            Delete(FACTS, keeps)
        generation += 1
    return FACTS

facts = SetbasedAI()
if facts:
    print(f"Eval Value: {facts[0].eval}")
    
    # Combine and sort games and practices directly
    sorted_names = []
    
    # Collect games and practices together
    for game_slot in facts[0].gameslots:
        sorted_names.extend(game_slot.games)
    for practice_slot in facts[0].practiceslots:
        sorted_names.extend(practice_slot.practices)

    # Sort the combined names alphabetically
    sorted_names.sort()

    # Use dictionaries to store the day and startTime info for faster lookup
    slot_info = {}

    # Populate the dictionary with game slot information
    for game_slot in facts[0].gameslots:
        for game in game_slot.games:
            slot_info[game] = (game_slot.day, game_slot.startTime)

    # Populate the dictionary with practice slot information
    for practice_slot in facts[0].practiceslots:
        for practice in practice_slot.practices:
            slot_info[practice] = (practice_slot.day, practice_slot.startTime)

    # Print the results
    for name in sorted_names:
        if name in slot_info:
            day, start_time = slot_info[name]
            print(f"{name} : {day}, {start_time}")