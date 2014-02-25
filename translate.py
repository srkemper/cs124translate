
import itertools as it
import sys
import getopt
import os
import math
import nltk
from nltk.corpus import cess_esp
from nltk import UnigramTagger, BigramTagger, TrigramTagger, HiddenMarkovModelTagger

def loadList(file_name):
    """Loads text files as lists of lines. Used in evaluation."""
    with open(file_name) as f:
        l = [line.strip() for line in f]
    return l

def main():
	tagged_corpus = cess_esp.tagged_sents()
	size = int(len(tagged_corpus) * .9)
	training = tagged_corpus[:size]
	print "training HiddenMarkovModelTagger"
	hmm_tagger = HiddenMarkovModelTagger.train(training)
	print "finished training"


	dict_file = "./data/dictionary.txt"
	sentences_file = "./data/corpus.txt"
	dictionary_lists = loadList(dict_file)
	sentences_lists = loadList(sentences_file)
	#print sentences_lists
	#print dictionary_lists
	dictionary = dict()
	for entry in dictionary_lists:
		entry_list = entry.split()
		key = ""
		translations = []
		for idx, word in enumerate(entry_list):
			if idx== 0: 
				key = word.lower()
			else:
				translations.append(word)
		dictionary[key]=translations
	#print dictionary

	tagged_sentences = []
	for idx, sentence in enumerate(sentences_lists):
		tagged_sentences.append(hmm_tagger.tag(sentence.split()))
		print("")
		print("Sentence ",idx)
		sentence_list = sentence.split()
		print sentence_list
		translation_list = []
		for word in sentence_list:
			# print(word)
			word = word.replace('.','')
			word = word.replace(',','')
			
			word = word.lower()
			# print(word)
			trans = dictionary.get(word)
			print(trans[0])
			translation_list.append(trans[0])
		print translation_list
	print tagged_sentences





    #cp.train(clues, gold_parsed_clues)
    ##parsed_clues = cp.parseClues(clues)
    #cp.evaluate(parsed_clues, gold_parsed_clues)


if __name__ == '__main__':
    main()

