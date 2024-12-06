from Slots import GameSlot, PracticeSlot

class HardConstr:
    
    
    ## gamemax funcion returns false when total games more than set max
    def gamemax(slot):
        return (length(GameSlot.games()) > GameSlot.max)
    
    ## practicemax funcion returns false when total practices more than set max
    def practicemax(slot):
        return (length(PracticeSlot.practices()) > PracticeSlot.max)


class SoftConstr:

    ## day specific functions
    def something():
        return