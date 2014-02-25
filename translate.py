
import itertools as it
import sys
import getopt
import os
import math

def noun_of_the_noun_switch(translation_list):
	switch = 1
	while switch!=0:
		for idx, word in enumerate(translation_list):
			firstN =""
			fi = -1
			of = False
			oi = -1
			the = False
			ti = -1
			secondN = ""
			si = -1
			if "/N" in word or "/NP" in word and fi==-1:
				firstN=word
				fi=idx
			if word == "of/PREP" and fi!=-1:
				of = True
				oi=idx
			if word == "of_the/PREP" and fi!=-1:
				of = True
				oi=idx
				ti=idx
				the = True
			if fi!=-1 and (word!="of/PREP" or word!="of_the/PREP"):
				firstN=""
				fi=-1
			if fi!=-1 and oi!=-1 and word=="the/PREP":
				ti=idx
				the=True
			if "/N" in word or "/NP" in word and fi==-1:



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
				key = word.lower()
			else:
				translations.append(word)
		dictionary[key]=translations
	#print dictionary

	for idx, sentence in enumerate(sentences_lists):
		print("")
		print("Sentence ",idx+1)
		sentence_list = sentence.split()
		translation_list = []
		for word in sentence_list:
			#print(word)
			word = word.replace('.','')
			word = word.replace(',','')
			word = word.replace(':','')
			word = word.replace('(','')
			word = word.replace(')','')
			word = word.replace('-','')
			word = word.lower()
			print(word)
			if word!='':
				trans = dictionary.get(word)
				translation_list.append(trans[0])
			
			translation_list = noun_of_the_noun_switch(translation_list)
			
			translation_list= noun_adjective_switch(translation_list)

		print(translation_list)





    #cp.train(clues, gold_parsed_clues)
    ##parsed_clues = cp.parseClues(clues)
    #cp.evaluate(parsed_clues, gold_parsed_clues)


if __name__ == '__main__':
    main()

