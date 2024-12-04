from Slots import GameSlot, PracticeSlot
import random

def Cross(factA,factB):
    index = random.randint(0,len(factA))
    
    factB_index = 0
    if factA[index] is GameSlot:
        amount_to_cross = random.randint(1,factA.totalGames) #if total games cant be a thing then just make an iterator
        Get_rand_game(factA[index],amount_to_cross)
        if factB[factB_index] is not GameSlot:
            factB_index = 1
        
def Get_rand_game(gameslot,amount):
    games_to_swap = []
    while len(games_to_swap) < amount:
        index = random.randint(0,fact.totalGames) #total games again
        fact[]
        
#ask about fact, whether it has mutple game slots or just one array of array of game slots
        
    