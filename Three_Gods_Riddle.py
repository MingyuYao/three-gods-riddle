import random
from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    def answer(self, question):
        """
        The Agent will answer yes/no to your question in its own language:
        [T] will always say "yes" if your question evaluate to True, else "no";
        [F] will always say "no" if your question evaluate to True, else "yes";
        [R] will always have 50% chance to say "yes" and 50% chance to say "no".
        The default set of answers are: ["ozo", "ulu"]
        """
        pass

class T(Agent):
    def __init__(self, b=None):
        if type(b)==list and len(b)==2 and type(b[0]) is type(b[1]) is str:
            self.__b = b
        else:
            self.__b = ["ozo", "ulu"]
    def answer(self, question):
        ans = bool(eval(question)) if type(question)==str else bool(question)
        return self.__b[int(ans)]
    
class F(Agent):
    def __init__(self, b=None):
        if type(b)==list and len(b)==2 and type(b[0]) is type(b[1]) is str:
            self.__b = b
        else:
            self.__b = ["ozo", "ulu"]
    def answer(self, question):
        ans = bool(eval(question)) if type(question)==str else bool(question)
        return self.__b[1-int(ans)]

class R(Agent):
    def __init__(self, b=None):
        if type(b)==list and len(b)==2 and type(b[0]) is type(b[1]) is str:
            self.__b = b
        else:
            self.__b = ["ozo", "ulu"]
    def answer(self, question):
        ans = random.random()<0.5
        return self.__b[int(ans)]

def score(ag, ap):
    if type(ap)!= list:
        print("Please provide a list of guesses for agents!")
        return False
    if len(ag) != len(ap):
        print("The Length of guesses does not match the number of agents!")
        return False
    sc = 0
    for i,v in enumerate(ap):
        if   v == 'T' and type(ag[i])==T:
            sc+=1
        elif v == 'F' and type(ag[i])==F:
            sc+=1
        elif v == 'R' and type(ag[i])==R:
            sc+=1
    print("You've correctly guessed {}/{} of our agents".format(sc,len(ag)))
    return True

def hint():
    print("""\
=-=-=-=-=-=-=-=-=-=-=-=-=-= HOW TO PLAY =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
You are tasked to ask N questions to one of N agents to figure out the
identity of each agent. There are three kind of Agents: ["T","F","R"].
"T" will always answer "yes" if the question is True, "no" otherwise.
"F" will always answer "yes" if the question is False, "no" otherwise.
"R" will always have 50% chance to answer either "yes" or "no".
The agents don't speak your language in default, instead they say "ozo"
or "ulu" but you don't know which one means "yes".(Default N=3)
=-=-=-=-=-=-=-=-=-=-=-=-=-=-= COMMAND =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
hint()        Print this help.
game()        Start a new game.
quit()        Exit this program.
""")

def game(custom_rules=False):
    if custom_rules:
        a, ag = gen_agents("prompt","prompt")
    else:
        a, ag = gen_agents()
    print("*** There are {} agents.".format(len(ag)))
    print("*** There is {} T,F,R agents respectively".format(a))
    print("""*** Some question you can ask as follows:
--> ag[1].answer("1+1==2") == "ozo"
--> isinstance(ag[1], T)""")
    for x in range(len(ag)):
        ai = int(input("({}/{})Enter the index of agent you want to ask: [0-{}]".format(x+1,len(ag),len(ag)-1)))
        aq = eval(input(">==>  What question you want to ask ag[{}]?\n>>>>".format(ai)))
        aw = ag[ai].answer(aq)
        print("<==< The answer you get from the agent is: " + aw)
    flag = False
    while not flag:
        print("*** You have asked all the questions, now it's your time to guess their identity: ")
        ap = eval(input(">==> Please provide your guesses as a list of letters, e.g. ['T', 'F', 'R']: \n"))
        flag = score(ag, ap)
    
def gen_agents(a=None,b=None):
    if a == None:
        a = [1, 1, 1]
    else:
        a = list(eval(input("*** please suggest how many [T,F,R] agents you want in the game:\n")))
    if b != None:
        b = input("*** please suggest alternative [\"yes\",\"no\"] you want the agent to use, or press Enter to skip:\n")
        if b and type(eval(b)) == list and len(eval(b))==2:
            b = eval(b)
            random.random()<0.5 and b.reverse()
        else:
            b = None
        
    ag = []
    for i in range(a[0]):
        ag.append(T(b))
    for i in range(a[1]):
        ag.append(F(b))
    for i in range(a[2]):
        ag.append(R(b))
    random.shuffle(ag)
    return (a, ag)
        

if __name__=="__main__":
    hint()
    while True:
        exec(input(">>> "))

    
        
