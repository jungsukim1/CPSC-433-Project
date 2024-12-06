from InputParser import parse_input_file
from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random


#fact - list of all selected games and practices in their slots
#games - all possible games
#practices - all possible practices
#TODO connect with ORTree and test that it works
def Mutation(schedule,games,practices,partial_assign):
       
    availableGames = games
    availablePractices = practices
    
    changed_games = [] #keeps track of all the changed indexs in the new fact A
    changed_practices = []
    
    #loop for how many games we will change
    for i in range(random.randint(1,(schedule.getTotalGames() + schedule.getTotalPractices() - 1))):
        
        if (len(changed_games) + schedule.getTotalGames() == len(games)):
            loop_range = 0
        elif (len(changed_practices) + schedule.getTotalPractices() == len(games)):
            loop_range = 1
        elif (len(changed_games) + schedule.getTotalGames() == len(games) and len(changed_practices) + schedule.getTotalPractices() == len(games)):
            break
        else:
            loop_range = random.randint(0,1) 
            
        if loop_range == 1:
            random_gameslot_index = random.randint(0, len(schedule.gameslots) - 1)
            selected_gameslot = schedule.gameslots[random_gameslot_index]
            #print(selected_gameslot.games)
            newGame = Generate_Game(schedule,selected_gameslot,availableGames,changed_games,partial_assign)
            if newGame == None:
                return None
            changed_games.append(selected_gameslot.removeGame())
            selected_gameslot.addGame(newGame)
            
        elif loop_range == 0:
            random_practiceslot_index = random.randint(0, len(schedule.practiceslots) - 1)
            selected_practiceslot = schedule.practiceslots[random_practiceslot_index]
            newPractice = Generate_Practice(schedule,selected_practiceslot,availablePractices,changed_games,partial_assign)
            if newPractice == None:
                return None
            changed_practices.append(selected_practiceslot.removePractice())
            selected_practiceslot.addPractice(newPractice)
    
            #ORTREE to check the new fact
    print("changed games:" , changed_games, "changed practices:", changed_practices)
    return schedule #return modified gameslots and practice slots 

def Generate_Game(schedule,gameSlot,games,changed_games,partial_as): 
    temp_arr = games.copy()
    
    if len(temp_arr) == 0:
        return None
    
    if len(temp_arr) != 1:
        rand_game_index = random.randint(0, len(temp_arr)-1)
    else:
        rand_game_index = 0
    
    result = temp_arr[rand_game_index]
    if result in gameSlot.games or result in changed_games or Schedule_check(schedule,result,"") == False or result in partial_as:
        temp_arr.remove(result)
        result = Generate_Game(schedule,gameSlot,temp_arr,changed_games)
        
    
    return result

#finds a game that isnt in the slot already
def Generate_Practice(schedule,practiceSlot,practices,changed_games,partial_as): 
    temp_arr = practices.copy()
    
    if len(temp_arr) == 0:
        return None
    
    if len(temp_arr) != 1:
        rand_game_index = random.randint(0, len(temp_arr)-1)
    else:
        rand_game_index = 0
        
    result = practices[rand_game_index]
    if result in practiceSlot.practices or result in changed_games or Schedule_check(schedule,"",result) == False or result in partial_as:
        temp_arr.remove(result)
        result = Generate_Practice(schedule,practiceSlot,temp_arr,changed_games)
    
    return result

def Schedule_check(schedule,game,practice):
    if practice == "":
        for gameslots in schedule.gameslots:
            if game in gameslots.games:
                return False
    else:
        for practiceslots in schedule.practiceslots:
            if practice in practiceslots.practices:
                return False
    
    return True


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
# sched.totalGames = 3
# sched.totalPractices = 2
# sched.practiceslots = [prac1,prac2]
# sched.printSchedule()
# print("next")



# a = Mutation(sched,games,practices)
# a.printSchedule()
