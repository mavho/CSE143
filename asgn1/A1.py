import math
import smoothing as SM
def main():
    # stores a mapping of tokens already seen. generates count.
    vocab = {}
    bivocab = {}
    trivocab = {}
    SM.smoothing(names = 'hello', bigram = vocab)
    # unigramProb stores key as word and value as prob of word/totalWord
    bigramProb = {}
    trigramProb = {}
    wordcount = initialize(vocab)

    
    createbi(vocab,bivocab,'A1-Data/1b_benchmark_unks.train.tokens')
    print('count: ' + str(len(vocab)))
    getBiProb(vocab,bivocab,bigramProb)

    createtri(bivocab,trivocab,'A1-Data/1b_benchmark_unks.train.tokens')
    getTriProb(bivocab,trivocab,trigramProb)

    cal_perplexity(vocab, wordcount, bigramProb,trigramProb)
    

def initialize(vocab):
    word_count = 0
    ### includes the stop
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
            vocab.pop(key)

    ### prepend unks to file the name
    wc = replace_unknowns('A1-Data/1b_benchmark.train.tokens', 'A1-Data/1b_benchmark_unks.train.tokens', vocab)
    replace_unknowns('A1-Data/1b_benchmark.dev.tokens', 'A1-Data/1b_benchmark_unks.dev.tokens', vocab)
    replace_unknowns('A1-Data/1b_benchmark.test.tokens', 'A1-Data/1b_benchmark_unks.test.tokens', vocab)
    return word_count

### Given the probabilities of the n-grams
### calculate the perplexity of the sentence?
def cal_perplexity(vocab, wc, bigramProb, trigramProb):
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
        for line in  SM.file_generator(file):
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
    
    ### calculating bi grams
    for file in fileset:
        print("fileset: " + file)
        L = 0 
        word_count = 0
        ZERO_FLAG = False
        for line in  SM.file_generator(file):
            line = line.split()
            line.insert(len(line), "<STOP>")
            ### adds number of tokens in a sentence, exclude START
            word_count += len(line)
            line.insert(0, "<START>")
            ### Calculate perplexity of a sentence
            temp = 0
            for i in range(1, len(line)):
                bigram = (line[i-1], line[i])
                if bigram in bigramProb:
                    prob = bigramProb[bigram]
                    temp += (-1 * math.log(prob, 2))
                else:
                    ZERO_FLAG = True
                    break
            L += temp 
        if ZERO_FLAG:
            print('Zero Encountered: INFIN')
        else:
            print(math.pow(2, L/word_count))
        
    for file in fileset:
        print("fileset: " + file)
        L = 0 
        word_count = 0
        ZERO_FLAG = False
        for line in  SM.file_generator(file):
            line = line.split()
            line.insert(len(line), "<STOP>")
            ### adds number of tokens in a sentence, exclude START
            word_count += len(line)
            line.insert(0, "<START>")
            ### Calculate perplexity of a sentence
            temp = 0
            for i in range(2, len(line)):
                trigram = (line[i-2], line[i-1], line[i])
                if trigram in trigramProb:
                    prob = trigramProb[trigram]
                    temp += (-1 * math.log(prob, 2))
                else:
                    ZERO_FLAG = True
                    break
            L += temp 
        if ZERO_FLAG:
            print('Zero Encountered: INFIN')
        else:
            print(math.pow(2, L/word_count))
#vocab is only needed to remove unks   
def createbi(vocab, bivocab, file):
    #creates list of words from file
    for line in SM.file_generator(file):
        temp = "<START> " + line + " <STOP>"
        temp = temp.split()
        for i in range(1, len(temp)):
            bigram = (temp[i - 1], temp[i])
            ### count of bigrams
            if bigram not in bivocab:
                bivocab[bigram] = 1
            else:
                bivocab[bigram] += 1

def createtri(bivocab,trivocab,file):
    for line in SM.file_generator(file):
        temp = "<START> " + line + " <STOP>"
        temp = temp.split()
        for i in range(2, len(temp)):
            trigram = (temp[i - 2] , temp [ i-1] , temp[i])
            if trigram not in trivocab:
                trivocab[trigram] = 1
            else:
                trivocab[trigram] +=1


#prob(a|b) = prob(b,a)/prob(b)

def getUniProb(unigram,unigramProb, wc):
    for each in unigram:
        unigramProb[each] = unigram[each]/wc
    print("unigram sum")
    print(sum(unigramProb.values()))

def getBiProb(unigram_vocab,bigram_vocab,bigramProb):
    for key in bigram_vocab:
            #print(bigram_vocab[key]/unigram_vocab[key[0]])
            bigramProb[key] = bigram_vocab[key]/unigram_vocab[key[1]]
    print("bigram sum")
    print(sum(bigramProb.values()))

def getTriProb(bigram_vocab,trivocab,trigramProb):
    for key in trivocab:
        trigramProb[key] = trivocab[key]/bigram_vocab[key[:2]]
    print("trigram sum")
    print(sum(trigramProb.values()))



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
                fline += ' ' + token + ' '
            
            ### count stop
            count += 1
            fline = fline.strip()
            outfile.write(fline.encode('utf-8') + '\n'.encode('utf-8'))
    return count


def ngram_generator(file):
    ### read in byte
    with open(file=file, mode='rb')  as _f:
        for line in _f:
            yield line.decode('utf-8') + " <STOP>" # check here#

if __name__ == '__main__':
    main()
