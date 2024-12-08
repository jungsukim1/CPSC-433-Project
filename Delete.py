from Slots import GameSlot, PracticeSlot
from Schedule import Schedule

def Delete(fact, keeps):
    if not fact:
        print("**Error** Fact is empty")
        return fact
    
    while len(fact) > keeps:
        del fact[-1]
    return fact
    