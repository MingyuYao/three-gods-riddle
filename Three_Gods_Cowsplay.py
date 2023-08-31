import random
from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    def cowsplay(self, arr, map_func):
        """
        The Agent will use a relic to tell the count of truth in an given array:
        The relic will say "shh" for 0 truth and "moo" up to three times depends
        on the number of truth mod 3:
        [T] will count only the truth as the input of the relic.
        [F] will count only the falsehood as the input of the relic
        [R] will always give a random number in range(4) as the input of the relic.
        The default set of cowsplays are: ["shh", "moo"]
        """
        pass

class T(Agent):
    def __init__(self, b=None):
        if type(b)==list and len(b)==2 and type(b[0]) is type(b[1]) is str:
            self.__b = b
        else:
            self.__b = ["shh", "moo"]
    def cowsplay(self, arr, map_func):
        map_arr = list(map(lambda x: bool(map_func(x)), arr))
        cow_say = lambda x : 0 if x<=0 else x%3 or 3
        cow_ans = cow_say(sum(map_arr))
        return self.__b[0] if cow_ans == 0 else " ".join([self.__b[1]]*cow_ans)
    
class F(Agent):
    def __init__(self, b=None):
        if type(b)==list and len(b)==2 and type(b[0]) is type(b[1]) is str:
            self.__b = b
        else:
            self.__b = ["shh", "moo"]
    def cowsplay(self, arr, map_func):
        map_arr = list(map(lambda x: not bool(map_func(x)), arr))
        cow_say = lambda x : 0 if x<=0 else x%3 or 3
        cow_ans = cow_say(sum(map_arr))
        return self.__b[0] if cow_ans == 0 else " ".join([self.__b[1]]*cow_ans)

class R(Agent):
    def __init__(self, b=None):
        if type(b)==list and len(b)==2 and type(b[0]) is type(b[1]) is str:
            self.__b = b
        else:
            self.__b = ["shh", "moo"]
    def cowsplay(self, arr, map_func):
        cow_ans = random.randint(0,min(len(arr),3))
        return self.__b[0] if cow_ans == 0 else " ".join([self.__b[1]]*cow_ans)

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
This time, the Agent will use a relic to tell the count of truth in the
given array instead of answer your questions directly.The relic will say
"shh" for 0 truth and "moo" up to three times as the number of truth mod 3.
"T" will give only the number of truth in the array to the relic.
"F" will give only the number of falsehood in the array to the relic.
"R" will give a random integer between 0 and min(3, len(array)) to the relic.
In the game prompt, you'll need to format your question as the arr and a
map function seperated by ';', and for the map function it will be wrapped in
a <lambda it> function so can write the predicate only with 'it' as param.
e.g. >>>> ag[:-1]; isinstance(it, R)
p.s. You found that the relic was acturally an Acient Prediction Teller (APT).
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
    print("""*** Some question you can given to the relic are as follows:
--> ag[:-1]; isinstance(it, R)
--> [ag[0]]; it.cowsplay([it],lambda x:isinstance(x,F)) == 'moo'""")
    for x in range(len(ag)):
        ai = int(input("({}/{})Enter the index of agent you want to ask: [0-{}]".format(x+1,len(ag),len(ag)-1)))
        aq = input(">==>  What question you want to use ag[{}]'s relic for?\n>>>>".format(ai))
        ar = eval(aq.split(';')[0])
        aq = "lambda it:" + aq.split(';')[1]
        aw = ag[ai].cowsplay(ar, eval(aq))
        print("<==< The sound you get from the agent's relic is: " + aw)
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
        b = input("*** please suggest alternative [\"shh\",\"moo\"] you want the agent's relic to sound, or press Enter to skip:\n")
        if b and type(eval(b)) == list and len(eval(b))==2:
            b = eval(b)
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

    
        
