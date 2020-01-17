def main():

    # stores a mapping of tokens already seen. generates count.
    mapping = {}
    for line in ngram_generator('A1-Data/1b_benchmark.train.tokens'):
        for word in line.split(' '):
            if word in mapping:
                mapping[word] += 1
            else:
                mapping[word] = 1
    
    ### tokens that appear less than 3 times are deleted and added to 'unk
    mapping['unk'] = 0
    for key in list(mapping):
        if mapping[key] < 3:
            mapping['unk'] += mapping[key]
            del mapping[key]

    print('count: ' + str(len(mapping)))



def ngram_generator(file):
    ### read in bytes
    with open(file=file, mode='rb')  as _f:
        for line in _f:
            yield line.decode('utf-8')
if __name__ == '__main__':
    main()