from Slots import GameSlot, PracticeSlot

def partConstr(assignment, fact, slot):
    from Main import not_compatible, unwanted

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
    from Main import not_compatible, unwanted, DEFAULTFACT
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