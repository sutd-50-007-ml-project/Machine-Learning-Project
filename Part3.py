import math
import sys
from Part1 import get_train
from Part2 import get_sentence, transition_parameter

def modifiedViterbi(x, states, emission, transition, sentence):
    emii = emission
    transii = transition
    n = len(sentence)

    #the minimum value that float can represent
    #the values of transition/emission parameters will replace this
    takesmallest = math.log(sys.float_info.min)-1

    scores = {}

    #here instead of transition parameters x emission parameters,
    #we use log(transition parameters) + log(emission parameters)
    #to deal with underflow

    #for i = 0, i.e. from start state to the next state
    scores[0] = {}
    for j in states:
        if ("Start", j) in transii:
            transit = math.log(transii[("Start", j)])
        else:
            transit = takesmallest
        
        if (sentence[0], j) in emii:
            emit = math.log(emii[(sentence[0], j)])
        else:
            emit = takesmallest

        required = transit + emit
        scores[0][j] = (required, "Start")

    #for the rest of i states
    for i in range(1,n):
        scores[i] = {}

        #from state i to all other j states, calculate log of transition & emission parameters
        for j in states:
            maxprobe = []
            for l in states:
                if (l, j) in transii:
                    transit = math.log(transii[(l,j)])
                else:
                    transit = takesmallest

                if (sentence[i],j) in emii:
                    emit = math.log(emii[(sentence[i], j)])
                else:
                    emit = takesmallest
                
                if i > 1:
                    for m in range(x):
                        #calculate top m scores of current state using top 5 scores of previous state
                        score = scores[i-1][l][m][0] + transit + emit
                        maxprobe.append((score, l, m))
                else:
                    score = scores[i-1][l][0] + transit + emit
                    maxprobe.append((score, l, 0))
                
            #x = number of top scores/best sequences
            #find the top x scores and append to list
            bestX = []
            for m in range(x):
                max = (-sys.maxsize, 'nan', 'nan')
                for o in range(len(maxprobe)):
                    if maxprobe[o][0] > max[0]:
                        max = maxprobe[o]
                
                maxprobe.remove(max)
                bestX.append(max)
            
            scores[i][j] = bestX
    
    #from second last state to stop state
    scores[n] = {}
    maxprobe = []
    for j in states:
        if (j, "Stop") in transii:
            transit = math.log(transii[(j, "Stop")])
        else:
            transit = takesmallest
        
        for p in range(x):
            score = scores[n-1][j][m][0] + transit
            maxprobe.append((score, j, m))
    
    bestX = []
    for q in range(x):
        max = (-sys.maxsize, 'nan', 'nan')
        for r in range(len(maxprobe)):
            if maxprobe[r][0] > max[0]:
                max = maxprobe[r]
        maxprobe.remove(max)
        bestX.append(max)

    scores[n] = bestX

    # go back, helps in finding path later
    path = ['Stop']
    final = scores[n][x-1]
    path.append(final[1])

    for s in range((n-1), 0, -1):
        final = scores[s][final[1]][final[2]]
        path.append(final[1])

    path.append('Start')

    return scores, list(reversed(path))

#getting all necessary info for modified Viterbi algorithm
#change to the appropriate paths for ES/RU
train_file = open("/Users/sweeen/Downloads/Project/ES/train", "r", encoding='UTF-8')
ViterbiSentence = get_sentence("/Users/sweeen/Downloads/Project/ES/dev.in") 

train_emissions, train_labels, _ , _ =  get_train (train_file)
train_transitionRU = transition_parameter("/Users/sweeen/Downloads/Project/ES/train")[1]

with open ("/Users/sweeen/Downloads/Project/ES/dev.p3.out", "w" , encoding="UTF-8") as file :       #change here for ES/RU , RU/ES
    for sentence in ViterbiSentence:
        ListPath = (modifiedViterbi(5, train_labels, train_emissions, train_transitionRU, sentence))[1]
        for i in range(len(sentence)-1) :
            if ListPath[i] in ["Start" , 'Stop' ]: #dont want to append start and stop into dev2
                pass
            else:
                file.write(sentence[i] +" "+ ListPath[i+1])
                file.write ('\n')
        file.write('\n')

#python3 /Users/sweeen/Downloads/Project/EvalScript/evalResult.py /Users/sweeen/Downloads/Project/ES/dev.out /Users/sweeen/Downloads/Project/ES/dev.p3.out
#python3 /Users/sweeen/Downloads/Project/EvalScript/evalResult.py /Users/sweeen/Downloads/Project/RU/dev.out /Users/sweeen/Downloads/Project/RU/dev.p3.out