from InputParser import parse_input_file
from Slots import GameSlot, PracticeSlot
import random


#fact - list of all selected games and practices in their slots
#games - all possible games
#practices - all possible practices
#TODO connect with ORTree and test that it works
def Mutation(fact,games,practices):
    
    availableGames = games
    availablePractices = practices
    
    changed_indexs = [] #keeps track of all the changed indexs in the new fact A
    
    loop_range = random.randint(0, len(fact) - 1) #number of slots we will change
    for i in range(loop_range):
        rand_index = random.randint(0, len(fact) - 1) #random slot
        changed_indexs.append(rand_index)
        
        selected_slot = fact[rand_index]
        if selected_slot is GameSlot:
            newGame = Generate_Game(fact,games,rand_index)
            selected_slot.removeGame()
            selected_slot.addGame(newGame)
        
        elif selected_slot is PracticeSlot:
            newPractice = Generate_Practice(fact,practices)
            selected_slot.removePractice()
            selected_slot.addPractice(newPractice)
    
    #ORTREE to check the new fact
    
    return fact #return modified gameslots and practice slots 

#finds a game that isnt in the slot already
def Generate_Game(fact,games,index): 
    rand_game_index = random.randint(0, len(games) - 1)
    result = games[rand_game_index]
    if games[rand_game_index] in fact[index].games:
        result = Generate_Game(fact,games)
    
    return result

#finds a game that isnt in the slot already
def Generate_Practice(fact,practices,index): 
    rand_game_index = random.randint(0, len(practices) - 1)
    result = practices[rand_game_index]
    if practices[rand_game_index] in fact[index].practices:
        result = Generate_Game(fact,practices)
    
    return result