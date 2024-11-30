from InputParser import parse_input_file
from Slots import GameSlot, PracticeSlot
import random

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
        else:
            schedule.addGame(partial_assignments[key][0])
        del partial_assignments[key]

# fact = [slots_array]

# Manually constructed `fact` array
fact = [[
    # Game slots with violations
    GameSlot(4, 1, "MO", "10:00"),  # Max = 2
    GameSlot(5, 1, "WE", "10:00"),  # Max = 3
    GameSlot(4, 1, "MO", "18:00"),
    GameSlot(4, 1, "TH", "18:30"),
    GameSlot(5, 1, "TU", "11:00"), 
    
    # Practice slots with violations
    PracticeSlot(4, 1, "MO", "10:00"),  # Max = 2
    PracticeSlot(4, 1, "WE", "09:00"),  # Max = 1
    PracticeSlot(4, 1, "WE", "19:00"),
    PracticeSlot(4, 1, "TU", "18:00"),
    PracticeSlot(4, 1, "TH", "18:00"),
]]

# Adding games/practices to create violations
fact[0][0].addGame("Team1")
fact[0][0].addGame("Team2")
fact[0][0].addGame("Team3")  # Exceeds max for MO 10:00

fact[0][2].addGame("CMSA U17T1 DIV 05")
fact[0][2].addGame("CMSA U12T3 DIV 01")
fact[0][2].addGame("CUSA O18 DIV 01")  # Exceeds max for MO 10:00

fact[0][3].addGame("CMSA U15T3 DIV 03")
fact[0][3].addGame("Team2")
fact[0][3].addGame("Team3")  # Exceeds max for MO 10:00

fact[0][4].addGame("Team1")
fact[0][4].addGame("Team2")
fact[0][4].addGame("Team3")

fact[0][1].addGame("CMSA U13T1 DIV 01")
fact[0][1].addGame("CMSA U12T1S DIV 09")
fact[0][1].addGame("Team6")
fact[0][1].addGame("Team7")  # Exceeds max for WE 10:00

fact[0][5].addPractice("Team1")
fact[0][5].addPractice("Team2")
fact[0][5].addPractice("Team3")  # Exceeds max for MO 09:00

fact[0][6].addPractice("CMSA U12T1S")
fact[0][6].addPractice("Team5")  # Exceeds max for WE 09:00

fact[0][7].addPractice("CMSA U17T1 DIV 09")
fact[0][7].addPractice("CMSA U13T3 DIV 09")  # Exceeds max for WE 09:00

fact[0][8].addPractice("CMSA U12T1S")
fact[0][9].addPractice("CMSA U12T1S")


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

def OrTree(fact, games, practices):
    assigned = set()
    finished = False
    index = 0
    if constr(fact):
        return fact
    else:
        while(not constr(fact)):
            while((not (len(assigned) < len(games) + len(practices))) and 
                (not finished)):
                
                return


def partConstr(assignment, fact):
    #take either game slot or practice slot, and check if it is valid
    #if jungsu makes or tree auto fill mon, wed, fr or tue, thur for practice and games,
    #this func is fucking useless
    return

def constr(fact):
    
    team_dict = {}
    #take schedule(fact), and check if schedule is valid
    #check gamesmax and practicemax (DONE)
    for slot in fact[0]:
        time_slot = f"{slot.day} {slot.startTime}"
        if (isinstance(slot, GameSlot)):
            if (slot.getSize() > slot.max):
                print("OVER GAME MAX")
                return False
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["games"].update(slot.games)
        elif (isinstance(slot, PracticeSlot)):
            if (slot.getSize() > slot.max):
                print("OVER PRACTICE MAX")
                return False
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["practices"].update(slot.practices)
            
    for i in team_dict.items():
        print(i)
    
    target_teams = {'CMSA U12T1', 'CMSA U13T1'}
    teams_exists = any(any(game.startswith(base) for base in target_teams) for _, activities in team_dict.items() for game in activities['practices'] | activities['games'])
    
    
    special_teams = {"CMSA U12T1S", "CMSA U13T1S"}
    u13_pair = {"CMSA U13T1S", "CMSA U13T1"}
    u12_pair = {"CMSA U12T1S", "CMSA U12T1"}
    special_exists = any(any(game.startswith(base) for base in special_teams) for _, activities in team_dict.items() for game in activities['practices'] | activities['games'])
    #same team assigned game and practice on same day and time (DONE)
    #check not compatible set (DONE)
        #cant have it on same slot
    #check unwanted set, no games or practice for that team (DONE)
    #DIV 9 are all evening (DONE)
    #no games tues 11-12:30 (DONE)
    for time_slot, teams in team_dict.items():
        overlap = teams["games"].intersection(teams["practices"])
        combined_teams = teams["games"].union(teams["practices"])
        day, time = time_slot.split(" ")
        hour, minute = time.split(":")
        hour = int(hour)
        minute = int(minute)
        if hour <= 18:
            div9_exists = [name for name in combined_teams if 'DIV 09' in name]
            if div9_exists:
                print("DIV 09 in morning/afternoon slots")
                return False
        if day == "TU":
            tuesday_games = teams["games"]
            if tuesday_games:
                print("Tuesday game 11-12:30 not allowed")
                return False
        for sets in not_compatible:
            if all(teams in combined_teams for teams in sets):
                print(f"Teams {', '.join(sets)} are scheduled on {time_slot}")
                return False
        if  overlap:
            print("OVERLAP OF GAMES")
            return False
        if time_slot in unwanted:
            overlap = combined_teams.intersection(unwanted[time_slot])
            if overlap:
                print(f"UNWANTED CONSTRAINT: {', '.join(overlap)} are in the unwanted list for {time_slot}")
                return False
    # if a team has a game on monday, they need to have it on wed and fri (DONE)
    # same for tuesday and thurs (DONE)
    # practice monday, wed (DONE)
    # practice tues, thur (DONE)
    
    # U15/U16/U17/U19 cant be in same game slots (DONE)
        keywords = {"U15", "U16", "U17", "U19"}
        keyword_overlap = [team for team in teams["games"] if any(keyword in team for keyword in keywords)]
        if len(keyword_overlap) > 1:
            print("U15... Overlap")
            print(keyword_overlap)
            return False
    
    #CMSA U12 T1S and CMSA U13 T1S must be scheduled for pracice on tues thurs 6-7
        if teams_exists:
            if special_exists:
                u13_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u13_pair)]
                u12_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in u12_pair)]
                print(u13_matching)
                print(u12_matching)
                special_teams_exists = [team for team in teams["practices"] if any(keyword in team for keyword in special_teams)]     
                if (day == "TU" or day == "TH") and (hour == 18 and minute == 0):
                    if len(special_teams_exists) == 0:
                        print("SPECIAL TEAM NOT IN SLOT")
                        return False
                else:
                    if len(special_teams_exists) > 0:
                        print("SPECIAL TEAM IN WRONG SLOT")
                        return False
                if len(u12_matching) > 1 or len(u13_matching) > 1:
                    print("SPECIAL TEAMS OVERLAP")
                    return False
                
    #CMSA U12T1S cant be in the same slot with CMSA U12T1 (DONE)
    #CMSA U13T1S cant be in the same slot with CMSA U13T1 (DONE)
    print("TEST PASSED")
    return True

constr(fact)

# OrTree(fact, games, practices)