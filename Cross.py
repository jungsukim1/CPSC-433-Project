from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random
import math

def Cross(scheduleA,scheduleB,partial_assign):
    
    temp_games_list = [] 
    temp_practices_list = [] 
    temp_games_listB = []
    temp_practices_listB = []
    
    schedA_gameslots = scheduleA.getTotalGames()
    schedA_practiceslots = scheduleA.getTotalPractices()
    schedB_gameslots = scheduleA.getTotalGames()
    schedB_practiceslots = scheduleA.getTotalPractices()
    totalobjectsA = scheduleA.getTotalGames() + scheduleA.getTotalPractices()   
    totalobjectsB = scheduleB.getTotalGames() + scheduleB.getTotalPractices()
    
    #the max loop amount is the totalnumber of games+practice of the smaller sched incase they arent the same size
    loop_max = totalobjectsA if totalobjectsA < totalobjectsB else totalobjectsB 
    loop_max /= 4
    loop_max = round(loop_max)
    loop_amount = 0
    
    #print("aiofhhgrogirg" ,str(loop_max),str(totalobjectsA),str(totalobjectsB) )
    #random num of game/prac to cross
    for i in range (random.randint(1,loop_max)):
        
        if i > loop_amount:
            loop_amount = i
            
        if (schedA_gameslots == len(temp_games_list)):
            what_to_change = 0
        elif (schedA_practiceslots == len(temp_practices_list)):
            what_to_change = 1
        else:
            what_to_change = random.randint(0,1) #choose prac or game
        
        if what_to_change == 1: 
            taken_gameSlot = Get_rand_game(scheduleA,partial_assign)
            temp_games_list.append(taken_gameSlot)
        
        else:
            taken_practiceSlot = Get_rand_practice(scheduleA,partial_assign)
            temp_practices_list.append(taken_practiceSlot)
            
    for i in range (loop_amount):
        
        if (schedB_gameslots == len(temp_games_listB)):
            what_to_change = 0
        elif (schedB_practiceslots == len(temp_practices_listB)):
            what_to_change = 1
        else:
            what_to_change = random.randint(0,1) #choose prac or game
        
        if what_to_change == 1: 
            taken_gameSlot = Get_rand_game(scheduleB,partial_assign)
            temp_games_listB.append(taken_gameSlot)
        else:
            taken_practiceSlot = Get_rand_practice(scheduleB,partial_assign)
            temp_practices_listB.append(taken_practiceSlot)
    
    for gameSlotADict in temp_games_list:
        gameSlotA = gameSlotADict["resultSlot"]
        
        #loop through all slots of sched B
        for gameSlotB in scheduleB.gameslots: 
            #if this slot day/time matches the one we are replacing 
            if gameSlotB.day == gameSlotA.day and gameSlotB.startTime == gameSlotA.startTime:
                gameSlotB.addGame(gameSlotA.removeGame())
                break
                    
    for practiceSlotADict in temp_practices_list:
        practiceSlotA = practiceSlotADict["resultSlot"]
        
        for practiceSlotB in scheduleB.practiceslots:
            if practiceSlotB.day == practiceSlotA.day and practiceSlotB.startTime == practiceSlotA.startTime:
                practiceSlotB.addPractice(practiceSlotA.removePractice())
                break
    
#===================================================================================================================
    
    for gameSlotBDict in temp_games_listB:
        gameSlotB = gameSlotBDict["resultSlot"]
        
        #loop through all slots of sched B
        for gameSlotA in scheduleA.gameslots: 
            #if this slot day/time matches the one we are replacing 
            if gameSlotA.day == gameSlotB.day and gameSlotB.startTime == gameSlotA.startTime:
                gameSlotA.addGame(gameSlotB.removeGame())
                break
                    
    for practiceSlotBDict in temp_practices_listB:
        practiceSlotB = practiceSlotBDict["resultSlot"]
        
        for practiceSlotA in scheduleA.practiceslots:
            if practiceSlotA.day == practiceSlotB.day and practiceSlotB.startTime == practiceSlotA.startTime:
                practiceSlotA.addPractice(practiceSlotB.removePractice())
                break
    
    return (scheduleA,scheduleB) #return tuple of sched A and B
        
#finds a random game
def Get_rand_game(schedule,partial_as):

    available_indices = list(range(len(schedule.gameslots)))

    while available_indices:
        # Randomly pick an index from the available indices
        index = random.choice(available_indices)
        chosen_gameSlot = schedule.gameslots[index]

        print(chosen_gameSlot.games, chosen_gameSlot.getSize(), "index", index)

        # Check if the chosen slot is valid (not empty)
        if chosen_gameSlot.getSize() > 0 and chosen_gameSlot not in partial_as:
            break  # Found a non-empty slot, exit the loop

        # Remove the index from available indices because it's empty
        available_indices.remove(index)
        if not available_indices:
            print("All slots are empty")
            break
    
    print(chosen_gameSlot.games, chosen_gameSlot.getSize())
    taken_game = chosen_gameSlot.removeGame()
    
    #print("out (games)")
    #store the game in a temp gameslot object
    #purpose was to store the gameitself and day/time, you could technically use a dict instead but nah
    resultSlot = GameSlot(-1,-1,chosen_gameSlot.day,chosen_gameSlot.startTime)
    resultSlot.addGame(taken_game)
    
    return {"resultSlot" : resultSlot, "indexA" : index} #returns a dict of the slot obj and the index where it was taken from
    

def Get_rand_practice(schedule,partial_as):
    
    available_indices = list(range(len(schedule.practiceslots)))

    while available_indices:
        # Randomly pick an index from the available indices
        index = random.choice(available_indices)
        chosen_practiceSlot = schedule.practiceslots[index]

        #print(chosen_practiceSlot.practices, chosen_practiceSlot.getSize(), "index", index)

        # Check if the chosen slot is valid (not empty)
        if chosen_practiceSlot.getSize() > 0 and chosen_practiceSlot not in partial_as:
            break  # Found a non-empty slot, exit the loop

        # Remove the index from available indices because it's empty
        available_indices.remove(index)
        
        if not available_indices:
            print("All slots are empty")
            break
        
    # index = random.randint(0,len(schedule.practiceslots)- 1)
    # chosen_practiceSlot = schedule.practiceslots[index]
    
    # while chosen_practiceSlot.getSize() == 0:
    #     index = random.randint(0,len(schedule.practiceslots) - 1)
    #     chosen_practiceSlot = schedule.practiceslots[index]
    #print(chosen_practiceSlot.practices, chosen_practiceSlot.getSize())
    taken_practice = chosen_practiceSlot.removePractice()
    #print("out (practice)")
    
    #store the game in a temp gameslot object
    #purpose was to store the gameitself and day/time, you could technically use a dict instead but nah
    resultSlot = PracticeSlot(-1,-1,chosen_practiceSlot.day,chosen_practiceSlot.startTime)
    resultSlot.addPractice(taken_practice)
    
    return {"resultSlot" : resultSlot, "indexA" : index} #returns a dict of the slot obj and the index where it was taken from
        

# games = ["CMSA U13T3 DIV 01",
# "CMSA U13T3 DIV 02",
# "CUSA O18 DIV 01",
# "CMSA U17T1 DIV 01"]

# practices = ["CMSA U13T3 DIV 01 PRC 01",
# "CMSA U13T3 DIV 02 OPN 02",
# "CUSA O18 DIV 01 PRC 01"
# ,"CMSA U17T1 PRC 01"]
        
# game1 = GameSlot(1,0,"MO","7:00")
# game1.addGame("CMSA U13T3 DIV 01")
# game2 = GameSlot(1,0,"TU","9:00")
# game2.addGame("CMSA U13T3 DIV 02")
# game3 = GameSlot(1,0,"FR","11:00")
# game3.addGame("CUSA O18 DIV 01")

# prac1 = PracticeSlot(1,0,"MO","7:00")
# prac1.addPractice("CMSA U13T3 DIV 01 PRC 01")
# prac2 = PracticeSlot(1,0,"TU","9:00")
# prac2.addPractice("CMSA U13T3 DIV 02 OPN 02")

# sched = Schedule([],[])
# sched.gameslots = [game1,game2,game3]
# sched.practiceslots = [prac1,prac2]
# print("schedule A")
# sched.printSchedule()
# print("next\n")

# games_2 = ["CMSA U19T1 DIV 01",
# "CSSA U19T2 DIV 01",
# "CUSA O19T1 DIV 01",
# "CUSA O35T1 DIV 01"]

# practices_2 = ["CUSA U14T2 DIV 02 PRC 03",
# "CMSA U14T2 DIV 02 PRC 04",
# "CMSA U14T3 PRC 01",
# "CSSA U14T3 PRC 02"]

# game11 = GameSlot(1,0,"MO","7:00")
# game11.addGame("CMSA U19T1 DIV 01")
# game22 = GameSlot(1,0,"TU","9:00")
# game22.addGame("CSSA U19T2 DIV 01")
# game33 = GameSlot(1,0,"FR","11:00")
# game33.addGame("CUSA O35T1 DIV 01")

# prac11 = PracticeSlot(1,0,"MO","7:00")
# prac11.addPractice("CUSA U14T2 DIV 02 PRC 03")
# prac22 = PracticeSlot(1,0,"TU","9:00")
# prac22.addPractice("CMSA U14T3 PRC 01")

# sched2 = Schedule([],[])
# sched2.gameslots = [game11,game22,game33]
# sched2.practiceslots = [prac11,prac22]
# print("schedule B")
# sched2.printSchedule()
# print("crossing....\n")

# a,b = Cross(sched,sched2)
# print("new A")
# a.printSchedule()
# print("\nnew B")
# b.printSchedule()