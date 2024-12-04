from InputParser import parse_input_file
from Slots import GameSlot, PracticeSlot

# python Main.py input.txt 1 0 1 0 10 10 10 10

# fact=[
#     GameSlot(4, 1, "Mon","11:00"),
#     PracticeSlot(4, 1, "Tues","11:00")
# ]

# fact[0].addGame("Booking1")
# fact[0].addPractice("Booking2")

(
    game_slots, practice_slots, games, practices, not_compatible,
    unwanted, preferences, pair, partial_assignments, wminfilled, 
    wpref, wpair, wsecdiff, pengamemin, penpracticemin,
    pennotpaired, pensection
    ) = parse_input_file()




def eval_minfilled(fact):
    game_min = game_slots["min"]
    prac_min = practice_slots['min']

    # finding how many games assigned in fact
    game_temp = 0
    for used_game in games:
        if used_game in fact:
            game_temp += 1
    
    # finding how many practices assigned in fact
    prac_temp = 0
    for used_prac in practices:
        if used_prac in fact:
            prac_temp += 1

    game_temp = (game_min - game_temp) * pengamemin
    prac_temp = (prac_min - prac_min) * penpracticemin

    return (game_temp + prac_temp)


def eval_pref(fact):
    pref_val = 0
    
    # checking how many pref is satisfied in fact
    for key, val in preferences.items():
        if key in fact:
            pref_val += val
        else:
            pref_val -= val
        
    return pref_val

# make sure this actually works the way u think it works
def eval_pair(fact):
    
    slot_pair = pair
    val = 0
    team_dict = {}
    for slot in fact:
        time_slot = f"{slot.day} {slot.startTime}"
        if (isinstance(slot, GameSlot)):
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["games"].update(slot.games)
        elif (isinstance(slot, PracticeSlot)):
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["practices"].update(slot.practices)

    for time_slot, teams in team_dict.items():
        combined_teams = teams["games"].union(teams["practices"])
        pair_matching = [team for team in combined_teams if any(keyword.lower() in team.lower() for keyword in slot_pair)]

        # pair not on the same slot
        if len(pair_matching) > 1:
            val += pennotpaired
        
    return val

def eval_secdiff(fact):

    team_dict = {}
    val = 0

    for slot in fact:
        time_slot = f"{slot.day} {slot.startTime}"
        if (isinstance(slot, GameSlot)):
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["games"].update(slot.games)
        elif (isinstance(slot, PracticeSlot)):
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["practices"].update(slot.practices)

    for time_slot, teams in team_dict.items():
        keywords = {} # find out a way to get all unique age/tier
        keyword_overlap = [team for team in teams["games"] if any(keyword in team for keyword in keywords)]
        if len(keyword_overlap) > 1:
            val += pensection

    return val

def Eval(fact):
    
    val = (eval_minfilled(fact) * wminfilled) + (eval_pref(fact) * wpref) + (eval_pair(fact) * wpair) + (eval_secdiff(fact) * wsecdiff)
    
    return val
    
