from statemachine import StateMachine

#Maybe add somec checks on the data, like not empty check
class StateMachineSM:
    memory=[]
    m={}

    def __init__(self):
        self.m = StateMachine()
        self.m.add_state("Still_state", self.still_state_transitions)
        self.m.add_state("Moving_state", self.moving_state_transitions)
        self.m.add_state("Bumping_state", self.bumping_state_transitions)
        self.m.add_state("Holding_state", self.holding_state_transitions)
        self.m.add_state("Crash_state", self.crash_state_transitions)
        #m.add_state("Crash", None, end_state=1) #If we want to add a end state
        self.m.set_start("Still_state")

    @staticmethod
    def conditionOr(op,data, names, values):
        result=False
        for i,key in enumerate(names):
            if(op==">"):
                result=result or abs(data[key])>values[i]
            else:
                result=result or abs(data[key])<values[i]
        return result

    @staticmethod
    def conditionAnd(op,data, names, values):
        result=True
        for i,key in enumerate(names):
            if(op==">"):
                result=result and abs(data[key])>values[i]
            else:
                result=result and abs(data[key])<values[i]
        return result

    def still_state_transitions(self, data):
        #if data["Std_norm"] >0.01 or abs(data["Der_norm"])>0.04 or data["Std_current"] >1 or abs(data["Der_current"])>10:
        #if self.conditionAnd(">",data, ["Std_norm","Der_norm","Std_current","Der_current"], [0.01,0.04,1,10]):
        if self.conditionAnd(">",data, ["norm", "current", "Std_norm","Std_current"], [0.9, 5, 0.005, 0.8]):
            newState = "Moving_state"
        else:
            newState = "Still_state"
        return newState

    def moving_state_transitions(self, data):
        if (data["normOut"] * data["currentOut"]) < 40:
            newState = "Crash_state"
        elif self.conditionAnd(">",data, ["Std_current","Der_current"], [15,70]):
            newState = "Holding_state"
        #elif self.conditionAnd(">",data, ["Std_norm","Der_norm","Std_current","Der_current"], [0.1,0.5,4,20]):
        #    newState = "Bumping_state"
        elif self.conditionAnd("<",data, ["norm", "current", "Std_norm","Std_current"], [0.9, 5, 0.005, 0.8]):
            newState = "Still_state"
        else:
            newState = "Moving_state"
        return newState
    
    def bumping_state_transitions(self, data):
        if self.conditionOr("<",data, ["Std_norm","Der_norm","Std_current","Der_current"], [0.1,0.5,4,20]):
            newState = "Moving_state"
        elif self.conditionOr("<",data, ["Std_norm","Der_norm","Std_current","Der_current"], [0.01,0.04,1,10]):
            newState = "Still_state"
        else:
            newState = "Bumping_state"
        return newState

    def holding_state_transitions(self, data):
        if self.conditionAnd("<",data, ["Std_current","Der_current"], [15,70]):
            newState = "Moving_state"
        elif self.conditionAnd("<",data, ["norm", "current", "Std_norm","Std_current"], [0.9, 5, 0.005, 0.8]):
            newState = "Still_state"
        else:
            newState = "Holding_state"
        return newState
    
    def crash_state_transitions(self, data):
        if self.conditionAnd("<",data, ["norm", "current", "Std_norm","Std_current"], [0.9, 5, 0.005, 0.8]):
            newState = "Still_state"
        else:
            newState = "Crash_state"
        return newState

    def runOneStep(self,data):
        return self.m.runOneStep(data)


if __name__== "__main__":
    m = StateMachineSM()

    m.runOneStep({"Std_norm" :0,"Der_norm" :0,"Std_current":0, "Der_current":0 })
    m.runOneStep({"Std_norm" :1,"Der_norm" :1,"Std_current":1, "Der_current":1 })
