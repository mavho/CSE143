import math
import smoothing as SM

def main():
    ### store count of ngrams
    vocab = {}
    bivocab = {}
    trivocab = {}
    ### store probabilities of ngrams
    bigramProb = {}
    trigramProb = {}
    unigramProb = {}

    wordcount = initialize(vocab)

    getUniProb(vocab, unigramProb, wordcount)

    createbi(vocab,bivocab,'A1-Data/1b_benchmark_unks.train.tokens')
    getBiProb(vocab,bivocab,bigramProb)

    createtri(bivocab,trivocab,'A1-Data/1b_benchmark_unks.train.tokens')
    getTriProb(bivocab,trivocab,trigramProb)

    cal_perplexity(vocab, wordcount,unigramProb, bigramProb, trigramProb)

    SM.smoothing(unigramProb = unigramProb, bigramProb = bigramProb, trigramProb = trigramProb, l1 = 0.2, l2 = 0.3, l3 =0.5)
    

### initializes the starting vocab. Replaces words under 3 with unk. Replace in all files
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

    ### replace unks in files
    replace_unknowns('A1-Data/1b_benchmark.train.tokens', 'A1-Data/1b_benchmark_unks.train.tokens', vocab)
    replace_unknowns('A1-Data/1b_benchmark.dev.tokens', 'A1-Data/1b_benchmark_unks.dev.tokens', vocab)
    replace_unknowns('A1-Data/1b_benchmark.test.tokens', 'A1-Data/1b_benchmark_unks.test.tokens', vocab)
    return word_count

### for each n-gram in the sentence, 
### find the probability (given the probability dicts)
### of that ngram which is stored in the dictionary
### log and sum it up
def cal_perplexity(vocab, wc,unigramProb, bigramProb, trigramProb):
    fileset = ['A1-Data/1b_benchmark_unks.train.tokens','A1-Data/1b_benchmark_unks.dev.tokens','A1-Data/1b_benchmark_unks.test.tokens']
    ### perplexity of unigrams
    for file in fileset:
        print("fileset: " + file)
        L = 0 
        word_count = 0
        for line in  SM.file_generator(file):
            line = line.split()
            line.insert(len(line), "<STOP>")
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
        for line in SM.file_generator(file):
            if ZERO_FLAG:
                break
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
            if ZERO_FLAG:
                break
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

### fills the bigram dictionary with count of each bigram
def createbi(vocab, bivocab, file):
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

### fills the trigram dictionary with count of each trigram
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


def getUniProb(unigram,unigramProb, wc):
    for each in unigram:
        unigramProb[each] = unigram[each]/wc
#    print("unigram sum")
#    print(sum(unigramProb.values()))

#prob(a|b) = prob(b,a)/prob(b)
def getBiProb(unigram_vocab,bigram_vocab,bigramProb):
    for key in bigram_vocab:
            bigramProb[key] = bigram_vocab[key]/unigram_vocab[key[1]]
#    print("bigram sum")
#    print(sum(bigramProb.values()))

def getTriProb(bigram_vocab,trivocab,trigramProb):
    for key in trivocab:
        trigramProb[key] = trivocab[key]/bigram_vocab[key[:2]]
#    print("trigram sum")
#    print(sum(trigramProb.values()))

### replace words that fall under unk criteria and OOV
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

### iterator
def ngram_generator(file):
    ### read in byte
    with open(file=file, mode='rb')  as _f:
        for line in _f:
            yield line.decode('utf-8') + " <STOP>" # check here#

if __name__ == '__main__':
    main()
