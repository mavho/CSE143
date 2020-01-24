import math
def main():
    # stores a mapping of tokens already seen. generates count.
    vocab = {}
    bivocab = {}
    # unigramProb stores key as word and value as prob of word/totalWord
    bigramProb = {}
    vocabProb = {}
    wordcount = initialize(vocab)
    print( "wordcount is" , wordcount)
    getUniProb(vocab,vocabProb,wordcount)
    cal_perplexity(vocab, wordcount)
    createbi(vocab,bivocab,'A1-Data/1b_benchmark_unks.train.tokens')
    print('count: ' + str(len(vocab)))
    getBiProb(vocab,bivocab,bigramProb)
    

def initialize(vocab):
    word_count = 0
    for line in ngram_generator('A1-Data/1b_benchmark.train.tokens'):
        for word in line.split():
            word_count += 1
            if word in vocab:
                vocab[word] += 1
            else:
                vocab[word] = 1
    
    ### tokens that appear less than 3 times are deleted and added to 'unk
    vocab['<unk>'] = 0
    for key in list(vocab):
        if vocab[key] < 3:
            vocab['<unk>'] += vocab[key]
            del vocab[key]

    ### prepend unks to file the name
    wc = replace_unknowns('A1-Data/1b_benchmark.train.tokens', 'A1-Data/1b_benchmark_unks.train.tokens', vocab)
    vocab['<unk>'] += replace_unknowns('A1-Data/1b_benchmark.dev.tokens', 'A1-Data/1b_benchmark_unks.dev.tokens', vocab)
    vocab['<unk>'] += replace_unknowns('A1-Data/1b_benchmark.test.tokens', 'A1-Data/1b_benchmark_unks.test.tokens', vocab)
    return word_count

### Given the probabilities of the n-grams
### calculate the perplexity of the sentence?
def cal_perplexity(vocab, wc):
    fileset = ['A1-Data/1b_benchmark_unks.train.tokens','A1-Data/1b_benchmark_unks.dev.tokens','A1-Data/1b_benchmark_unks.test.tokens']
    unigramProb = {}
    getUniProb(vocab, unigramProb, wc)
    ###
    ### for each n-gram in the sentence, 
    ### find the probability (given the probability dicts)
    ### of that ngram which is stored in the dictionary
    ### log and sum it up
    ###
    for file in fileset:
        print("fileset: " + file)
        L = 0 
        word_count = 0
        for line in  file_generator(file):
            line = line.split()
            line.insert(len(line), "<STOP>")
            ### Calculate perplexity of a sentence
            temp = 0
            for i in range(0, len(line)):
                word_count += 1
                prob = unigramProb[line[i]]
                temp += (-1 * math.log(prob, 2))
            L += temp 
        print(math.pow(2, L/word_count))

#vocab is only needed to remove unks   
def createbi(vocab, bivocab, file):
    #creates list of words from file
    for line in file_generator(file):
        temp = "<START> " + line + " <STOP>"
        temp = temp.split()
        for i in range(1, len(temp)):
            bigram = (temp[i - 1], temp[i])
            ### count of bigrams
            if bigram not in bivocab:
                bivocab[bigram] = 1
            else:
                bivocab[bigram] += 1
#prob(a|b) = prob(b,a)/prob(b)
def getBiProb(unigram_vocab,bigram_vocab,bigramProb):
    for key in bigram_vocab:
        if key[0] not in unigram_vocab:
            bigramProb[key] = 0 
        else:
            #print(bigram_vocab[key]/unigram_vocab[key[0]])
            bigramProb[key] = bigram_vocab[key]/unigram_vocab[key[0]]
    print(sum(bigramProb.values()))

def getUniProb(unigram,unigramProb, wc):
    runningSum = 0
    print(wc ,"wc is")
    for num in unigram:
        runningSum += unigram[num]
    for each in unigram:
        unigramProb[each] = unigram[each]/len(unigram)
    print(sum(unigramProb.values()))

def replace_unknowns(in_file, outfile, vocab):
    count = 0
    with open(file = in_file, mode='rb') as in_f, open(outfile,'wb') as outfile:
        for line in in_f:
            line = line.decode('utf-8')
            fline = ''
            for token in line.split():
                count += 1
                if token not in vocab:
                    token = '<unk>'
                    #replace replaces all tokens 
                fline += token + ' '
            fline = fline.strip()
            outfile.write(fline.encode('utf-8') + '\n'.encode('utf-8'))
    return count

def file_generator(file):
    with open(file = file, mode = 'rb') as _f:
        for line in _f:
            yield line.decode('utf-8')

def ngram_generator(file):
    ### read in byte
    with open(file=file, mode='rb')  as _f:
        for line in _f:
            yield line.decode('utf-8') + " <STOP>" # check here#

if __name__ == '__main__':
    main()