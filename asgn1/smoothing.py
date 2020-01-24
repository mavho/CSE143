import math
### Calculates perplexity, and smooths out the probabilities
def smoothing(**kwargs):
    print("Smoothing function")
    fileset = ['A1-Data/1b_benchmark_unks.train.tokens','A1-Data/1b_benchmark_unks.dev.tokens','A1-Data/1b_benchmark_unks.test.tokens']
    lambdas = (kwargs['l1'], kwargs['l2'], kwargs['l3'])
    ### calculating bi grams
    for file in fileset:
        print("Bigrams fileset: " + file)
        L = 0
        word_count = 0
        for line in  file_generator(file):
            line = line.split()
            line.insert(len(line), "<STOP>")
            ### adds number of tokens in a sentence, exclude START
            word_count += len(line)
            line.insert(0, "<START>")
            ### Calculate perplexity of a sentence
            temp = 0
            for i in range(1, len(line)):
                bigram = (line[i-1], line[i])
                prob = smooth(bigram, uniProb = kwargs['unigramProb'], biProb = kwargs['bigramProb'], lambdas = lambdas)
                temp += (-1 * math.log(prob, 2))
            L += temp
        print(math.pow(2, L/word_count))

    ### calculating tri grams
    for file in fileset:
        print("Trigrams fileset: " + file)
        L = 0
        word_count = 0
        for line in  file_generator(file):
            line = line.split()
            line.insert(len(line), "<STOP>")
            ### adds number of tokens in a sentence, exclude START
            word_count += len(line)
            line.insert(0, "<START>")
            ### Calculate perplexity of a sentence
            temp = 0
            for i in range(2, len(line)):
                trigram = (line[i-2],line[i-1], line[i])
                prob = smooth(trigram, uniProb = kwargs['unigramProb'], biProb = kwargs['bigramProb'],triProb=kwargs['trigramProb'], lambdas = lambdas)
                temp += (-1 * math.log(prob, 2))
            L += temp
        print(math.pow(2, L/word_count))

### takes 3 lambdas, applies it to the probabilities of the n_grams
def smooth(n_gram, **kwargs):
    prob = 0
    lambdas = kwargs['lambdas']
    ### smoothing bigram
    if len(n_gram) == 2:
        unigram = n_gram[1]
        bigram = n_gram
        ### if the bigram isn't in the dict, it's prob is 0
        if bigram not in kwargs['biProb']:
            prob = (lambdas[0] * kwargs['uniProb'][unigram]) + (lambdas[1] * 0)
            else:
        prob = (lambdas[0] * kwargs['uniProb'][unigram]) + (lambdas[1] * kwargs['biProb'][bigram])

    if len(n_gram) == 3:
        unigram = n_gram[2]
        bigram = n_gram[:2]
        trigram = n_gram
        ### uni, bi, tri -gram probabilities
        bgProb = 0
        tgProb = 0
        if trigram  in kwargs['triProb']:
            tgProb = lambdas[2] * kwargs['triProb'][trigram]
        if bigram in kwargs['biProb']:
            bgProb = lambdas[1] * kwargs['biProb'][bigram]
        ### not going to do edge case of unigram not in unigram - cause it will be in unigram
        prob = (lambdas[0] * kwargs['uniProb'][unigram]) + bgProb + tgProb 

    return(prob)
def file_generator(file):
    with open(file = file, mode = 'rb') as _f:
        for line in _f:
            yield line.decode('utf-8')