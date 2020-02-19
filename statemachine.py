class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []
        self.handler=None

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def runOneStep(self, cargo):
        if(self.handler is None):
            try:
                self.handler = self.handlers[self.startState]
            except:
                raise InitializationError("must call .set_start() before .run()")
            #if not self.endStates:
            #    raise  InitializationError("at least one state must be an end_state")

        newState= self.handler(cargo)
        if newState.upper() in self.endStates:
            print("reached end state", newState)
            #break
        else:
            print("State: ", newState)
            self.handler = self.handlers[newState.upper()]
