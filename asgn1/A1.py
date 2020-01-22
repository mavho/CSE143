def main():
    # stores a mapping of tokens already seen. generates count.
    vocab = {}
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
            vocab[key] = '<unk>'

    ### prepend unks to file the name
    replace_unknowns('A1-Data/1b_benchmark.train.tokens', 'A1-Data/1b_benchmark_unks.train.tokens', vocab)
    vocab['<unk>'] += replace_unknowns('A1-Data/1b_benchmark.dev.tokens', 'A1-Data/1b_benchmark_unks.dev.tokens',vocab)
    vocab['<unk>'] += replace_unknowns('A1-Data/1b_benchmark.test.tokens', 'A1-Data/1b_benchmark_unks.test.tokens', vocab)

    print('count: ' + str(len(vocab)))


### Replace words that don't appear in training data.
def replace_unknowns(in_file, outfile, vocab):
    count = 0
    with open(file = in_file, mode='rb') as in_f, open(outfile,'wb') as outfile:
        for line in in_f:
            line = line.decode('utf-8')
            for token in line.split():
                if token not in vocab or vocab[token] == '<unk>':
                    count += 1
                    #replace replaces all tokens 
                    line = line.replace(token, '<unk>')
            outfile.write(line.encode('utf-8'))
    return count

def ngram_generator(file):
    ### read in byte
    with open(file=file, mode='rb')  as _f:
        for line in _f:
            yield line.decode('utf-8')

if __name__ == '__main__':
    main()