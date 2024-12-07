from Slots import GameSlot, PracticeSlot
from collections import Counter

def eval_minfilled(fact, pengamemin, penpracticemin):
    game_pen = 0
    practice_pen = 0
    
    for slot in fact.gameslots + fact.practiceslots:
        if isinstance(slot, GameSlot):
            if slot.getSize() < slot.getMin():
                game_pen += pengamemin
        else:
            if slot.getSize() < slot.getMin():
                practice_pen += penpracticemin
    return (game_pen + practice_pen)


def eval_pref(fact, preferences):
    pref_val = 0
    
    for slot in fact.gameslots + fact.practiceslots:
        time_slot = f"{slot.day} {slot.startTime}"
        if isinstance(slot, GameSlot):
            for games in slot.games:
                for pref in preferences[games]:
                    if time_slot != pref[0]:
                        pref_val += pref[1]
                        
        else:
            for practices in slot.practices:
                for pref in preferences[practices]:
                    if time_slot != pref[0]:
                        pref_val += pref[1]
    return pref_val

def eval_pair(fact, pair, pennotpaired):
    slot_pair = pair
    val = 0
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

    for time_slot, teams in team_dict.items():
        combined_teams = teams["games"].union(teams["practices"])
        for pair in slot_pair:
            if (pair[0] in combined_teams) ^ (pair[1] in combined_teams):
                val += pennotpaired 
    return val/2

#sec diff needs to check tier ranges
def eval_secdiff(fact, pensection):

    team_dict = {}
    val = 0

    for slot in fact.gameslots + fact.practiceslots:
        time_slot = f"{slot.day} {slot.startTime}"
        if (isinstance(slot, GameSlot)):
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set()}
            team_dict[time_slot]["games"].update(slot.games)

    for time_slot, teams in team_dict.items():
        overlap_teams = [team.split(" ") for team in teams["games"]]
        
        for i in range(len(overlap_teams)):
            for j in range(i + 1, len(overlap_teams)):
                if overlap_teams[i][1] == overlap_teams[j][1]:
                      if (int(overlap_teams[j][-1]) - int(overlap_teams[i][-1])) == 1:
                        val += pensection               
    return val

def Eval(fact, wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin, preferences, pair, pennotpaired, pensection):
    
    val = ((eval_minfilled(fact, pengamemin, penpracticemin) * wminfilled) + (eval_pref(fact, preferences) * wpref) + 
            (eval_pair(fact, pair, pennotpaired) * wpair) + (eval_secdiff(fact, pensection) * wsecdiff))
    
    return val
    

# print(Eval(fact))