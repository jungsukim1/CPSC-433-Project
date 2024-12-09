from Slots import GameSlot, PracticeSlot
from collections import Counter

def eval_minfilled(fact, pengamemin, penpracticemin):
    # Evaluate the penalty for game and practice slots that do not meet their minimum size
    game_pen = 0
    practice_pen = 0
    
    # Loop through all game and practice slots
    for slot in fact.gameslots + fact.practiceslots:
        if isinstance(slot, GameSlot):  # Check if it's a GameSlot
            if slot.getSize() < slot.getMin():  # Check if the size is less than the minimum
                game_pen += pengamemin  # Add penalty for insufficient games
        else:  # It's a PracticeSlot
            if slot.getSize() < slot.getMin():  # Check if the size is less than the minimum
                practice_pen += penpracticemin  # Add penalty for insufficient practices
    return (game_pen + practice_pen)  # Return the total penalty

def eval_pref(fact, preferences):
    # Evaluate the penalty based on the preferences for the scheduled times
    pref_val = 0
    
    # Loop through all game and practice slots
    for slot in fact.gameslots + fact.practiceslots:
        time_slot = f"{slot.day} {slot.startTime}"  # Format time as day and start time
        if isinstance(slot, GameSlot):  # If it's a GameSlot
            for games in slot.games:
                for pref in preferences[games]:  # Check preferences for each game
                    if time_slot != pref[0]:  # If the scheduled time doesn't match the preferred time
                        pref_val += pref[1]  # Add the penalty value from the preference
        else:  # If it's a PracticeSlot
            for practices in slot.practices:
                for pref in preferences[practices]:  # Check preferences for each practice
                    if time_slot != pref[0]:  # If the scheduled time doesn't match the preferred time
                        pref_val += pref[1]  # Add the penalty value from the preference
    return pref_val  # Return the total preference penalty

def eval_pair(fact, pair, pennotpaired):
    # Evaluate the penalty for pairs that are scheduled in different time slots
    slot_pair = pair
    val = 0
    team_dict = {}

    # Loop through all game and practice slots to organize teams by time slot
    for slot in fact.gameslots + fact.practiceslots:
        time_slot = f"{slot.day} {slot.startTime}"  # Format time as day and start time
        if isinstance(slot, GameSlot):  # If it's a GameSlot
            if time_slot not in team_dict:  # If time slot not already in the dictionary
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["games"].update(slot.games)  # Add games to the time slot
        elif isinstance(slot, PracticeSlot):  # If it's a PracticeSlot
            if time_slot not in team_dict:  # If time slot not already in the dictionary
                team_dict[time_slot] = {"games": set(), "practices": set()}
            team_dict[time_slot]["practices"].update(slot.practices)  # Add practices to the time slot

    # Evaluate the penalty for each time slot
    for time_slot, teams in team_dict.items():
        combined_teams = teams["games"].union(teams["practices"])  # Combine games and practices for the time slot
        for pair in slot_pair:  # Loop through the pairs
            if (pair[0] in combined_teams) ^ (pair[1] in combined_teams):  # If only one team from the pair is scheduled
                val += pennotpaired  # Add penalty for non-paired teams
    return val / 2  # Return the penalty value, divided by 2 to account for double counting

def eval_secdiff(fact, pensection):
    # Evaluate the penalty for teams in the same section scheduled too closely together
    team_dict = {}
    val = 0

    # Loop through all game slots to organize teams by time slot
    for slot in fact.gameslots:
        time_slot = f"{slot.day} {slot.startTime}"  # Format time as day and start time
        if isinstance(slot, GameSlot):  # If it's a GameSlot
            if time_slot not in team_dict:  # If time slot not already in the dictionary
                team_dict[time_slot] = {"games": set()}
            team_dict[time_slot]["games"].update(slot.games)  # Add games to the time slot

    # Evaluate the penalty for teams in the same section
    for time_slot, teams in team_dict.items():
        overlap_teams = [team.split(" ") for team in teams["games"]]  # Split teams by their section
        
        # Compare each pair of teams to check if they're in the same section
        for i in range(len(overlap_teams)):
            for j in range(i + 1, len(overlap_teams)):
                if overlap_teams[i][1] == overlap_teams[j][1]:  # If the teams are in the same section
                    if (int(overlap_teams[j][-1]) - int(overlap_teams[i][-1])) == 1:  # If the teams are in consecutive slots
                        val += pensection  # Add penalty for consecutive scheduling of teams in the same section
    return val  # Return the total penalty for section differences

def Eval(fact, wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin, preferences, pair, pennotpaired, pensection):
    # Calculate the total evaluation score based on all the factors
    val = ((eval_minfilled(fact, pengamemin, penpracticemin) * wminfilled) + 
           (eval_pref(fact, preferences) * wpref) + 
           (eval_pair(fact, pair, pennotpaired) * wpair) + 
           (eval_secdiff(fact, pensection) * wsecdiff))
    
    return val  # Return the final evaluation score