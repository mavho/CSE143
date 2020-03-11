# -*- coding: utf-8 -*-
"""CSE-143_A3_Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r4RY4WuXJKrwH9Ju0hQeV2brXq_Nzvpt
"""
### Unquote bottom line when running on colab.
"""
from google.colab import drive
drive.mount('/content/gdrive/')
import os
import sys
print(os.listdir('/content/gdrive/My Drive/CSE-143-A3'))
sys.path.append('/content/gdrive/My Drive/CSE-143-A3')

directory = '/content/gdrive/My Drive/CSE-143-A3'
"""
### Unquote top line when running on colab.

import random
from conlleval import evaluate as conllevaluate

def decode(input_length, tagset, score):
    """
    Compute the highest scoring sequence according to the scoring function.
    :param input_length: int. number of tokens in the input including <START> and <STOP>
    :param tagset: Array of strings, which are the possible tags.  Does not have <START>, <STOP>
    :param score: function from current_tag (string), previous_tag (string), i (int) to the score.  i=0 points to
        <START> and i=1 points to the first token. i=input_length-1 points to <STOP>
    :return: Array strings of length input_length, which is the highest scoring tag sequence including <START> and <STOP>
    """
    ### insert start tag  
    tagset_len = len(tagset)
    SA = [[0]*input_length for i in range(tagset_len)]
    BP = [[0]*input_length for i in range(tagset_len)]
    #print(tagset)
    """
    SA stores the scores
    each column represents a token in the input
    each row represents a tag
        x0 x1 x2 x3 x4.... xn
    t0
    t1
    t2
    t3
    .
    ty
    """
    max_score = -999
    max_tag = 0
    ### Base case 
    for i in range(tagset_len):
        ### this part i'm the least sure about, should 0 be 0 or 1. changing it to either doesn't really matter
        local_score = score(tagset[i],"<START>", 1)
        if local_score > max_score:
            max_score = local_score
            max_tag = i
        SA[i][0] = max_score 
        BP[i][0] = max_tag 

    ### SA[i][tag] = max of (score(blah blah blah) + previous SA[i][tag-1])


    """
    for first word token till last word token
        for each tag:
            find the max of all score(tag,tag', token pos) + previous word's tag' score
            store SA[tag][pos] = max score
            store BP[tag][pos] = tag' that achieved this max store
    """
    for i in range(1,input_length - 1):
        ### go through the pairs of tags
        for tag in range(tagset_len):
            max_score = -99999
            max_tag = 0  
            #print("%d Current tag pair %s, %s" % (i,tagset[tag],tagset[tag-1]))
            for pair in range(tagset_len):
                local_score = SA[pair][i-1] + score(tagset[tag],tagset[pair],i)
                if(local_score > max_score):
                    max_score = local_score
                    max_tag = pair
            BP[tag][i] = max_tag
            SA[tag][i] = max_score

    ### last row of input
    M = input_length - 1 
    max_score = -999 
    max_tag = -1 
    """
    The last token <STOP> is handled a little differently, but still really the same
    Goal of this is to obtain the best tag' that achieved the max
    we'll store that tag in max_tag
    """
    for i in range(tagset_len):
        end_score = score('<STOP>', tagset[i], M) + SA[i][M-1]
        if end_score > max_score:
            max_score = end_score
            max_tag = i 
    res = [0] * (M + 1)
    res[len(res)-1] = max_tag
    for m in reversed(range(1,M)):
        res[m] = BP[res[m+1]][m]
    """
    for i in SA:
        print(i)
    for i in BP:
        print(i)
    """
    for key,val in enumerate(res):
        res[key] = tagset[val]
    res[0] = '<START>'
    res[len(res)-1] = '<STOP>'

    # Look at the function compute_score for an example of how the tag sequence should be scored
    return res

def compute_score(tag_seq, input_length, score):
    """
    Computes the total score of a tag sequence
    :param tag_seq: Array of String of length input_length. The tag sequence including <START> and <STOP>
    :param input_length: Int. input length including the padding <START> and <STOP>
    :param score: function from current_tag (string), previous_tag (string), i (int) to the score.  i=0 points to
        <START> and i=1 points to the first token. i=input_length-1 points to <STOP>
    :return:
    """
    total_score = 0
    for i in range(1, input_length):
        total_score += score(tag_seq[i], tag_seq[i - 1], i)
    return total_score


def compute_features(tag_seq, input_length, features):
    """
    Compute f(xi, yi)
    :param tag_seq: [tags] already padded with <START> and <STOP>
    :param input_length: input length including the padding <START> and <STOP>
    :param features: func from token index to FeatureVector
    :return:
    """
    feats = FeatureVector({})
    for i in range(1, input_length):
        feats.times_plus_equal(1, features.compute_features(tag_seq[i], tag_seq[i - 1], i))
    return feats


def sgd(training_size, epochs, gradient, parameters, training_observer):
    """
    Stochastic gradient descent
    :param training_size: int. Number of examples in the training set
    :param epochs: int. Number of epochs to run SGD for
    :param gradient: func from index (int) in range(training_size) to a FeatureVector of the gradient
    :param parameters: FeatureVector.  Initial parameters.  Should be updated while training
    :param training_observer: func that takes epoch and parameters.  You can call this function at the end of each
           epoch to evaluate on a dev set and write out the model parameters for early stopping.
    :return: final parameters
    """
    # Look at the FeatureVector object.  You'll want to use the function times_plus_equal to update the
    # parameters.
    # To implement early stopping you can call the function training_observer at the end of each epoch.
    return


def train(data, feature_names, tagset, epochs):
    """
    Trains the model on the data and returns the parameters
    :param data: Array of dictionaries representing the data.  One dictionary for each data point (as created by the
        make_data_point function).
    :param feature_names: Array of Strings.  The list of feature names.
    :param tagset: Array of Strings.  The list of tags.
    :param epochs: Int. The number of epochs to train
    :return: FeatureVector. The learned parameters.
    """
    parameters = FeatureVector({})

    def perceptron_gradient(i):
        """
        Computes the gradient of the Perceptron loss for example i
        :param i: Int
        :return: FeatureVector
        """
        inputs = data[i]
        input_len = len(inputs['tokens'])
        gold_labels = inputs['gold_tags']
        features = Features(inputs, feature_names)

        def score(cur_tag, pre_tag, i):
            return parameters.dot_product(features.compute_features(cur_tag, pre_tag, i))

        tags = decode(input_len, tagset, score)
        fvector = compute_features(tags, input_len, features)           # Add the predicted features
        #print('Input:', inputs)        # helpful for debugging
        #print("Predicted Feature Vector:", fvector.fdict)
        #print("Predicted Score:", parameters.dot_product(fvector))
        fvector.times_plus_equal(-1, compute_features(gold_labels, input_len, features))    # Subtract the features for the gold labels
        #print("Gold Labels Feature Vector: ", compute_features(gold_labels, input_len, features).fdict)
        #print("Gold Labels Score:", parameters.dot_product(compute_features(gold_labels, input_len, features)))
        return fvector

    def training_observer(epoch, parameters):
        """
        Evaluates the parameters on the development data, and writes out the parameters to a 'model.iter'+epoch and
        the predictions to 'ner.dev.out'+epoch.
        :param epoch: int.  The epoch
        :param parameters: Feature Vector.  The current parameters
        :return: Double. F1 on the development data
        """
        dev_data = read_data('ner.dev')
        (_, _, f1) = evaluate(dev_data, parameters, feature_names, tagset)
        write_predictions('ner.dev.out'+str(epoch), dev_data, parameters, feature_names, tagset)
        parameters.write_to_file('model.iter'+str(epoch))
        return f1

    return sgd(len(data), epochs, perceptron_gradient, parameters, training_observer)


def predict(inputs, input_len, parameters, feature_names, tagset):
    """
    :param inputs:
    :param input_len:
    :param parameters:
    :param feature_names:
    :param tagset:
    :return:
    """
    features = Features(inputs, feature_names)
    ### in a linear model, local scoring function can be defined as a dot product of weights and features.
    #print(features.inputs['gold_tags'])
    
    def score(cur_tag, pre_tag, i):
        return parameters.dot_product(features.compute_features(cur_tag, pre_tag, i))

    return decode(input_len, tagset, score)


def make_data_point(sent):
    """
        Creates a dictionary from String to an Array of Strings representing the data.  The dictionary items are:
        dic['tokens'] = Tokens padded with <START> and <STOP>
        dic['pos'] = POS tags padded with <START> and <STOP>
        dic['NP_chunk'] = Tags indicating noun phrase chunks, padded with <START> and <STOP>
        dic['gold_tags'] = The gold tags padded with <START> and <STOP>
    :param sent: String.  The input CoNLL format string
    :return: Dict from String to Array of Strings.
    """
    dic = {}
    sent = [s.strip().split() for s in sent]
    dic['tokens'] = ['<START>'] + [s[0] for s in sent] + ['<STOP>']
    dic['pos'] = ['<START>'] + [s[1] for s in sent] + ['<STOP>']
    dic['NP_chunk'] = ['<START>'] + [s[2] for s in sent] + ['<STOP>']
    dic['gold_tags'] = ['<START>'] + [s[3] for s in sent] + ['<STOP>']
    return dic

def read_data(filename):
    """
    Reads the CoNLL 2003 data into an array of dictionaries (a dictionary for each data point).
    :param filename: String
    :return: Array of dictionaries.  Each dictionary has the format returned by the make_data_point function.
    """
    data = []
    with open(filename, 'r') as f:
        sent = []
        for line in f.readlines():
            if line.strip():
                sent.append(line)
            else:
                data.append(make_data_point(sent))
                sent = []
        data.append(make_data_point(sent))

    return data

def write_predictions(out_filename, all_inputs, parameters, feature_names, tagset):
    """
    Writes the predictions on all_inputs to out_filename, in CoNLL 2003 evaluation format.
    Each line is token, pos, NP_chuck_tag, gold_tag, predicted_tag (separated by spaces)
    Sentences are separated by a newline
    The file can be evaluated using the command: python conlleval.py < out_file
    :param out_filename: filename of the output
    :param all_inputs:
    :param parameters:
    :param feature_names:
    :param tagset:
    :return:
    """
    count = 0
    with open(out_filename, 'w', encoding='utf-8') as f:
        for inputs in all_inputs:
            input_len = len(inputs['tokens'])
            tag_seq = predict(inputs, input_len, parameters, feature_names, tagset)
            for i, tag in enumerate(tag_seq[1:-1]):  # deletes <START> and <STOP>
                f.write(' '.join([inputs['tokens'][i+1], inputs['pos'][i+1], inputs['NP_chunk'][i+1], inputs['gold_tags'][i+1], tag])+'\n') # i + 1 because of <START>
            f.write('\n')

def evaluate(data, parameters, feature_names, tagset):
    """
    Evaluates precision, recall, and F1 of the tagger compared to the gold standard in the data
    :param data: Array of dictionaries representing the data.  One dictionary for each data point (as created by the
        make_data_point function)
    :param parameters: FeatureVector.  The model parameters
    :param feature_names: Array of Strings.  The list of features.
    :param tagset: Array of Strings.  The list of tags.
    :return: Tuple of (prec, rec, f1)
    """
    all_gold_tags = [ ]
    all_predicted_tags = [ ]
    for inputs in data:
        all_gold_tags.extend(inputs['gold_tags'][1:-1])  # deletes <START> and <STOP>
        input_len = len(inputs['tokens'])
        all_predicted_tags.extend(predict(inputs, input_len, parameters, feature_names, tagset)[1:-1]) # deletes <START> and <STOP>
    return conllevaluate(all_gold_tags, all_predicted_tags)


def main_predict(data_filename, model_filename):
    """
    Main function to make predictions.
    Loads the model file and runs the NER tagger on the data, writing the output in CoNLL 2003 evaluation format to data_filename.out
    :param data_filename: String
    :param model_filename: String
    :return: None
    """
    data = read_data(data_filename)
    parameters = FeatureVector({})
    parameters.read_from_file(model_filename)

    tagset = ['B-PER', 'B-LOC', 'B-ORG', 'B-MISC', 'I-PER', 'I-LOC', 'I-ORG', 'I-MISC', 'O']
    feature_names = ['tag', 'prev_tag', 'current_word']

    write_predictions(data_filename+'.out', data, parameters, feature_names, tagset)
    evaluate(data, parameters, feature_names, tagset)

    return


def main_train():
    """
    Main function to train the model
    :return: None
    """
    print('Reading training data')
    train_data = read_data('ner.train')
    #train_data = read_data('ner.train')[1:1] # if you want to train on just one example

    tagset = ['B-PER', 'B-LOC', 'B-ORG', 'B-MISC', 'I-PER', 'I-LOC', 'I-ORG', 'I-MISC', 'O']
    feature_names = ['tag', 'prev_tag', 'current_word']

    print('Training...')
    parameters = train(train_data, feature_names, tagset, epochs=10)
    print('Training done')
    dev_data = read_data('ner.dev')
    evaluate(dev_data, parameters, feature_names, tagset)
    test_data = read_data('ner.test')
    evaluate(test_data, parameters, feature_names, tagset)
    parameters.write_to_file('model')

    return


class Features(object):
    def __init__(self, inputs, feature_names):
        """
        Creates a Features object
        :param inputs: Dictionary from String to an Array of Strings.
            Created in the make_data_point function.
            inputs['tokens'] = Tokens padded with <START> and <STOP>
            inputs['pos'] = POS tags padded with <START> and <STOP>
            inputs['NP_chunk'] = Tags indicating noun phrase chunks, padded with <START> and <STOP>
            inputs['gold_tags'] = DON'T USE! The gold tags padded with <START> and <STOP>
        :param feature_names: Array of Strings.  The list of features to compute.
        """
        self.feature_names = feature_names
        self.inputs = inputs

    def compute_features(self, cur_tag, pre_tag, i):
        """
        Computes the local features for the current tag, the previous tag, and position i
        :param cur_tag: String.  The current tag.
        :param pre_tag: String.  The previous tag.
        :param i: Int. The position
        :return: FeatureVector
        """
        ### self.inputs['tokens'][i] is the current word
        #print("Current word %s" % (self.inputs['tokens'][i]))
        feats = FeatureVector({})
        if 'tag' in self.feature_names:
            feats.times_plus_equal(1, FeatureVector({'t='+cur_tag: 1}))
        if 'prev_tag' in self.feature_names:
            feats.times_plus_equal(1, FeatureVector({'ti='+cur_tag+"+ti-1="+pre_tag: 1}))
        if 'current_word' in self.feature_names:
            feats.times_plus_equal(1, FeatureVector({'t='+cur_tag+'+w='+self.inputs['tokens'][i]: 1}))
        return feats

class FeatureVector(object):

    def __init__(self, fdict):
        self.fdict = fdict

    def times_plus_equal(self, scalar, v2):
        """
        self += scalar * v2
        :param scalar: Double
        :param v2: FeatureVector
        :return: None
        """
        for key, value in v2.fdict.items():
            self.fdict[key] = scalar * value + self.fdict.get(key, 0)


    def dot_product(self, v2):
        """
        Computes the dot product between self and v2.  It is more efficient for v2 to be the smaller vector (fewer
        non-zero entries).
        :param v2: FeatureVector
        :return: Int
        """
        retval = 0
        for key, value in v2.fdict.items():
            #print("%s : %d : %d" % (key,value, self.fdict.get(key,0)))
            retval += value * self.fdict.get(key, 0)
        return retval

    def write_to_file(self, filename):
        """
        Writes the feature vector to a file.
        :param filename: String
        :return: None
        """
        print('Writing to ' + filename)
        with open(filename, 'w', encoding='utf-8') as f:
            for key, value in self.fdict.items():
                f.write('{} {}\n'.format(key, value))


    def read_from_file(self, filename):
        """
        Reads a feature vector from a file.
        :param filename: String
        :return: None
        """
        self.fdict = {}
        with open(filename, 'r') as f:
            for line in f.readlines():
                txt = line.split()
                self.fdict[txt[0]] = float(txt[1])

main_predict('ner.dev', 'model.simple')  # Uncomment to predict on 'dev.ner' using the model 'model.simple' (need to implement 'decode' function)
#main_train()    # Uncomment to train a model (need to implement 'sgd' function)

"""To sort the model weights for easy viewing, you can use Unix commands:"""

#!cat "/content/gdrive/My Drive/CSE-143-A3/model" | awk '{print $2, $1}' | sort -gr > "/content/gdrive/My Drive/CSE-143-A3/model.sorted.txt"

"""The file `model.sorted.txt` will be viewable in your Google Drive folder."""
