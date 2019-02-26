""" this is a thing """
import sys
import os
import re
import math
from porter2stemmer import Porter2Stemmer

# pylint: disable-msg=C0103
# pylint: disable-msg = C0330

contraction_dict = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it'd": "it had",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there had",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'alls": "you alls",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had",
    "you'd've": "you would have",
    "you'll": "you you will",
    "you'll've": "you you will have",
    "you're": "you are",
    "you've": "you have"
}


def removeSGML(in_string):
    """This is a doc baby"""
    out_string = re.sub(r'<.*?>', '', in_string)
    return out_string

def tokenizeText(in_string):
    """this takes in a string and returns a list of tokens"""
    tokenizedList = []
    in_string = in_string.lower()
    for word in in_string.split():
        # check to see if it's a contraction
        if word in contraction_dict:
            uncontracted_word = contraction_dict[word]
            for word1 in uncontracted_word.split():
                tokenizedList.append(word1)
            continue
        # check to see if the word is possessive
        elif re.match(r'[a-z]*\'s[.?,!]?', word) != None:
            tokenizedList.append(word[:-2])
            tokenizedList.append('\'s')
            continue
        # check to see if the word is a date
        elif re.match(r'[0-9]*\/[0-9]*\/[0-9]*', word) != None:
            tokenizedList.append(word)
        # check to see if the word is an acronym
        elif word.count('.') > 1:
            continue
        # check for punctuation
        elif re.match(r'[a-z]*[.!,?"]', word) != None:
            tokenizedList.append(word[:-1])
            tokenizedList.append(word[-1:])
        # check to see if it's numbers
        elif re.match(r'^[0-9]{1,2}([,.][0-9]{1,2})?$', word) != None:
            tokenizedList.append(word)
        # all other words get tokenized as-is
        else:
            tokenizedList.append(word)
    for word in tokenizedList:
        word = re.sub(r'[^a-zA-Z0-9]+', '', word)

    finalList = []
    for word in tokenizedList:
        if word not in [',', '.', '"', "'s", '\xe2\x80\x94', '\x9d']:
            finalList.append(word)
    return finalList

def removeSpaces(input_list):
    """removes all empty characters"""
    return [value for value in input_list if value != '']


def removeStopwords(input_list):
    """takes in a list of words, removes the stopwords, returns another list"""
    stopwords = open("stopwords", "r")
    stopword_string = stopwords.read()
    stopwords.close()
    stopword_list = stopword_string.split()
    stopword_list += ['also', 'county', 'about']
    out_list = []
    for word in input_list:
        if word in stopword_list:
            continue
        else:
            out_list.append(word)
    return out_list

def stemWords(input_list):
    """takes in a list of word and stems it"""
    stemmer = Porter2Stemmer()
    output_list = []
    for word in input_list:
        word = stemmer.stem(word)
        output_list.append(word)
    return output_list

def trainNaiveBayes(file_list):
    """trains a naive bayes algo"""
    document_dict = {}
    vocabulary = {}
    # track number of files of each
    b_count = 0.0
    w_count = 0.0
    h_count = 0.0
    # track total number of words of each
    total_words_b = 0.0
    total_words_h = 0.0
    total_words_w = 0.0
    output_words = {}
    # read in file
    for filename in file_list:
        in_file = open(filename, 'r')
        text = in_file.read()
        text = removeSGML(text)
        text = tokenizeText(text)
        text = removeStopwords(text)
        text = removeSpaces(text)
        # text = stemWords(text)
        # See what base truth is to add to count
        if filename.find('black') != -1:
            b_count += 1.0
            document_dict[filename] = {"race": "black"}
        elif filename.find('hispanic') != -1:
            h_count += 1.0
            document_dict[filename] = {"race": "hispanic"}
        else:
            w_count += 1.0
            document_dict[filename] = {"race": "white"}
        for word in text:
            if word not in vocabulary:
                vocabulary[word] = {'black': 0.0, 'white': 0.0, 'hispanic': 0.0}
            if document_dict[filename]['race'] == 'black':
                vocabulary[word]['black'] += 1.0
                total_words_b += 1.0
            elif document_dict[filename]['race'] == 'hispanic':
                vocabulary[word]['hispanic'] += 1.0
                total_words_h += 1.0
            else:
                vocabulary[word]['white'] += 1.0
                total_words_w += 1.0
    for word in vocabulary:
        output_words[word] = {}
        output_words[word]['black'] = (vocabulary[word]['black']
                                        + 1.0) / (total_words_b + float(len(vocabulary)))
        output_words[word]['white'] = (vocabulary[word]['white']
                                        + 1.0) / (total_words_w + float(len(vocabulary)))
        output_words[word]['hispanic'] = (vocabulary[word]['hispanic']
                                        + 1.0) / (total_words_h + float(len(vocabulary)))

    output_class = {'b_prob': (b_count / (b_count + h_count + w_count)),
                    'h_prob': (h_count / (b_count + h_count + w_count)),
                    'w_prob': (w_count / (b_count + h_count + w_count))}

    return(output_words, output_class, len(vocabulary))


def testNaiveBayes(filename, class_dict, word_dict):
    """tests bayes"""
    in_file = open(filename, 'r')
    text = in_file.read()
    in_file.close()
    text = removeSGML(text)
    text = tokenizeText(text)
    text = removeStopwords(text)
    text = removeSpaces(text)
    # text = stemWords(text)
    b_score = 0.0
    h_score = 0.0
    w_score = 0.0
    for word in text:
        if word in word_dict:
            df = len(INVERTED_INDEX[word]['docs'])
            tf_idf = INVERTED_INDEX[word]['count'] * math.log(CORPUS_SIZE / df, 2)
            if USE_TFIDF is False:
                tf_idf = 1

            b_score += math.log10(word_dict[word]['black']) * tf_idf
            h_score += math.log10(word_dict[word]['hispanic']) * tf_idf
            w_score += math.log10(word_dict[word]['white']) * tf_idf

    b_score *= class_dict['b_prob']
    h_score *= class_dict['h_prob']
    w_score *= class_dict['w_prob']
    # print h_score, b_score, w_score
    if b_score > w_score:
        return 'black'
    elif USE_HISPANIC is True and h_score > b_score and h_score > w_score:
        return 'hispanic'
    return 'white'



def createInvertedIndex(filenames):
    global INVERTED_INDEX
    INVERTED_INDEX = {}
    
    for filename in filenames:
        in_file = open(filename, 'r')
        text = in_file.read()
        in_file.close()
        text = removeSGML(text)
        text = tokenizeText(text)
        text = removeStopwords(text)
        text = removeSpaces(text)

        for word in text:
            if word not in INVERTED_INDEX:
                INVERTED_INDEX[word] = {'count': 0, 'docs': set()} 

            INVERTED_INDEX[word]['count'] += 1
            INVERTED_INDEX[word]['docs'].add(filename)
    

def printTopWords(wordProbabilities, category, N):
    pairs = []
    for word in wordProbabilities:
        p = wordProbabilities[word][category]
        pairs.append((word, p))

    sortedByProbability = sorted(pairs, key=lambda tup: tup[1], reverse=True)
    topN = sortedByProbability[:N]
    
    print 'Top', N, 'for', category, 'articles'
    for x in topN:
        print x[0], x[1]
    print ''

    return topN


def topWordsVennDiagram(wordProbabilities):
    topBlackWords = printTopWords(wordProbabilities, 'black', 20)
    topWhiteWords = printTopWords(wordProbabilities, 'white', 20)
    #printTopWords(word_probs, 'hispanic', 10)
    
    topBlackWords = set([word for word, prob in topBlackWords])
    topWhiteWords = set([word for word, prob in topWhiteWords])
    
    wordsInBoth = topBlackWords.intersection(topWhiteWords)
    whiteExclusive = topWhiteWords.difference(topBlackWords)
    blackExclusive = topBlackWords.difference(topWhiteWords)

    print 'White only words'
    print whiteExclusive
    print '\nBlack only words'
    print blackExclusive
    print '\nWhite and Black words'
    print wordsInBoth


INVERTED_INDEX = {}
CORPUS_SIZE = 0
USE_TFIDF = True
USE_HISPANIC = False

def main(directory=None, useTfIdf=False, useHispanic=False):
    """main function"""
    global CORPUS_SIZE
    global USE_TFIDF
    global USE_HISPANIC

    if directory is None:
	directory = sys.argv[1]

    USE_TFIDF = useTfIdf
    USE_HISPANIC = useHispanic

    files = os.listdir(directory)
    if useHispanic == False:
        files = [f for f in files if 'hispanic' not in f]
    gramp_file_list = sorted(files)
    CORPUS_SIZE = len(gramp_file_list)
    perm_file_list = []
    accuracy = 0.0

    for item in gramp_file_list:
        perm_file_list.append(directory + item)

    # get highest conditional probablity words
    word_probs, classes, numWords = trainNaiveBayes(perm_file_list)
    topWordsVennDiagram(word_probs)

    createInvertedIndex(perm_file_list)

    out_file_name = 'output_' + directory.replace('/', '_')
    if USE_TFIDF is True:
        out_file_name += '_tfidf'
    if useHispanic is True:
        out_file_name += '_useHispanic'
    print 'Writing to', out_file_name
    out_file = open(out_file_name, 'w')
    for index, filename in enumerate(perm_file_list):
        temp_list = perm_file_list[:]
        temp_list.pop(index)
        temp_tup = trainNaiveBayes(temp_list)
        # for word in temp_tup[0]:
        #     word_difference_list.append((word, abs(temp_tup[0][word]['black'] - temp_tup[0][word]['white'])))
        # print sorted(word_difference_list, key=lambda tup: tup[1], reverse=True)[:20]
        # trash = raw_input()
        output = testNaiveBayes(filename, temp_tup[1], temp_tup[0])
        print filename, output
        out_file.write(filename + ' ' + output +'\n')
        if filename.find('black') != -1:
            if output == 'black':
                accuracy += 1.0
        elif filename.find('hispanic') != -1:
            if output == 'hispanic':
                accuracy += 1.0
        else:
            if output == 'white':
                accuracy += 1.0
    out_file.write('accuracy:' + str(accuracy/float(len(perm_file_list))))
    print accuracy/float(len(perm_file_list))
    out_file.close()


if __name__ == '__main__':
    main()
