from Slots import GameSlot, PracticeSlot
from Schedule import Schedule

def Delete(fact, keeps):
    # Check if the fact list is empty, and print an error message if it is
    if not fact:
        print("**Error** Fact is empty")
        return fact

    # Remove elements from the end of the list until the length is less than or equal to 'keeps'
    while len(fact) > keeps:
        del fact[-1]

    return fact  # Return the modified fact list with the required number of elements