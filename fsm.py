"""
         // <------ dormir
         ||           /\
         \/           ||
      acordar ----> comer ----> estudar
                      /\          ||
                      ||          ||
                      || <------- ||             
fsm = FiniteStateMachine()
fsm.createState("acordar", ["comer"])
fsm.createState("estudar", ["comer"])
fsm.createState("comer", ["estudar", "dormir"])
fsm.createState("dormir", ["acordar"])
fsm.changeState("acordar") # OK
fsm.changeState("dormir")  # Erro
print(fsm.getState()) 
"""

class FiniteStateMachine:
    def __init__(self):
        self.__states = {}
        self.__currentState = None
        self.__count = 0
        
    def createState(self, STATENAME, NEXTSTATELIST ):
        self.__states[STATENAME] = NEXTSTATELIST
        self.__count += 1
        
    def getState(self):
        return self.__currentState
    
    def changeState(self, STATE):
        if STATE in self.__states:
            if self.__currentState == None or (STATE in self.__states[self.__currentState]):
                self.__currentState = STATE
            else:
                raise Exception("Erro em FiniteStateMachine::changeState: _{}_ não pertence ao próximo estado de _{}_.".format(STATE, self.__currentState))
        else:
            raise Exception("Erro em FiniteStateMachine::changeState: {} não existe.".format(STATE))
