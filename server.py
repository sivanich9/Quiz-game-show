import socket
import sys
from thread import *
import time
from random import *
import select

# AF_NET is the address of the socket
# SOL_SOCKET means the type of the socket
#SOCK_STREAM means that the data or characters are read in a flow
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

TIMEOUT = 10
timeout = 10

all_connections = []
all_address = []

#Setting up the server details and checks whether proper size of arguments are given
if len(sys.argv) != 2:
    print ("Type in the following order : script,  port number")
    exit()



#These are the values that the client must be aware about
s.bind(('127.0.0.1', int(sys.argv[1])))
s.listen(100)

questions = [" Grand Central Terminal, Park Avenue, New York is the world's? \n a.largest railway station b.highest railway station c.longest railway station d.None of the above",
     " Entomology is the science that studies? \n a.Behavior of human beings b.Insects c.The origin and history of technical and scientific terms d.The formation of rocks",
     " Which sea creature has three hearts? \n a.Dolphin b.Octopus c.Walrus d.Seal",
     " Eritrea, which became the 182nd member of the UN in 1993, is in the continent of \n a.Asia b.Africa c.Europe d.Australia",
     " How many bones does an adult human have? \n a.206 b.208 c.201 d.196",
     " Garampani sanctuary is located at \n a.Junagarh, Gujarat b.Diphu, Assam c.Kohima, Nagaland d.Gangtok, Sikkim ",
     " For which of the following disciplines is Nobel Prize awarded? \n a.Physics and Chemistry b.Physiology or Medicine c.Literature, Peace and Economics d.All of the above",
     " Hitler party which came into power in 1933 is known as \n a.Labour Party b.Nazi Party c.Ku-Klux-Klan d.Democratic Party",
     " FFC stands for \n a.Foreign Finance Corporation b.Film Finance Corporation c.Federation of Football Council d.None of the above ",
     " Fastest shorthand writer was \n a.Dr. G. D. Bist b.J.R.D. Tata c.J.M. Tagore d.Khudada Khan",
     " First human heart transplant operation conducted by Dr. Christiaan Barnard on Louis Washkansky, was conducted in \n a.1967 b.1968 c.1958 d.1922"
     " Galileo was an Italian astronomer who \n a.developed the telescope b.discovered four satellites of Jupiter c.discovered that the movement of pendulum produces a regular time measurement d.All of the above",
     " Exposure to sunlight helps a person improve his health because \n a.the infrared light kills bacteria in the body b.resistance power increases c.the pigment cells in the skin get stimulated and produce a healthy tan d.the ultraviolet rays convert skin oil into Vitamin D",
     " First China War was fought between \n a.China and Britain b.China and France c.China and Egypt d.China and Greek",
     " For the Olympics and World Tournaments, the dimensions of basketball court are \n a.26 m x 14 m b.28 m x 15 m c.27 m x 16 m d.28 m x 16 m ",
     " Who gifted the Statue of Libery to the US? \n a.Brazil b.France c.Wales d.Germany"]

answers = ['a', 'b', 'b', 'b', 'a', 'b', 'd', 'b', 'b', 'a', 'a', 'd', 'd', 'a', 'b', 'b']

scores = []
Buzz = [0, 0, 0]
client = ["", -1]
msg = ""

def AcceptConns():
    while True:
        conn, address = s.accept()
        s.setblocking(1)
        all_connections.append(conn)
        all_address.append(address)
        scores.append(0)
        print("Connection has been established ")
        if(len(all_connections) == 3):
            time.sleep(1)
            Instructions()
            time.sleep(10)
            startquiz()
    
    
    
def Instructions():
    BroadCast("Hello!!! Welcome to the quiz.\nYour quiz will start in 10 seconds\nAnswer before your opponent answers\n\n\n")
   

def startquiz():
    if len(questions) != 0:
        Buzz[2] = randint(0, 10000)%len(questions)
        for conn in all_connections:
            conn.send(questions[Buzz[2]])
        i, o, e = select.select(all_connections, [], [], TIMEOUT)
        if i:
            temp = i[0].recv(1024)
            Buzz[0] = 1
            client[0] = i[0]
            for p in range(len(all_connections)):
                if i[0] == all_connections[p]:
                    break
            client[1] = p
            client[0].send("You pressed the buzzer first. So please answer you have only 10 seconds.\n")
            for conn in all_connections:
                if conn == client[0]:
                    continue
                conn.send("Player" + str(client[1]+1) + " pressed the buzzer first. You have no chance to answer\n")
               
            i1, o1, e1 = select.select(i, [], [], timeout)
            if i1:
                msg = i1[0].recv(1024)
                if msg[0] == answers[Buzz[2]][0]:
                    client[0].send("Right answer!!!.\n")
                    BroadCast("Player" + str(client[1]+1) + "'s score + 1\n")
                    scores[client[1]] += 1
                else:
                    client[0].send("SORRY!!!Wrong answer!!!.\n")
                    BroadCast("Player" + str(client[1]+1) + "'s score - 0.5\n")
                    scores[client[1]] -= 0.5
            else:
                client[0].send("TimeOut!!! You can't answer this question again.\n")
                BroadCast("Player" + str(client[1]+1) + "'s score - 0.5\n")
                scores[client[1]] -= 0.5
            if len(questions) != 0:
                questions.pop(Buzz[2])
                answers.pop(Buzz[2])
            if len(questions) == 0:
                endquiz(0)
        else:
            BroadCast("Sorry!!! TimeOut. No one pressed the buzzer.\n")
            if len(questions) != 0:
                questions.pop(Buzz[2])
                answers.pop(Buzz[2])
            if len(questions) == 0:
                endquiz(0)
        maxm = max(scores)
        if maxm >= 5:
            _index = scores.index(maxm)
            all_connections[_index].send("\nCongratulations!!!You Won.\n")
            endquiz(1)
        else:
            startquiz()
    else:
        endquiz(0)

def endquiz(temp):
    if temp:
        for t in range(len(all_connections)):
            all_connections[t].send("\nYou scored " + str(scores[t]) + " points.\n")
        maxm = max(scores)
        _index = scores.index(maxm)
        for conn in all_connections:
            if conn == all_connections[_index]:
                continue
            conn.send("Player" + str(_index+1) + " Won.\n")
        BroadCast("\nGame Over\n")
        BroadCast("----")
    else:
        BroadCast("None of you won the quiz\nIt's a draw\n")
        for t in range(len(all_connections)):
            all_connections[t].send("You scored " + str(scores[t]) + " points.\n")


def BroadCast(msg):
    for conn in all_connections:
        try:
            conn.send(msg)
        except:
            conn.close()
            remove(conn) 

def remove(conn):
    if conn in all_connections:
        i = all_connections.index(conn)
        all_connections.pop(i)
        all_address.pop(i)

AcceptConns()





