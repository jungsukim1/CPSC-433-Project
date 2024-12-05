from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random

def Cross(scheduleA,scheduleB):
    index = random.randint(0,1)
    
    temp_games_list = [] 
    temp_practices_list = [] 
    
    totalobjectsA = scheduleA.totalGames + scheduleA.totalPractices
    totalobjectsB = scheduleB.totalGames + scheduleB.totalPractices
    
    #the max loop amount is the totalnumber of games+practice of the smaller sched incase they arent the same size
    loop_max = totalobjectsA if totalobjectsA < totalobjectsB else totalobjectsB 
    
    #random num of game/prac to cross
    for i in range (random.randint(1,loop_max - 1)):
        what_to_change = random.randint(0,1) #choose prac or game
        
        if what_to_change == 1: 
            taken_gameSlot = Get_rand_game(scheduleA)
            temp_games_list.append(taken_gameSlot)
        
        else:
            taken_practiceSlot = Get_rand_practice(scheduleA)
            temp_practices_list.append(taken_practiceSlot)
    
    for gameSlotADict in temp_games_list:
        replacement_slotA = scheduleA.gameslots[gameSlotADict["indexA"]]
        gameSlotA = gameSlotADict["resultSlot"]
        
        #loop through all slots of sched B
        for gameSlotB in scheduleB.gameslots: 
            #if this slot day/time matches the one we are replacing 
            if gameSlotB.day == gameSlotA.day and gameSlotB.startTime == gameSlotA.startTime:
                replacement_slotA.addGame(gameSlotB.removeGame())
                gameSlotB.addGame(gameSlotA.removeGame())
                break
                    
    for practiceSlotADict in temp_practices_list:
        replacement_slotA = scheduleA.practiceslots[practiceSlotADict["indexA"]]
        practiceSlotA = practiceSlotADict["resultSlot"]
        
        for practiceSlotB in scheduleB.practiceslots:
            if practiceSlotB.day == practiceSlotA.day and practiceSlotB.startTime == practiceSlotA.startTime:
                replacement_slotA.addPractice(practiceSlotB.removePractice())
                practiceSlotB.addPractice(practiceSlotA.removePractice())
                break
    
    return (scheduleA,scheduleB) #return tuple of sched A and B
        
#finds a random game
def Get_rand_game(schedule):
    index = random.randint(0,schedule.totalGames - 1)
    chosen_gameSlot = schedule.gameslots[index]
    taken_game = chosen_gameSlot.games.removeGame()
    
    #store the game in a temp gameslot object
    #purpose was to store the gameitself and day/time, you could technically use a dict instead but nah
    resultSlot = GameSlot(-1,-1,chosen_gameSlot.day,chosen_gameSlot.startTime)
    resultSlot.addGame(taken_game)
    
    return {"resultSlot" : resultSlot, "indexA" : index} #returns a dict of the slot obj and the index where it was taken from
    

def Get_rand_practice(schedule):
    index = random.randint(0,schedule.totalPractices - 1)
    chosen_practiceSlot = schedule.practiceslots[index]
    taken_practice = chosen_practiceSlot.practices.removeGame()
    
    #store the game in a temp gameslot object
    #purpose was to store the gameitself and day/time, you could technically use a dict instead but nah
    resultSlot = PracticeSlot(-1,-1,chosen_practiceSlot.day,chosen_practiceSlot.startTime)
    resultSlot.addGame(taken_practice)
    
    return {"resultSlot" : resultSlot, "indexA" : index} #returns a dict of the slot obj and the index where it was taken from
        
    