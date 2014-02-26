import itertools as it
import sys
import getopt
import os
import math

import nltk
from HolbrookCorpus import HolbrookCorpus
from LanguageModel import LanguageModel
from nltk.corpus import brown
from nltk.corpus import cess_esp
from nltk import UnigramTagger, BigramTagger, TrigramTagger, HiddenMarkovModelTagger

#import nltk
#from nltk.corpus import cess_esp
#from nltk import UnigramTagger, BigramTagger, TrigramTagger, HiddenMarkovModelTagger
import re
from random import randint

def remove_pos_tags_and_underscores(translation_list):
	new_list = []
	for word in translation_list:
		words = word.split('/')
		new_list.append(words[0])
	final_list = []
	for word in new_list:
		words = word.split('_')
		for tok in words:
			final_list.append(tok)
	return final_list


def noun_adjective_switch(translation_list):
	switch = 1
	regex = "(.*) (\w*/NP?) (\w*)/ADJ? (.*)"
	trans = " ".join(translation_list)
	while switch!=0:
		switch =0
		EntityMatches = re.findall(regex,trans)
		if(len(EntityMatches))>0:
			switch =1
			for idx, match in enumerate(EntityMatches):
				#print trans
				trans = EntityMatches[idx][0]+" "+ EntityMatches[idx][2]+"_"+EntityMatches[idx][1]+" "+EntityMatches[idx][3]
				#print trans
				#print EntityMatches[idx][2]+"_"+EntityMatches[idx][1]
	translation_list = trans.split()
	return translation_list


def noun_of_the_noun_switch(translation_list):
	switch = 1
	regex = "(.*) (\w*/NP?) of[ _the/PREP]* (\w*)/NP? (.*)"
	trans = " ".join(translation_list)
	while switch!=0:
		switch =0
		EntityMatches = re.findall(regex,trans)
		if(len(EntityMatches))>0:
			switch =1
			for idx, match in enumerate(EntityMatches):
				#print trans
				trans = EntityMatches[idx][0]+" "+ EntityMatches[idx][2]+"_"+EntityMatches[idx][1]+" "+EntityMatches[idx][3]
				#print trans
				#print EntityMatches[idx][2]+"_"+EntityMatches[idx][1]
	translation_list = trans.split()
	return translation_list


def loadList(file_name):
    """Loads text files as lists of lines. Used in evaluation."""
    with open(file_name) as f:
        l = [line.strip() for line in f]
    return l

def testLanguageModel():
	trainingCorpus = HolbrookCorpus(brown.sents())
  	
	LM = LanguageModel(trainingCorpus)
	
	q = []
	q.append("I like to trained.")
	q.append("I like to trains.")
	q.append("I like to train.")
	q.append("I liked to training.")

	best = LM.most_likely(q)
	
	print best

	return

def main():

	testLanguageModel()

	#tagged_corpus = cess_esp.tagged_sents()
	#size = int(len(tagged_corpus) * .9)
	#training = tagged_corpus[:size]
	#print "training HiddenMarkovModelTagger"
	#hmm_tagger = HiddenMarkovModelTagger.train(training)
	#print "finished training"

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
		if sentence == "": continue
		sentence = sentence.replace('.','')
		sentence = sentence.replace(',','')
		sentence = sentence.replace(':','')
		sentence = sentence.replace('(','')
		sentence = sentence.replace(')','')
		sentence = sentence.replace('-','')
		sentence = sentence.lower()
		# tagged_sentences.append(hmm_tagger.tag(sentence.split()))

		print("")


		print("Sentence ",idx+1)

		sentence_list = sentence.split()

		full_translation_list_of_lists = []
		demo_translation_list = []

		for word in sentence_list:
			# print(word)
			word = word.replace('.','')
			word = word.replace(',','')
			word = word.replace(':','')
			word = word.replace('(','')
			word = word.replace(')','')
			word = word.replace('-','')
			word = word.lower()
			#print(word)
			if word!='':
				trans = dictionary.get(word)
#				for translation in trans:
#					if idx==0:
#						full_translation_list_of_lists.append(word)
#					else:
						#for lest in full_translation_list_of_lists:
							#lest.
		#print(translation_list)
		
		#print tagged_sentences
			demo_translation_list.append(trans[(idx+3)%len(trans)])
			
		pos_free_translation_list = remove_pos_tags_and_underscores(demo_translation_list)
		print("Initial Translation: ",' '.join(pos_free_translation_list),)
		
		translation_list= noun_adjective_switch(demo_translation_list)
		translation_list = noun_of_the_noun_switch(demo_translation_list)
		
		pos_free_translation_list = remove_pos_tags_and_underscores(demo_translation_list)
		print("Final Translation: ",' '.join(pos_free_translation_list),)

    #cp.train(clues, gold_parsed_clues)
    ##parsed_clues = cp.parseClues(clues)
    #cp.evaluate(parsed_clues, gold_parsed_clues)


if __name__ == '__main__':
    main()

