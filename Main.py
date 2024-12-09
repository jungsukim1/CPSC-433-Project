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

# Function to create the Game and Practice Slots
def create_game_and_practice_slots(game_slots, practice_slots):

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

# Function to Verify the Inputs
def verifyInput():
    gamesTotal = 0
    practiceTotal = 0

    for slot in game_slots:
        gamesTotal += game_slots[slot]['max']
    for slot in practice_slots:
        practiceTotal += practice_slots[slot]['max']

    # No Games and Practices were given in the input
    if not games and not practices:
        print("No games and practices")
        return False
    # No Games Slots and Practice Slots were given
    if not game_slots and practice_slots:
        print("No game slots and practice slots")
        return False
    # Games were given but no Game Slots
    if games and not game_slots:
        print("Games exist but no slots")
        return False
    # Practices were given but no Practice Slots
    if practices and not practice_slots:
        print("Practice exist but no slots")
        return False
    # Special Teams were requested but no slots
    if any('CMSA U12T1' in game for game in games) or any('CMSA U13T1' in game for game in games):
        if not any(
            schedule.day == "TU" and schedule.startTime == "18:00" and isinstance(schedule, PracticeSlot)
            for schedule in DEFAULTFACT.practiceslots
        ):
            print("No Special Team Slot Exist!")
            return False
    # Too many games for Slots
    if len(games) > gamesTotal:
        print("Not enough Game slots")
        return False
    # Too many practices for Slots
    if len(practices) > practiceTotal:
        print("Not enough Practice slots")
        return False
    return True


# Create GameSlot and PracticeSlot objects
game_slot_objects, practice_slot_objects = create_game_and_practice_slots(game_slots, practice_slots)

# Create the first schedule object
DEFAULTFACT = Schedule([], [])

# Array to keep track of the partial assignments
PARTIAL_ASSIGNMENTS = []

# Append all GameSlot objects to the array
for game_slot in game_slot_objects.values():
    DEFAULTFACT.addGameSlot(game_slot)

# Append all PracticeSlot objects to the array
for practice_slot in practice_slot_objects.values():
    DEFAULTFACT.addPracticeSlot(practice_slot)

# Adds the Partial Assignments into the first schedule
def addPartialAssign():        
    gamesTotal = 0  # Counter for the total number of game slots
    practiceTotal = 0  # Counter for the total number of practice slots

    # Iterate through all the slots (both games and practices)
    for schedule in DEFAULTFACT.gameslots + DEFAULTFACT.practiceslots:
        key = f"{schedule.day} {schedule.startTime}"  # Unique key for each schedule based on day and time
        
        # If the slot is a PracticeSlot
        if isinstance(schedule, PracticeSlot):
            practiceTotal += schedule.max
            # Check if there is a partial assignment for this slot
            if key in partial_assignments and partial_assignments[key]:
                # Ensure the assignment is a practice-related assignment
                if "PRC" in partial_assignments[key][0] or "OPN" in partial_assignments[key][0]:
                    schedule.addPractice(partial_assignments[key][0])  # Assign the practice
                    # Add the practice to the list of partial assignments if not already added
                    if partial_assignments[key][0] not in PARTIAL_ASSIGNMENTS:
                        PARTIAL_ASSIGNMENTS.append(partial_assignments[key][0])
                    # Remove the assigned practice from the partial_assignments dictionary
                    del partial_assignments[key]
        
        # If the slot is a GameSlot
        else:
            gamesTotal += schedule.max
            # Check if there is a partial assignment for this slot
            if key in partial_assignments and partial_assignments[key]:
                # Ensure the assignment is a game-related assignment
                if "PRC" not in partial_assignments[key][0] or "OPN" not in partial_assignments[key][0]:
                    schedule.addGame(partial_assignments[key][0])  # Assign the game
                    # Add the game to the list of partial assignments if not already added
                    if partial_assignments[key][0] not in PARTIAL_ASSIGNMENTS:
                        PARTIAL_ASSIGNMENTS.append(partial_assignments[key][0])
                    # Remove the assigned game from the partial_assignments dictionary
                    del partial_assignments[key]
        
        # Handle specific scheduling rules for Tuesday at 18:00 for PracticeSlots
        if (schedule.day == "TU" and schedule.startTime == "18:00" and isinstance(schedule, PracticeSlot)):
            # Assign specific practices based on the presence of certain game identifiers
            if any('CMSA U12T1' in game for game in games):
                if 'CMSA U12T1S' not in PARTIAL_ASSIGNMENTS:
                    PARTIAL_ASSIGNMENTS.append('CMSA U12T1S')  # Add to partial assignments if not present
                schedule.addPractice('CMSA U12T1S')  # Assign the specific practice
            if any('CMSA U13T1' in game for game in games):
                if 'CMSA U13T1S' not in PARTIAL_ASSIGNMENTS:
                    PARTIAL_ASSIGNMENTS.append('CMSA U13T1S')  # Add to partial assignments if not present
                schedule.addPractice('CMSA U13T1S')  # Assign the specific practice

    return True

def OrTree(fact, games, practices):
    # If no fact is provided, use the default fact
    if fact == None:
        fact = DEFAULTFACT

    # Filter out any games or practices already assigned
    games = [game for game in games if game not in PARTIAL_ASSIGNMENTS]
    practices = [practice for practice in practices if practice not in PARTIAL_ASSIGNMENTS]

    # If the initial fact satisfies the constraints, return it
    if constr(fact):
        return fact

    # Loop until a valid schedule is found
    while True:
        # Create a deep copy of the fact to work with
        tempFact = copy.deepcopy(fact)
        # Initialize a new Schedule object to hold the updated schedule
        newFact = Schedule([], [])  
        # Initialize sets to track assigned games and practices
        assignedGames = set()  
        assignedPractice = set()  
        moGamesAssigned = defaultdict(list)
        tuGamesAssigned = defaultdict(list)
        moPracticesAssigned = defaultdict(list)
        tuPracticesAssigned = defaultdict(list)

        # Process all game and practice slots in the schedule
        while tempFact.gameslots or tempFact.practiceslots:
            # Combine game and practice slots into a single list
            combined_slots = tempFact.gameslots + tempFact.practiceslots
            # Randomly select a slot to process
            slot = random.choice(combined_slots)  
            
            if isinstance(slot, GameSlot):  # If it's a game slot
                tempFact.removeSpecificGameSlot(slot)
                # Add the game slot to the new schedule if not already added
                if slot not in newFact.gameslots:
                    newFact.addGameSlot(slot)
            else:  # If it's a practice slot
                tempFact.removeSpecificPracticeSlot(slot)
                # Add the practice slot to the new schedule if not already added
                if slot not in newFact.practiceslots:
                    newFact.addPracticeSlot(slot)

            # Process game slots
            if isinstance(slot, GameSlot):
                if (slot.day == "MO") or (slot.day == "TU" and slot.startTime != "11:00"):
                    # Remove games that fail the partial constraints
                    for game in list(slot.games):
                        if not partConstr(newFact, slot):
                            assignedGames.discard(game)
                            slot.games.discard(game)
                            # Remove from the assigned games based on day and time
                            if slot.day == "MO" and game in moGamesAssigned[slot.startTime]:
                                moGamesAssigned[slot.startTime].remove(game)
                            elif slot.day == "TU" and game in tuGamesAssigned[slot.startTime]:
                                tuGamesAssigned[slot.startTime].remove(game)
                        else:
                            # Track assigned games by day and time
                            if slot.day == "MO" and game not in moGamesAssigned[slot.startTime]:
                                moGamesAssigned[slot.startTime].append(game)
                            elif slot.day == "TU" and game not in tuGamesAssigned[slot.startTime]:
                                tuGamesAssigned[slot.startTime].append(game)
                    
                    # Assign available games to the slot
                    availableGames = [g for g in games if g not in assignedGames]
                    while slot.getSize() < slot.max and availableGames:
                        ranGame = random.choice(availableGames)
                        slot.addGame(ranGame)
                        # Check if the game satisfies the constraints
                        if partConstr(newFact, slot):
                            assignedGames.add(ranGame)
                            # Track the assigned game by day and time
                            if slot.day == "MO" and ranGame not in moGamesAssigned[slot.startTime]:
                                moGamesAssigned[slot.startTime].append(ranGame)
                            elif slot.day == "TU" and ranGame not in tuGamesAssigned[slot.startTime]:
                                tuGamesAssigned[slot.startTime].append(ranGame)
                        else:
                            # Remove the game if constraints are not met
                            slot.games.discard(ranGame)
                            assignedGames.discard(ranGame)
                        availableGames.remove(ranGame)

            # Process practice slots
            else:
                if slot.day in {"MO", "TU", "FR"}:
                    # Remove practices that fail the partial constraints
                    for practice in list(slot.practices):
                        if not partConstr(newFact, slot):
                            assignedPractice.discard(practice)
                            slot.practices.discard(practice)
                            # Remove from assigned practices based on day and time
                            if slot.day == "MO" and practice in moPracticesAssigned[slot.startTime]:
                                moPracticesAssigned[slot.startTime].remove(practice)
                            elif slot.day == "TU" and practice in tuPracticesAssigned[slot.startTime]:
                                tuPracticesAssigned[slot.startTime].remove(practice)
                        else:
                            # Track assigned practices by day and time
                            if slot.day == "MO" and practice not in moPracticesAssigned[slot.startTime]:
                                moPracticesAssigned[slot.startTime].append(practice)
                            elif slot.day == "TU" and practice not in tuPracticesAssigned[slot.startTime]:
                                tuPracticesAssigned[slot.startTime].append(practice)

                    # Assign available practices to the slot
                    availablePractice = [p for p in practices if p not in assignedPractice]
                    while slot.getSize() < slot.max and availablePractice:
                        ranPractice = random.choice(availablePractice)
                        slot.addPractice(ranPractice)
                        # Check if the practice satisfies the constraints
                        if partConstr(newFact, slot):
                            assignedPractice.add(ranPractice)
                            # Track the assigned practice by day and time
                            if slot.day == "MO" and ranPractice not in moPracticesAssigned[slot.startTime]:
                                moPracticesAssigned[slot.startTime].append(ranPractice)
                            elif slot.day == "TU" and ranPractice not in tuPracticesAssigned[slot.startTime]:
                                tuPracticesAssigned[slot.startTime].append(ranPractice)
                        else:
                            # Remove the practice if constraints are not met
                            slot.practices.discard(ranPractice)
                            assignedPractice.discard(ranPractice)
                        availablePractice.remove(ranPractice)

        # If constraints are satisfied for the new schedule, exit the loop
        if constr(newFact):
            break
        else:
            # If constraints are not met, reset and retry
            fact = DEFAULTFACT

    return newFact  # Return the newly generated schedule

# Normalize the set of team names by removing practice or open identifiers for easier overlap checks
def normalize_set(slot_set):
    # Use regex to strip "PRC" or "OPN" prefixes and any associated numbers from team names
    return {re.sub(r"(PRC|OPN) (0[1-9]|[1-9][0-9])", "", item).strip() for item in slot_set}

# Check if there are any special bookings for games or practices
def specialBookingsChecker(team_dict, isPractice):
    # Define special game and practice bookings
    special_game_bookings = {'CMSA U12T1', 'CMSA U13T1'}
    special_practice_bookings = {"CMSA U12T1S", "CMSA U13T1S"}

    # Determine which set of keywords to use based on whether checking practices or games
    keyWords = special_game_bookings
    if isPractice:
        keyWords = special_practice_bookings

    # Iterate through each slot and its associated teams
    for slots, teams in team_dict.items():
        # Combine all teams from games and practices for this slot
        combined_teams = teams["games"].union(teams["practices"])
        for team in combined_teams:
            # Check if any team matches the special bookings
            for special_teams in keyWords:
                if team in special_teams:
                    return True  # Special booking found

    return False  # No special booking found

# Function that only checks the constraints for the current slot
def partConstr(fact, slot):    
    # Check if the number of games or practices exceeds the slot's maximum capacity
    if isinstance(slot, GameSlot):
        if len(slot.games) > slot.max:
            return False
    else:
        if len(slot.practices) > slot.max:
            return False

    # Create a dictionary to organize teams by time slot, combining games and practices
    team_dict = {}
    for slot in fact.gameslots + fact.practiceslots:
        time_slot = f"{slot.day} {slot.startTime}"
        if isinstance(slot, GameSlot):
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["games"].update(slot.games)
        elif isinstance(slot, PracticeSlot):
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["practices"].update(slot.practices)

    # Check for the existence of special bookings
    special_game_bookings_exists = specialBookingsChecker(team_dict, False)
    special_practice_bookings_exists = specialBookingsChecker(team_dict, True)

    # Define specific team pairs for scheduling rules
    u13_pair = {"CMSA U13T1S", "CMSA U13T1"}
    u12_pair = {"CMSA U12T1S", "CMSA U12T1"}

    # Iterate through each time slot and validate hard constraints
    for time_slot, teams in team_dict.items():
        # Remove extras like "PRC" or "OPN" to find overlapping teams
        overlap = normalize_set(teams["games"]).intersection(normalize_set(teams["practices"]))
        combined_teams = teams["games"].union(teams["practices"])
        day, time = time_slot.split(" ")

        # Division 9 teams must play only in the evening
        if [name for name in combined_teams if re.search(r'\bDIV 9\d+\b', name)]:
            if time > "18:00":
                return False

        # No games allowed on Tuesdays from 11:00 to 12:30
        if day == "TU" and "11:00" <= time <= "12:30":
            if teams["games"]:
                return False

        # Teams in the same "not compatible" set cannot play/practice together
        for sets in not_compatible:
            if all(team in teams["games"] for team in sets) or all(team in teams["practices"] for team in sets):
                return False

        # A team cannot have a game and practice at the same time
        if overlap:
            return False

        # Unwanted teams cannot be scheduled in specific time slots
        if time_slot in unwanted:
            if combined_teams.intersection(unwanted[time_slot]):
                return False

        # U15, U16, U17, and U19 teams cannot share the same game slot
        keywords = {"U15", "U16", "U17", "U19"}
        keyword_overlap = [team for team in teams["games"] if any(keyword in team for keyword in keywords)]
        if len(keyword_overlap) > 1:
            return False

        # CMSA U12T1S and CMSA U13T1S practices must be on Tuesday/Thursday 6-7 pm only
        if special_game_bookings_exists:
            if special_practice_bookings_exists:
                u13_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u13_pair)]
                u12_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u12_pair)]
                special_practices_in_this_slot = [team for team in teams["practices"] if any(keyword in team for keyword in {"CMSA U12T1S", "CMSA U13T1S"})]
                if (day == "TU" or day == "TH") and (time == "18:00"):
                    if len(special_practices_in_this_slot) == 0:
                        return False
                else:
                    if len(special_practices_in_this_slot) > 0:
                        return False

                # Ensure no duplicate bookings for U12 and U13 teams
                if len(u12_matching) > 1 or len(u13_matching) > 1:
                    return False

    # All constraints passed
    return True

def constr(fact):
    # Initialize dictionaries to track team assignments and sets for games and practices
    team_dict = {}
    gamesAssigned = set()
    practiceAssigned = set()

    # If no fact data is provided, return False
    if not fact:
        return False

    # Check if the maximum number of games and practices in each slot is not exceeded
    for slot in fact.gameslots + fact.practiceslots:
        time_slot = f"{slot.day} {slot.startTime}"

        # Handle GameSlots
        if isinstance(slot, GameSlot):
            if slot.getSize() > slot.max:
                return False  # Maximum number of games exceeded
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["games"].update(slot.games)
            for game in slot.games:
                if game not in gamesAssigned:
                    gamesAssigned.add(game)
                else:
                    return False  # Game is assigned more than once

        # Handle PracticeSlots
        elif isinstance(slot, PracticeSlot):
            if slot.getSize() > slot.max:
                return False  # Maximum number of practices exceeded
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["practices"].update(slot.practices)
            for practice in slot.practices:
                if practice not in practiceAssigned:
                    practiceAssigned.add(practice)
                else:
                    return False  # Practice is assigned more than once

    # Ensure all games and practices are assigned
    missingGames = set(games) - gamesAssigned
    missingPractice = set(practices) - practiceAssigned
    if missingGames or missingPractice:
        return False  # Some games or practices are missing

    # Check special booking constraints for the city of Calgary
    special_game_bookings_exists = specialBookingsChecker(team_dict, False)
    special_practice_bookings_exists = specialBookingsChecker(team_dict, True)
    u13_pair = {"CMSA U13T1S", "CMSA U13T1"}
    u12_pair = {"CMSA U12T1S", "CMSA U12T1"}

    # Iterate through each time slot and validate hard constraints
    for time_slot, teams in team_dict.items():
        # Remove extras (e.g., "PRC", "OPN") from team names to find overlap between games and practices
        overlap = normalize_set(teams["games"]).intersection(normalize_set(teams["practices"]))
        combined_teams = teams["games"].union(teams["practices"])
        day, time = time_slot.split(" ")

        # Division 9 teams must be scheduled in the evening
        if [name for name in combined_teams if re.search(r'\bDIV 9\d+\b', name)]:
            if time > "18:00":
                return False  # Division 9 teams can't be scheduled after evening

        # No games allowed on Tuesdays from 11:00 to 12:30
        if day == "TU" and "11:00" <= time <= "12:30":
            if teams["games"]:
                return False  # Games should not be scheduled in this time window

        # Check for "not compatible" sets (teams that can't be scheduled together)
        for sets in not_compatible:
            if all(team in teams["games"] for team in sets) or all(team in teams["practices"] for team in sets):
                return False  # Not compatible teams in the same time slot

        # Prevent assigning the same team to both game and practice in the same time slot
        if overlap:
            return False

        # Prevent assigning unwanted teams to specific time slots
        if time_slot in unwanted:
            if combined_teams.intersection(unwanted[time_slot]):
                return False  # Unwanted teams should not be scheduled in this slot

        # U15, U16, U17, and U19 teams cannot be assigned to the same game slot
        keywords = {"U15", "U16", "U17", "U19"}
        keyword_overlap = [team for team in teams["games"] if any(keyword in team for keyword in keywords)]
        if len(keyword_overlap) > 1:
            return False  # Multiple teams from the same age group shouldn't be scheduled together

        # CMSA U12T1S and CMSA U13T1S must be scheduled for practice on Tuesday/Thursday 6-7 pm only
        if special_game_bookings_exists:
            if special_practice_bookings_exists:
                u13_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u13_pair)]
                u12_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u12_pair)]
                special_practices_in_this_slot = [team for team in teams["practices"] if any(keyword in team for keyword in {"CMSA U12T1S", "CMSA U13T1S"})]
                if (day == "TU" or day == "TH") and (time == "18:00"):
                    if len(special_practices_in_this_slot) == 0:
                        return False  # Ensure practice is scheduled on the correct day and time
                else:
                    if len(special_practices_in_this_slot) > 0:
                        return False  # Ensure practice is not scheduled outside the allowed time window

                # Prevent multiple assignments of U12 and U13 teams in the same slot
                if len(u12_matching) > 1 or len(u13_matching) > 1:
                    return False

    # If no constraints are violated, return True
    return True

def SetbasedAI():
    FACTS = []
    keeps = 5
    numGen = 10
    generation = 0
    initialScheduleCount = 20

    if not verifyInput():  # Verify the input
        return
    if not addPartialAssign():  # Add partial assignments
        return
    
    # Generate initial schedules and evaluate them
    for i in range(initialScheduleCount):
        test = OrTree(DEFAULTFACT, games, practices)  # Create new schedule
        test.eval = Eval(test, wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin, preferences, pair, pennotpaired, pensection)  # Evaluate schedule
        FACTS.append(test)
        print(test.eval)  # Print evaluation score of the schedule
    FACTS.sort(key=lambda x: x.eval)  # Sort schedules based on evaluation
    Delete(FACTS, keeps)  # Keep only the top 'keeps' schedules

    # Start the genetic algorithm for the specified number of generations
    while generation < numGen:
        print(f"Generations: {generation}/{numGen}")  # Print current generation
        # Iterate through each schedule and apply mutation or crossover
        for i in range(len(FACTS)):
            mutOrCross = random.randint(0, 1)  # Randomly decide between mutation and crossover
            if mutOrCross == 0:  # Mutation
                mutFact = Mutation(FACTS[i])  # Apply mutation to the schedule
                fixedMutFact = OrTree(mutFact, games, practices)  # Create new schedule after mutation
                fixedMutFact.eval = Eval(fixedMutFact, wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin, preferences, pair, pennotpaired, pensection)  # Evaluate new schedule
                print(fixedMutFact.eval)  # Print evaluation score
                FACTS.append(fixedMutFact)  # Add mutated schedule to the list
            else:  # Crossover
                # Cross current schedule with the best schedule
                if i == 0:
                    crossFact1, crossFact2 = Cross(FACTS[0], random.choice(FACTS))  # Crossover between the best and random schedule
                else:
                    crossFact1, crossFact2 = Cross(FACTS[i], FACTS[0])  # Crossover with the best schedule

                # Create and evaluate the crossed schedules
                fixedCrossFact1 = OrTree(crossFact1, games, practices)
                fixedCrossFact2 = OrTree(crossFact2, games, practices)
                fixedCrossFact1.eval = Eval(fixedCrossFact1, wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin, preferences, pair, pennotpaired, pensection)
                fixedCrossFact2.eval = Eval(fixedCrossFact2, wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin, preferences, pair, pennotpaired, pensection)
                print(fixedCrossFact2.eval, fixedCrossFact1.eval)  # Print evaluation scores of crossed schedules
                FACTS.append(fixedCrossFact1)  # Add crossed schedule to the list
                FACTS.append(fixedCrossFact2)  # Add crossed schedule to the list
        FACTS.sort(key=lambda x: x.eval)  # Sort schedules by evaluation
        if len(FACTS) > keeps:
            Delete(FACTS, keeps)  # Keep only the best 'keeps' schedules
        generation += 1  # Increment generation count
    return FACTS  # Return the final set of best schedules

# Running the SetbasedAI function to generate and evaluate schedules
facts = SetbasedAI()
if facts:
    print(f"Eval Value: {facts[0].eval}")  # Print evaluation score of the best schedule
    
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
            day, start_time = slot_info[name]  # Retrieve the day and time for each game/practice
            print(f"{name} : {day}, {start_time}")  # Print the game/practice with its scheduled day and time