from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random

def Cross(scheduleA,scheduleB):
    
    temp_games_list = [] 
    temp_practices_list = [] 
    
    totalobjectsA = scheduleA.totalGames + scheduleA.totalPractices
    totalobjectsB = scheduleB.totalGames + scheduleB.totalPractices
    
    #the max loop amount is the totalnumber of games+practice of the smaller sched incase they arent the same size
    loop_max = totalobjectsA if totalobjectsA < totalobjectsB else totalobjectsB 
    
    #random num of game/prac to cross
    for i in range (random.randint(1,loop_max - 1)):
        
        if (scheduleA.totalGames == len(temp_games_list)):
            what_to_change = 1
        elif (scheduleA.totalPractices == len(temp_practices_list)):
            what_to_change = 0
        else:
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
    index = random.randint(0,len(schedule.gameslots) - 1)
    chosen_gameSlot = schedule.gameslots[index]
    
    while chosen_gameSlot.size == 0:
        index = random.randint(0,len(schedule.gameslots) - 1)
        chosen_gameSlot = schedule.gameslots[index]
    
    print(chosen_gameSlot.size)
    taken_game = chosen_gameSlot.removeGame()
    
    #store the game in a temp gameslot object
    #purpose was to store the gameitself and day/time, you could technically use a dict instead but nah
    resultSlot = GameSlot(-1,-1,chosen_gameSlot.day,chosen_gameSlot.startTime)
    resultSlot.addGame(taken_game)
    
    return {"resultSlot" : resultSlot, "indexA" : index} #returns a dict of the slot obj and the index where it was taken from
    

def Get_rand_practice(schedule):
    index = random.randint(0,len(schedule.practiceslots)- 1)
    chosen_practiceSlot = schedule.practiceslots[index]
    
    while chosen_practiceSlot.size == 0:
        index = random.randint(0,len(schedule.practiceslots) - 1)
        chosen_practiceSlot = schedule.practiceslots[index]
        
    print(chosen_practiceSlot.size)
    taken_practice = chosen_practiceSlot.removePractice()
    
    #store the game in a temp gameslot object
    #purpose was to store the gameitself and day/time, you could technically use a dict instead but nah
    resultSlot = PracticeSlot(-1,-1,chosen_practiceSlot.day,chosen_practiceSlot.startTime)
    resultSlot.addPractice(taken_practice)
    
    return {"resultSlot" : resultSlot, "indexA" : index} #returns a dict of the slot obj and the index where it was taken from
        

games = ["CMSA U13T3 DIV 01",
"CMSA U13T3 DIV 02",
"CUSA O18 DIV 01",
"CMSA U17T1 DIV 01"]

practices = ["CMSA U13T3 DIV 01 PRC 01",
"CMSA U13T3 DIV 02 OPN 02",
"CUSA O18 DIV 01 PRC 01"
,"CMSA U17T1 PRC 01"]
        
game1 = GameSlot(1,0,"MO","7:00")
game1.addGame("CMSA U13T3 DIV 01")
game2 = GameSlot(1,0,"TU","9:00")
game2.addGame("CMSA U13T3 DIV 02")
game3 = GameSlot(1,0,"FR","11:00")
game3.addGame("CUSA O18 DIV 01")

prac1 = PracticeSlot(1,0,"MO","7:00")
prac1.addPractice("CMSA U13T3 DIV 01 PRC 01")
prac2 = PracticeSlot(1,0,"TU","9:00")
prac2.addPractice("CMSA U13T3 DIV 02 OPN 02")

sched = Schedule()
sched.gameslots = [game1,game2,game3]
sched.totalGames = 3
sched.totalPractices = 2
sched.practiceslots = [prac1,prac2]
print("schedule A")
sched.printSchedule()
print("next\n")

games_2 = ["CMSA U19T1 DIV 01",
"CSSA U19T2 DIV 01",
"CUSA O19T1 DIV 01",
"CUSA O35T1 DIV 01"]

practices_2 = ["CUSA U14T2 DIV 02 PRC 03",
"CMSA U14T2 DIV 02 PRC 04",
"CMSA U14T3 PRC 01",
"CSSA U14T3 PRC 02"]

game11 = GameSlot(1,0,"MO","7:00")
game11.addGame("CMSA U19T1 DIV 01")
game22 = GameSlot(1,0,"TU","9:00")
game22.addGame("CSSA U19T2 DIV 01")
game33 = GameSlot(1,0,"FR","11:00")
game33.addGame("CUSA O35T1 DIV 01")

prac11 = PracticeSlot(1,0,"MO","7:00")
prac11.addPractice("CUSA U14T2 DIV 02 PRC 03")
prac22 = PracticeSlot(1,0,"TU","9:00")
prac22.addPractice("CMSA U14T3 PRC 01")

sched2 = Schedule()
sched2.gameslots = [game11,game22,game33]
sched2.totalGames = 3
sched2.totalPractices = 2
sched2.practiceslots = [prac11,prac22]
print("schedule B")
sched2.printSchedule()
print("crossing....\n")

a,b = Cross(sched,sched2)
print("new A")
a.printSchedule()
print("\nnew B")
b.printSchedule()