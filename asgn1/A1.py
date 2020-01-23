import math, re
def main():
    # stores a mapping of tokens already seen. generates count.
    vocab = {}
    # unigramProb stores key as word and value as prob of word/totalWord
    word_count = initialize(vocab)
    cal_perplexity(vocab,word_count)

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
    replace_unknowns('A1-Data/1b_benchmark.train.tokens', 'A1-Data/1b_benchmark_unks.train.tokens', vocab)
    vocab['<unk>'] += replace_unknowns('A1-Data/1b_benchmark.dev.tokens', 'A1-Data/1b_benchmark_unks.dev.tokens', vocab)
    vocab['<unk>'] += replace_unknowns('A1-Data/1b_benchmark.test.tokens', 'A1-Data/1b_benchmark_unks.test.tokens', vocab)

    return word_count


def cal_perplexity(vocab, wc):
    fileset = ['A1-Data/1b_benchmark_unks.train.tokens','A1-Data/1b_benchmark_unks.dev.tokens','A1-Data/1b_benchmark_unks.test.tokens']

    unigramProb = {}
    getProb(vocab,unigramProb, wc)
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

### fill the unigramProb with probabilities based on the training set
def getProb(unigram, unigramProb, wc):
    print("# of stops")
    print(unigram["<STOP>"])
    print("len of unigram")
    print(len(unigram))
    for each in unigram:
        #unigramProb[each] = unigram[each]/len(unigram)
        unigramProb[each] = unigram[each]/wc
    

# return prob of 1 word / all words
# store the prob of each word(key) : word / total words(value)
### Replace words that don't appear in training data.

def replace_unknowns(in_file, outfile, vocab):
    count = 0
    with open(file = in_file, mode='rb') as in_f, open(outfile,'wb') as outfile:
        for line in in_f:
            line = line.decode('utf-8')
            fline = ''
            for token in line.split():
                if token not in vocab:
                    token = '<unk>'
                    count += 1
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