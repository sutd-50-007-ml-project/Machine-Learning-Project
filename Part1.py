import sys

def get_train(train_file):
    
    examples = 0
    lines = 0
    train_emission_types = {} # key: all unique words, value: concatenation of all labels (separated by ,) emitting the word
    train_emissions = {} # key: all unique emissions (by concatenating word + label), value: count of the emission
    # { "helloB-positive: 5", "worldB-negative: 1"}
    train_labels = {} # key: all uniqe labels, value: count of label
    train_words = [] # all the unique words in training set

    # column separator
    separator = ' '


    for line in train_file:
        line = line.strip()
        lines += 1
        if (len(line) == 0):
            examples += 1


        else:
            word, label = line.rsplit(separator, 1)
            emission = label + word

            if word not in train_words:
                train_words.append(word)
            
            if label in train_labels:
                train_labels[label] += 1
            else:
                train_labels[label] = 1
                
            if emission in train_emissions:
                train_emissions[emission] += 1
            else:
                train_emissions[emission] = 1 #### use train emisioo
            
            if word in train_emission_types:
                train_emission_types[word] += ','
                train_emission_types[word] += label
            else:
                train_emission_types[word] = label

    return train_emissions, train_labels, train_words, train_emission_types


# emission parameter = no. of times a label emits a word / no. of times the label appears in the sequence
def emission_parameter(train_word, train_label, train_emissions, train_words, train_labels):
    k = 1
    countOfLabels = train_labels[train_label]
    
    if train_word in train_words: # word appears in training_set
        test_emission = train_label + train_word
        countOfEmissions = train_emissions[test_emission]
        return countOfEmissions / (countOfLabels + k)
    
    else: # word does not appear in training_set i.e. token "#UNK#"
        return k / (countOfLabels + k)


# transition parameter =

# Objective: Train the model to get predictions for test set
# How it works: 
#  1. Find the max emission paramater for each word in training set.
#    The label prediction for each word will be the label that gives 
#    the highest emission parameter. (Since each word can be emitted
#    by multiple labels)
# 2. Find max emission parameter for #UNK# token, which is used
#    for words in test set that don't appear in training set. The 
#    label prediction for "UNK" is the label that returns the max
#    emission parameter, amongst all the 7 possible labels given 
#    k = 1.
# Returns: Predictions (or model) for test set
def max_emission_parameter(train_emission_types, train_emissions, train_words, train_labels):
    predictions = {} # key: word, value: label that gives the highest emission parameter for that word
    max_emission = {} # key: word, value: max emission parameter value for that word

    
    # special token
    unk = "#UNK#"
    # find highest emission parameter for all words in training set
    for word, labels in train_emission_types.items():
        max_em = 0
        predictions[word] = ''
        labels_list = labels.split(',')
        
        # find highest emission parameter for a unique word (which may be emitted by multiple labels)
        for label in labels_list:
            new_em = emission_parameter(word, label, train_emissions, train_words, train_labels)
            # if new emission parameter calculated is higher
            if new_em > max_em:  
                # update the emission parameter value and update the prediction label
                max_em = new_em
                # set prediction label as the label that generates a higher emission parameter
                predictions[word] = label
                max_emission[label+word] = max_em
    
    max_unk_em = 0  
    
    # find highest emission parameter for amongst all labels for "UNK" tag      
    for label in train_labels:
        new_em = emission_parameter(unk, label, train_emissions, train_words, train_labels)
        if new_em > max_unk_em:
            max_unk_em = new_em
            predictions[unk] = label
    return predictions, max_emission
    
# Returns: Entire content for the output file
def sentiment_analysis(train_data, test_file):
    output = ''
    
    # column separator
    separator = ' '
    
    # special token
    unk = "#UNK#"
    
    train_emissions = train_data[0]
    train_labels = train_data[1]
    train_words = train_data[2]
    train_emission_types = train_data[3]
    
    # train model and get predictions
    predictions, max_em = max_emission_parameter(train_emission_types, train_emissions, train_words, train_labels)
    # get label prediction for each input word in test file 
    for line in test_file:
        word = line.split('\n')[0]
        if word:
            if word in predictions: # word appears in training_set
                prediction_line = word + separator + predictions[word] + '\n'
                output += prediction_line
                # print(word, predictions[word])
            
            else: # word does not appear in training_set i.e. token "#UNK#"
                prediction_line = word + separator + predictions[unk] + '\n'
                output += prediction_line
                #print(word, predictions[unk])
        else: # no word i.e. empty line
            output += '\n'
        
    return output, max_em
    
    
### Main Function ###

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print ('Please make sure you have installed Python 3.4 or above!')
        print ("Usage on Windows:  python Part1.py train_path test_path output_path")
        print ("Usage on Linux/Mac:  python3 Part1.py train_path test_path output_path")
        sys.exit()

    train_file = open(sys.argv[1], "r", encoding='UTF-8')
    test_file = open(sys.argv[2], "r", encoding='UTF-8')
    output_file = open(sys.argv[3], "w", encoding='UTF-8')

    # column separator
    separator = ' '

    # special token
    unk = "#UNK#"

    # Read training data
    train_data = get_train(train_file)

    # Make prediction using test data
    output, _ = sentiment_analysis(train_data, test_file)

    # Write prediction output to file
    output_file.write(output)