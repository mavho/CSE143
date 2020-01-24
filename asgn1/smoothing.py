### don't use this funciton yet.
def smoothing(**kwargs):
    for key,val in kwargs.items():
        print("{} {}".format(key,val))
        
    fileset = ['A1-Data/1b_benchmark_unks.train.tokens','A1-Data/1b_benchmark_unks.dev.tokens','A1-Data/1b_benchmark_unks.test.tokens']
    ### calculating bi grams
    for file in fileset:
        print("fileset: " + file)
        L = 0 
        word_count = 0
        ZERO_FLAG = False
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
                if bigram in bigramProb:
                    prob = bigramProb[bigram]
                    temp += (-1 * math.log(prob, 2))
                else:
                    ZERO_FLAG = True
                    break
            L += temp 
        if ZERO_FLAG:
            print('Zero Encountered: 0')
        else:
            print(math.pow(2, L/word_count))
        

    print("Smoothing function")

def file_generator(file):
    with open(file = file, mode = 'rb') as _f:
        for line in _f:
            yield line.decode('utf-8')