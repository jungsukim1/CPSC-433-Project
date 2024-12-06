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
                # game_slot = f"{time_slot} {games}"
                # pen_val = preferences.get(game_slot)
                # if game_slot in preferences.items():
                #     continue
                # else:
                #     pref_val += pen_val
                if preferences[games]:
                    if time_slot != preferences[games][0]:
                        pref_val += preferences[games][1]
                    # else:
                    #     print(preferences[games], games)
                        
        else:
            for practices in slot.practices:
                if preferences[practices]:
                    if time_slot != preferences[practices][0]:
                        pref_val += preferences[practices][1]
                    # else:
                    #     print(preferences[practices], practices)
                # practice_slot = f"{time_slot} {practices}"
                # pen_val = preferences.get(practice_slot)
                # if practice_slot in preferences.items():
                #     continue
                # else:
                #     pref_val += pen_val
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
        pair_matching = list(slot_pair) if all(team in combined_teams for team in slot_pair) else []
        

        
        if len(pair_matching) < 2:
            val += pennotpaired
        
    # print("Pair Matching", pair_matching)
    return val

def eval_secdiff(fact, pensection):

    team_dict = {}
    val = 0

    for slot in fact.gameslots + fact.practiceslots:
        time_slot = f"{slot.day} {slot.startTime}"
        if (isinstance(slot, GameSlot)):
            if time_slot not in team_dict:
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["games"].update(slot.games)

    for time_slot, teams in team_dict.items():
        overlap_teams = [team.split("DIV")[0].strip() for team in teams["games"]]
        overlap_count = Counter(overlap_teams)
        # duplicate_teams = [team for team, count in overlap_count.items() if count > 1]
        # duplicates = [team for team in teams["games"] if team.split("DIV")[0].strip() in duplicate_teams]
        
        duplicate_teams = []
        for team, count in overlap_count.items():
            if count > 1:
                duplicate_teams.append(team)
                
                
        duplicates = []
        for team in teams["games"]:
            if team.split("DIV")[0].strip() in duplicate_teams:
                duplicates.append(team)
        
        if len(duplicates) > 1:
            val += pensection
            
    # print("Sec Diff", duplicates)
    return val

def Eval(fact, wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin, preferences, pair, pennotpaired, pensection):
    
    val = ((eval_minfilled(fact, pengamemin, penpracticemin) * wminfilled) + (eval_pref(fact, preferences) * wpref) + 
            (eval_pair(fact, pair, pennotpaired) * wpair) + (eval_secdiff(fact, pensection) * wsecdiff))
    
    return val
    

# print(Eval(fact))