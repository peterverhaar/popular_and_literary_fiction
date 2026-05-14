
import math

from os.path import join
from nltk import word_tokenize
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
from collections import Counter
import re

def tokenise_remove_stopwords(full_text):
    words = word_tokenize(full_text)
    words = clean_wordlist(words)

    new_list= []
    for w in words:
        w = w.lower().strip()
        orig = ''
        if w.isalnum() and w not in stopwords:
            new_list.append( w )
    return new_list


def clean_wordlist(words):
    words = [word for word in words if word not in stopwords]
    words = [word for word in words if len(word.strip())>2]
    words = [re.sub(r'([….])|(\')','',word) for word in words]
    words = [word for word in words if re.search(r'\w', word)]
    return words

    

def calculate_word_frequencies(corpus):

    freq = Counter()
    for text in corpus:
        full_text = ''
        file_handler = open(text,encoding='utf-8')
        full_text = file_handler.read()
        words = word_tokenize(full_text)
        words = clean_wordlist(words)
        freq.update(words)

    return freq

        

def sorted_by_value( dict , ascending = True ):
    if ascending: 
        return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
    else:
        return {k: v for k, v in reversed( sorted(dict.items(), key=lambda item: item[1]))}



def log_likelihood( word_count1, word_count2, total1, total2 ):

    a = word_count1
    b = word_count2
    c = total1
    d = total2
 
    perc1 = (a/c)*100
    perc2 = (b/d)*100
    polarity = perc1 - perc2
 
    E1 = c*(a+b)/(c+d)
    E2 = d*(a+b)/(c+d)
    
    ln1 = math.log(a/E1)
    ln2 = math.log(b/E2)
    G2 = 2*((a* ln1) + (b* ln2))
    
    #if polarity < 0:
    #    G2 = -G2
    if a * math.log(a / E1) < 0:
        G2 = -G2

    return G2


def concordance(search_term,full_text,window):

    concordance = []

    regex = r'\b{}\b'.format( search_term )

    lines = re.split( r'\n' , full_text )

    for line in lines:

        if re.search( regex , line , re.IGNORECASE ):
            extract = ''
            position = re.search( regex , line , re.IGNORECASE ).start()
            start = position - len( search_term ) - window ;
            fragmentLength = start + 2 * window  + 2 * len( search_term )
            if fragmentLength > len( line ):
                fragmentLength = len( line )

            if start < 0:

                whiteSpace = ''
                i = 0
                while i < abs(start):
                    whiteSpace += ' '
                    i += 1
                extract = whiteSpace + line[ 0 : fragmentLength ]
            else:
                extract = line[ start : fragmentLength ]

            if re.search( '\w' , extract ) and re.search( regex , extract , re.IGNORECASE ):
                concordance.append( extract )

    return concordance

def manning_whitney():

    ll_scores = dict()

    total1 = 0
    total2 = 0

    for word1 in freq1:
        total1 += freq1[word1]
    for word2 in freq2:
        total2 += freq2[word2]

    for word in freq1:
        if word in freq2:

            ll_score = log_likelihood( freq1[word] , freq2[word] , total1 , total2 )
            ll_scores[word] = ll_score

    max = 25
    i = 0 
            
    for word in sortedByValue(ll_scores , ascending = False ):
        print( word , ll_scores[word] )
        i += 1
        if i == max: 
            break        



    from scipy.stats import mannwhitneyu

    ## make a list of all the words in both corpora
    words1 = tokenise_remove_stopwords(full_text1)
    words2 = tokenise_remove_stopwords(full_text2)

    def divide_into_chunks(words, length):

        chunks=[]
        ## chunk contains dictionaries
        # with word frequencies
        
        for i in range(0, len(words), length):
            counts = dict()
            for j in range(length):
                if i+j < len(words):
                    word = words[i+j]
                    counts[word] = counts.get(word,0)+1
            chunks.append(counts)
        return chunks


    length = 500
    chunks1 = divide_into_chunks(words1,length)
    chunks2 = divide_into_chunks(words2,length)


    # vocab is the union of terms in both sets
    all_words = dict()
        
    for chunk in chunks1:
        for word in chunk:
            all_words[word]= all_words.get(word,0) + 1
    for chunk in chunks2:
        for word in chunk:
            all_words[word]= all_words.get(word,0) + 1
        
    rho =  dict()
        
    for word in all_words:
            
        a=[]
        b=[]
            
        for chunk in chunks1:
            a.append(chunk.get(word,0))
        for chunk in chunks2:
            b.append(chunk.get(word,0))

        stat,pval=mannwhitneyu(a,b, alternative="two-sided")
        mean =len(chunks1)*len(chunks2)*0.5
        if stat <= mean:
            pval = 0 - pval
                
        rho[word]= ( pval )