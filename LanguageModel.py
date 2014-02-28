import math, collections
from operator import itemgetter
from nltk.corpus import brown
from nltk.probability import LidstoneProbDist
from nltk.model import NgramModel

class LanguageModel:

  STUPID_K = 0.4

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.trigramCounts = collections.defaultdict(lambda:0)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.lm = None
    self.train(corpus)

  def train(self, corpus):
    """Trains a language using a trigram model with stupid backoff
    to a bigram model with stupid backoff to a unigram model
    with plus one smoothing"""
    for sentence in corpus.corpus:
      for i in xrange(0, len(sentence.data)):
        token = sentence.data[i].word
        self.unigramCounts[token] += 1
        self.total += 1
        if i + 1 < len(sentence.data): 
            next = sentence.data[i+1].word
            self.bigramCounts[(token, next)] += 1
        if i + 2 < len(sentence.data):
            third = sentence.data[i+2].word
            self.trigramCounts[(token, next, third)] += 1

    train_tokens = brown.words()
    estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
    self.lm = NgramModel(3, train_tokens, True, False, estimator)


  def score(self, sentence):
    score = 0.0
    for i in xrange(2, len(sentence)):
        token = sentence[i]
        prev = sentence[i-1]
        first = sentence[i-2]
        tricount = self.trigramCounts[(first, prev, token)]
        #begin with trigram model
        if tricount > 0:
            score += self.lm.prob(token, [prev + " " + first])
            # score += math.log(tricount)
            score -= math.log(self.bigramCounts[(first, prev)])
            continue
        #back off to bigram model
        biCount = self.bigramCounts[(prev, token)]
        if biCount > 0: 
            score += math.log(biCount)
            score += math.log(self.STUPID_K)
            score -= math.log(self.unigramCounts[prev])
            continue  
        #back off to unigram model with +1 smoothing
        count = self.unigramCounts[token]
        score += math.log(self.STUPID_K) 
        score += math.log(count + 1.0)
        score -= math.log(self.total + len(self.unigramCounts))

    return score


  def n_most_likely(self, sentences, n):
    """Given a list of string sentences, returns the n most likely"""
    #m = (float("-inf"),"")
    scores = []
    for s in sentences:
        prob = self.score(s)
        scores.append((s, prob))
    scores = sorted(scores, key=itemgetter(1,0), reverse=True)
    sents = []
    for tup in scores[:n]:
        sents.append(tup[0])
    return sents

