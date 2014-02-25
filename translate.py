import itertools as it
import sys
import getopt
import os
import math

def loadList(file_name):
    """Loads text files as lists of lines. Used in evaluation."""
    with open(file_name) as f:
        l = [line.strip() for line in f]
    return l

def main():
	
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
				key = word
			else:
				translations.append(word)
		dictionary[key]=translations
	#print dictionary

	for idx, sentence in enumerate(sentences_lists):
		if sentence == "": continue
		print("")
		print("Sentence ",idx)
		print sentence
		sentence_list = sentence.split()
		translation_list = []
		for word in sentence_list:
			#print(word)
			word = word.replace('.','')
			word = word.replace(',','')
			
			word = word.lower()
			#print(word)
			trans = dictionary.get(word)
			print trans
			translation_list.append(trans[0])
		print translation_list





    #cp.train(clues, gold_parsed_clues)
    ##parsed_clues = cp.parseClues(clues)
    #cp.evaluate(parsed_clues, gold_parsed_clues)


if __name__ == '__main__':
    main()

