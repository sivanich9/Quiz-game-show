HOW TO RUN:

open 4 terminals
In one terminal run the command =>Python Server.Py <Port Number>.
In remaining three terminals run the command => python client.py <port number>.

PROJECT OVERVIEW:

There is a host who conducts the show and participants/players who provide answers. Let us say there are three participants. The host has a long list of questions and correct answers with him. He randomly chooses one of the questions (making sure it is not a repeat of previous questions) and sends to all three players. The players receive the question, think about the answer for a while and press the buzzer. There is a timer for 10 seconds for buzzer to be presssed. Otherwise, the host moves on to the next question. The first one to press the buzzer is given a chance to provide the answer within 10 seconds. If the answer is correct, he is given 1 point, otherwise -0.5. Nobody gets chance to answer this question again. The host then proceeds with the next question. The game stops when any player gets 5 points and that player is declared the winner.

PROJECT DESCRIPTION:

I used python language.
server waits for a connection from the three clients.once three clients are connected question will appear on your terminals
it will wait for 10 seconds. if you press buzzer after 10 seconds then you will not get marks for that question and it automatically displays the next question.
if you press buzzzer within 10 sec and again if you answer question after 10 sec then you will get negative marks for pressing buzzer and not answering in 10 sec. Then it automatically display next question. Once the question is displayed, it doesn't display next time.
The quiz is for 5 marks. If the client score 5 marks the quiz will end. the client is declared as winner.

