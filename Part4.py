separator = " "

def get_train_count(train_file):
    #calculate the number of times a word and label appears together
    #calculate the number of times a label appears
    #stores both of these in separate dictionaries
    no_of_lines = 0

    #the dictionary that stores the number of times a particular word and label appears together
    word_label_dict = {}

    #the dictionary that stores the number of times a particular label appears in total
    label_dict = {}

    for line in train_file:
        line = line.strip()

        if len(line) != 0:
            no_of_lines += 1
            label = line.rsplit(separator, 1)[1]

            if line in word_label_dict:
                word_label_dict[line] += 1

            else:
                word_label_dict[line] = 1

            if label in label_dict:
                label_dict[label] += 1

            else:
                label_dict[label] = 1

    return word_label_dict, label_dict, no_of_lines

def get_prob(word_label_dict, label_dict, no_of_lines):
    #get the probability that a word and label appears together
    #get the probability that a label appears
    #by using the number of times they appear / total number of lines
    word_label_prob = {}
    label_prob = {}
    most_common_label = ""

    for word_label in word_label_dict:
        word_label_prob[word_label] = word_label_dict[word_label] / no_of_lines

    for label in label_dict:
        label_prob[label] = label_dict[label] / no_of_lines

    #find the label that has the highest probability of appearing
    most_common_label = max(label_dict, key=label_dict.get)

    return word_label_prob, label_prob, most_common_label

def p_label_given_word(word_label_prob, label_prob):
    #calculate the probability of a label given a word
    #by using p(word and label appearing together) / p(label appearing)
    prob_label_given_word_dict = {}

    for word_label in word_label_prob:
        label = word_label.rsplit(separator, 1)[1]
        prob_label_given_word_dict[word_label] = word_label_prob[word_label] / label_prob[label]

    #since each word can have multiple labels, we keep only the label with highest probability
    copy_prob = prob_label_given_word_dict
    new_prob_label_given_word_dict = {}     #dictionary to append the labels with highest probability

    #for each word in prob_label_given_word_dict, we compare with all the words in the copy dictionary
    #to check for duplicate words (with different labels)
    #create a new_dict to store all instances of a particular word, eg. "apple, 0", "apple, I-positive"
    #we get the max instance from this new_dict and store inside new_prob_label_given_word_dict
    #repeat for all other words in prob_label_given_word_dict
    for wl in prob_label_given_word_dict:
        w = wl.rsplit(separator, 1)[0]
        new_dict = {}

        for wo_lab in copy_prob:
            wo = wo_lab.rsplit(separator, 1)[0]

            if w == wo: 
                new_dict[wo_lab] = copy_prob[wl]

        max_word_label = max(new_dict, key=new_dict.get)
        
        if max_word_label not in new_prob_label_given_word_dict:
            new_prob_label_given_word_dict[max_word_label] = new_dict[max_word_label]

    return new_prob_label_given_word_dict

def predict_test_set(new_prob_label_given_word_dictionary, test_file, most_common_label):
    #produce labels using the probabilities calculated in p_label_given_word function
    test_dict = {}
    entire_file_array = []

    #put all words in test file into a dictionary with default label most_common_label and temp value of 0
    #so that if the word does not appear in training set, that word is automatically given the most common label
    for line in test_file:
        line = line.strip()
        entire_file_array.append(line)
        
        if line != "":
            word = line + " " + most_common_label
            test_dict[word] = -1

    #for each word in test_dict aka for each word in test file, check if it exists in training dictionary
    for line in test_dict:
        line_word, line_label = line.rsplit(separator, 1)

        for item in new_prob_label_given_word_dictionary:
            item_word, item_label = item.rsplit(separator, 1)

            if line_word == item_word:
                line_label = item_label

                #to replace the old key with the correct label and probability
                test_dict.pop(line) #remove the old key from the dictionary
                line = line_word + " " + line_label #create the key again with the new label
                test_dict[line] = new_prob_label_given_word_dictionary[item]    #add the modified key into the output dictionary

    for item in entire_file_array:
        if item != "":
            for word_label in test_dict:
                words, label = word_label.rsplit(separator, 1)

                if item == words:
                    index = entire_file_array.index(item)
                    item = item + " " + label
                    entire_file_array[index] = item #updating the new word
                    
    return (entire_file_array)

#opening train and test files
ES_train_file = open("/Users/sweeen/Downloads/Project/ES/train", "r", encoding='UTF-8')
RU_train_file = open("/Users/sweeen/Downloads/Project/RU/train", "r", encoding='UTF-8')
ES_test_file = open("/Users/sweeen/Downloads/Project/ES/dev.in", "r", encoding='UTF-8')
RU_test_file = open("/Users/sweeen/Downloads/Project/RU/dev.in", "r", encoding='UTF-8')

#putting all the functions together to get the output to be written to file
def output(training_set, test_set):
    word_label_dict, label_dict, no_of_lines = get_train_count(training_set)
    word_label_prob, label_prob, most_common_label = get_prob(word_label_dict, label_dict, no_of_lines)
    prob_label_given_word_dict = p_label_given_word(word_label_prob, label_prob)
    output_array = predict_test_set(prob_label_given_word_dict, test_set, most_common_label)
    return output_array

ES_output = output(ES_train_file, ES_test_file)
RU_output = output(RU_train_file, RU_test_file)

#write the outputs to the appropriate dev.p4.out
with open ("/Users/sweeen/Downloads/Project/ES/dev.p4.out", "w" , encoding="UTF-8") as file:
    for item in ES_output:
        file.write(item)
        file.write ('\n')

with open ("/Users/sweeen/Downloads/Project/RU/dev.p4.out", "w" , encoding="UTF-8") as file:
    for item in RU_output:
        file.write(item)
        file.write ('\n')

#python3 /Users/sweeen/Downloads/Project/EvalScript/evalResult.py /Users/sweeen/Downloads/Project/ES/dev.out /Users/sweeen/Downloads/Project/ES/dev.p4.out
#python3 /Users/sweeen/Downloads/Project/EvalScript/evalResult.py /Users/sweeen/Downloads/Project/RU/dev.out /Users/sweeen/Downloads/Project/RU/dev.p4.out