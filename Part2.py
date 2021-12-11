import math
import os
import sys
from Part1 import get_train, max_emission_parameter, sentiment_analysis

# column separator
separator = ' '

# special token
unk = "#UNK#"
    
def get_sentence(file) :

    devinfile = open(file, "r", encoding='UTF-8')
    SingleSentence = ["Start"]
    EntireFileSentence = []
    for line in devinfile :
        line = line.strip()

        if line == "":
            SingleSentence.append("Stop")
            EntireFileSentence.append(SingleSentence)
            SingleSentence = ["Start"]
        else :
            SingleSentence.append(line)

    return EntireFileSentence #returns the entire file's, in lists. Each list contains 1 sentence

#Part2 i)
def transition_parameter(pathtofile):
    # countuv/countu
    u_lab = {}
    uv_lab = {}
    z = {}
    currentState = 'Start' #initialise the start


    for line in open(pathtofile, 'r', encoding="UTF-8"):
        if currentState == 'Stop':
            previousState = 'Start'
        else:
            previousState = currentState

        line = line.rstrip()
        splitline = line.split(' ')
        x = splitline[:-1]
        currentState = splitline[-1]  ##deals with the special indents from the Russian Learn

        if currentState in u_lab:
            u_lab[currentState] += 1
        else:
            u_lab[currentState] = 1

        if previousState in u_lab:
            u_lab[previousState] += 1
        else:
            u_lab[previousState] = 1

        #transition is tupple, emision is string, viterbi

        if (previousState, currentState) in uv_lab:
            uv_lab[(previousState, currentState)] += 1
        else:
            uv_lab[(previousState, currentState)] = 1

        #
        # print(uv_lab)
        # print (u_lab)


        for w, countu in u_lab.items():
            for v in u_lab:
                if (w, v) in uv_lab:
                    countuv = uv_lab[(w, v)]
                    z[(w, v)] = countuv / countu
    #
    #
    # print(z)
    # print (list(u_label.keys()))
    # print (list(u_label.keys()), z)
    return list(u_lab.keys()), z



train_transitionES = transition_parameter("/Users/ouryuuzeno/Downloads/Project/ES/train")[1]
train_transitionRU = transition_parameter("/Users/ouryuuzeno/Downloads/Project/RU/train")[1]
#print (train_transitionES)

#Part3 ii)

def viterbiAlgo(states, emission, transition, sentence):
    #
    #     #part1 of psuedocode from lecture π(0, u) = {
    #                                                   1
    #                                                   0
    # if u = START
    # otherwise
    emii = emission
    transii = transition
    n = len(sentence)

    takesmallest = math.log(sys.float_info.min) - 1 #prevents underflow by utilising Log

    scores = {} #score is a dictionary
    scores[0] = {}

    for j in states:
        initialQuerry = str(j) + sentence[0] #convert part 1's emission_parameter
        if ("Start", j) in transii: ###
            # prevents underflow by utilising Log
            transit = math.log(transii[("Start", j)])
        else:
            transit = takesmallest



        if initialQuerry in emii: #convert part 1's emission_parameter into string to be used
            emit = math.log(emii[initialQuerry])
        else:
            emit = takesmallest

        required = transit + emit
        scores[0][j] = (required, "Start")

    scores[n] = {}
    maxprobe = []

    #part2 of psuedocode from lecture -- . For j = 0…n − 1, for each u ∈ T π(j + 1, u) = maxv{π(j, v) × bu(xj+1) × av,u}
    for i in range(1, n):
        scores[i] = {}
        for j in states:
            maxprobe = []
            for l in states:
                if (l, j) in transii:
                    transit = math.log(transii[(l, j)])
                else:
                    transit = takesmallest

                querry =  str(j) + sentence[i]
                if querry in emii:

                    emit = math.log(emii[querry])

                else:
                    emit = takesmallest
                score = scores[i - 1][l][0] + transit + emit
                maxprobe.append(score)

            required = max(maxprobe) #cant use numpy
            required_state = list(states.keys())[maxprobe.index(required)]
            scores[i][j] = (required, required_state)

    # STOP state

    for j in states:
        if (j, "Stop") in transii:
            transit = math.log(transii[(j, "Stop")])
        else:
            transit = takesmallest
        score = scores[n - 1][j][0] + transit
        maxprobe.append(score)

    stop = max(maxprobe)
    required_state = list(states.keys())[maxprobe.index(stop)]
    scores[n] = (stop, required_state)

    # go back, helps in finding path later
    #yn∗= arg maxu {π(n, u) ⋅ au,STOP}
    path = ['Stop']
    final = scores[n][1]
    path.append(final)

    for k in range((n - 1), -1, -1):
        final = scores[k][final][1]
        path.append(final)

    return scores, list(reversed(path))


# test_file = open(sys.argv[2], "r", encoding='UTF-8')
# output_file = open(sys.argv[3], "w", encoding='UTF-8')
train_file = open("/Users/ouryuuzeno/Downloads/Project/RU/train", "r", encoding='UTF-8')
ViterbiSentence = get_sentence("/Users/ouryuuzeno/Downloads/Project/RU/dev.in") 

test_file = open("/Users/ouryuuzeno/Downloads/Project/RU/dev.in", "r", encoding='UTF-8')
train_data = get_train (train_file) #gather what i need for viterbi

train_emissions = train_data[0]
train_labels = train_data[1]
train_words = train_data[2]
train_emission_types = train_data[3]

# print("Train emissions" + str(train_emissions))
_, max_em = sentiment_analysis(train_data, test_file)
# print("Max Emission Parameters: " + str(max_em))

#
# with open ("ES\dev.p2.out", "a" , encoding="utf-8") as file :
#     for sentence in ViterbiSentence:
#
#         file.write(str(viterbiAlgo(train_labels, train_emissions, train_transitionES, sentence)[0]))
#         file.write ('\n')

#
with open ("/Users/ouryuuzeno/Downloads/Project/RU/dev.p2.out", "w" , encoding="UTF-8") as file :       #change here for ES/RU , RU/ES
    for sentence in ViterbiSentence:
        ListPath = (viterbiAlgo(train_labels, max_em, train_transitionRU, sentence))[1] #change here for ES/RU , RU/ES
        for i in range(len(sentence)-1) :
            if ListPath[i] in ["Start" , 'Stop' ]: #dont want to append start and stop into dev2
                pass
            else:
                file.write(sentence[i] +" "+ ListPath[i+1])
                file.write ('\n')
                # print (sentence[i] +" "+ ListPath[i+1] )
        file.write('\n')



#python EvalScript/evalResult.py ES/dev.out ES/dev.p2.out

#python3 /Users/ouryuuzeno/Downloads/Project/EvalScript/evalResult.py /Users/ouryuuzeno/Downloads/Project/ES/dev.out /Users/ouryuuzeno/Downloads/Project/ES/dev.p2.out
#python3 /Users/ouryuuzeno/Downloads/Project/EvalScript/evalResult.py /Users/ouryuuzeno/Downloads/Project/RU/dev.out /Users/ouryuuzeno/Downloads/Project/RU/dev.p2.out