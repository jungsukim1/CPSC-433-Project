from Slots import GameSlot, PracticeSlot
from Schedule import Schedule
import random

def Delete(fact):
    if not fact:
        print("**Error** Fact is empty")
        return fact
    
    del fact[-1]
    return fact
    
    del fact[0]
    return fact
    