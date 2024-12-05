from InputParser import parse_input_file
from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random


#fact - list of all selected games and practices in their slots
#games - all possible games
#practices - all possible practices
#TODO connect with ORTree and test that it works
def Mutation(schedule,games,practices):
    
    availableGames = games
    availablePractices = practices
    
    changed_games = [] #keeps track of all the changed indexs in the new fact A
    
    #loop for how many games we will change
    for i in range(random.randint(1,(schedule.totalGames + schedule.totalPractices - 1))):
        loop_range = random.randint(0,1) 
        if loop_range == 1:
            selected_gameslot = schedule.gameslots
            random_gameslot_index = random.randint(0, len(selected_gameslot) - 1)
            newGame = Generate_Game(selected_gameslot,availableGames,random_gameslot_index,changed_games)
            changed_games.append(selected_gameslot.removeGame())
            selected_gameslot.addGame(newGame)
            
        elif loop_range == 0:
            selected_practiceslot = schedule.practiceslots
            random_practiceslot_index = random.randint(0, len(selected_practiceslot) - 1)
            newPractice = Generate_Practice(selected_practiceslot,availablePractices,random_practiceslot_index,changed_games)
            changed_games.append(selected_practiceslot.removePractice())
            selected_practiceslot.addPractice(newPractice)
    
            #ORTREE to check the new fact
    
    return schedule #return modified gameslots and practice slots 

#finds a game that isnt in the slot already
def Generate_Game(gameSlotsList,games,index,changed_games): 
    rand_game_index = random.randint(0, len(games) - 1)
    result = games[rand_game_index]
    if games[rand_game_index] in gameSlotsList[index].games or games[rand_game_index] in changed_games:
        result = Generate_Game(gameSlotsList,games,index)
    
    return result

#finds a game that isnt in the slot already
def Generate_Practice(practiceSlotsList,practices,index,changed_games): 
    rand_game_index = random.randint(0, len(practices) - 1)
    result = practices[rand_game_index]
    if practices[rand_game_index] in practiceSlotsList[index].practices or practices[rand_game_index] in changed_games:
        result = Generate_Game(practiceSlotsList,practices,index)
    
    return result