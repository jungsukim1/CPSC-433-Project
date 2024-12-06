from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random

def Delete(fact):
    # amount_to_delete = random.randint(1,schedule.totalGames + schedule.totalPractices - 1)
    
    # for i in range(amount_to_delete):
    #     choice = random.randint(0,1)
        
    #     if choice == 0:
    #         rand_index = random.randint(0,schedule.totalGames)
    #         schedule.gameslots[rand_index].removeGame()
            
    #     else:
    #         rand_index = random.randint(0,schedule.totalPractices)
    #         schedule.practiceslots[rand_index].removePractice()
    
    del fact[0]
    return fact
    