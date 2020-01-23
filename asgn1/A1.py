import math
def main():
    # stores a mapping of tokens already seen. generates count.
    vocab = {}
    bivocab = {}
    # unigramProb stores key as word and value as prob of word/totalWord
    unigramProb = {}
    bigramProb = {}
    initialize(vocab)
    createbi(vocab,bivocab,'A1-Data/1b_benchmark_unks.train.tokens')
    print('count: ' + str(len(vocab)))
    getProb(vocab,unigramProb)
    getBiProb(vocab,bivocab,bigramProb)
    print(bigramProb)
    
    
def initialize(vocab):
    for line in ngram_generator('A1-Data/1b_benchmark.train.tokens'):
        for word in line.split():
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
    replace_unknowns('A1-Data/1b_benchmark.train.tokens', 'A1-Data/1b_benchmark_unks.train.tokens', vocab)
    vocab['<unk>'] += replace_unknowns('A1-Data/1b_benchmark.dev.tokens', 'A1-Data/1b_benchmark_unks.dev.tokens', vocab)
    vocab['<unk>'] += replace_unknowns('A1-Data/1b_benchmark.test.tokens', 'A1-Data/1b_benchmark_unks.test.tokens', vocab)



### Given the probabilities of the n-grams
### calculate the perplexity of the sentence?
def cal_perplexity(**kwargs):
    fileset = ['A1-Data/1b_benchmark_unks.train.tokens','A1-Data/1b_benchmark_unks.dev.tokens','A1-Data/1b_benchmark_unks.test.tokens']
    L = 23
    #for file in fileset:
    #    for line in  file_generator(file):
    #        for token in line.split():
                ### calculate the perpleity
#vocab is only needed to remove unks   
def createbi(vocab, bivocab, file):
    vocablist = []
    length = len(vocablist)
    #creates list of words from file
    for line in ngram_generator(file):
        for word in line.split():
            vocablist.append(word)
    #to make sure all unks are caught
    unkvocablist = list(vocab)
    length = len(vocablist)
    for x in range(0,length):
        if vocablist[x] not in unkvocablist:
            vocablist[x] = '<unk>'
    #actualbivocab creation
    vocablist2 = vocablist.copy()
    vocablist.pop(0)
    bivocablist=list(zip(vocablist2, vocablist))
    for item in bivocablist:
        if item in bivocab:
            bivocab[item] += 1
        else:
            bivocab[item] = 1

def getProb(unigram,unigramProb):
    print("# of stops")
    print(unigram["<STOP>"])
    print("len of unigram")
    print(len(unigram))
    for each in unigram:
        unigramProb[each] = unigram[each]/len(unigram)
# return prob of 1 word / all words
# store the prob of each word(key) : word / total words(value)
### Replace words that don't appear in training data.

#prob(a|b) = prob(a and b)/prob(b)
def getBiProb(unigram,bigram,bigramProb):
    for key in bigram:
        print(key)
        bigramProb[key]=bigram[key]/unigram[key[0]]
        
 


def replace_unknowns(in_file, outfile, vocab):
    count = 0
    with open(file = in_file, mode='rb') as in_f, open(outfile,'wb') as outfile:
        for line in in_f:
            line = line.decode('utf-8')
            for token in line.split():
                if token not in vocab:
                    count += 1
                    #replace replaces all tokens 
                    line = line.replace(' ' + token + ' ', ' <unk> ', )
            outfile.write(line.encode('utf-8'))
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