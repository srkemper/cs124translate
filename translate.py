import itertools as it
import sys
import getopt
import os
import math
import random

import nltk
from HolbrookCorpus import HolbrookCorpus
from LanguageModel import LanguageModel
from nltk.corpus import brown
from nltk.corpus import cess_esp
from nltk import UnigramTagger, BigramTagger, TrigramTagger#, HiddenMarkovModelTagger

import nltk
from nltk.corpus import cess_esp

import re
from random import randint

def get_our_tags_from_nltk(tag):
	tags = []
	matches = re.findall("(^nc.s...)",tag) #singular noun
	if(len(matches))>0:
		tags.append("N")
	matches = re.findall("(^nc.p...)",tag) #plural noun
	if(len(matches))>0:
		tags.append("NP")
	matches = re.findall("(^np.....)",tag) #proper noun
	if(len(matches))>0:
		tags.append("PN")
	matches = re.findall("(^a.....)",tag) #adjective
	if(len(matches))>0:
		tags.append("ADJ")
	matches = re.findall("(^r.)",tag) #adverb
	if(len(matches))>0:
		tags.append("ADV")
	matches = re.findall("(^sp...)",tag) #preposition
	if(len(matches))>0:
		tags.append("PREP")
	matches = re.findall("(^c.)",tag) #conjunction
	if(len(matches))>0:
		tags.append("CONJ")
	matches = re.findall("(^da....)",tag) #article
	if(len(matches))>0:
		tags.append("ART")
	matches = re.findall("(^di....)",tag) #article or pronoun
	if(len(matches))>0:
		tags.append("ART")
		tags.append("PRO")
	matches = re.findall("(^v.n....)",tag) #infinitive verb
	if(len(matches))>0:
		tags.append("to_V1")
	# matches = re.findall("(^v.n....)",tag) #singular noun
	# if(len(matches))>0:
	# 	tags.append("to_V1")
	matches = re.findall("(^v..i3..|v.si3..|v..s3..)",tag) #past verb
	if(len(matches))>0:
		tags.append("VP")
	matches = re.findall("(^v.p0...|v..p1..)",tag) #first person present verb
	if(len(matches))>0:
		tags.append("V1")
	matches = re.findall("(^v..p3)",tag) #third person present verb
	if(len(matches))>0:
		tags.append("V3")
	matches = re.findall("(^v..f...)",tag) #future verb
	if(len(matches))>0:
		tags.append("VF")
	matches = re.findall("(^p.......)", tag) #pronoun
	if(len(matches))>0:
		tags.append("PRO")

	matches = re.findall("(v......)", tag)
	if(len(matches) > 0 and len(tags) == 0):
		tags.append("V1")
		tags.append("V3")
		tags.append("VP")
		tags.append("VF")
		tags.append("to_V1")

	return tags

def get_translations_by_pos(word, dictionary):
	word = word.replace('.','')
	word = word.replace(',','')
	word = word.replace(':','')
	word = word.replace('(','')
	word = word.replace(')','')
	word = word.replace('-','')

	source_tag = word.split("/")[1]
	source_word = word.split("/")[0]
	#print word, source_word

	# set up new dic organized by trans
	possibilities = dictionary.get(source_word)
	pos_dict = {}
	if possibilities == None or len(possibilities) == 0:
		return []
	for possiblity in possibilities:
		#print possiblity
		tag = possiblity.split("/")[1]
		word = possiblity.split("/")[0]
		if tag not in pos_dict:
			pos_dict[tag] = []
		pos_dict[tag].append(word)

	# turn their tag into ours
	tags = get_our_tags_from_nltk(source_tag)

	results = []
	for tag in tags:
		if tag not in pos_dict:
			continue
		prefix = ""
		if tag == "to_V1":
			tag = "V1"
			prefix = "to_"
		words = pos_dict[tag]
		for word in words:
			results.append(prefix + word + "/" + tag)

	if len(results) == 0:
		for trans in dictionary.get(source_word):
			results.append(trans)

	# print "source = " + word
	# print "tags = "
	# print tags
	# print "results = "
	#print results
	return results

def remove_pos_tags_and_underscores(translation_list):
	new_list = []
	for word in translation_list:
		words = word.split('/')
		new_list.append(words[0])
	final_list = []
	for word in new_list:
		words = word.split('_')
		for tok in words:
			if tok!='':
				final_list.append(tok)
	return final_list

def append_next_words(list_of_likely_translations,index,spanish_sentence_list,dictionary):
	newList = []
	word = spanish_sentence_list[index]
		
	word = word.replace('.','')
	word = word.replace(',','')
	word = word.replace(':','')
	word = word.replace('(','')
	word = word.replace(')','')
	word = word.replace('-','')
	word = word.lower()
		
	if word!='' and index==0:
		#print index
		translations = get_translations_by_pos(word, dictionary)
		#translations.append('')

		#newList.append(translations)
		for trans in translations: 
			newList.append([trans])
		#print "NEWLIST", newList
	elif word!='':
		translations = get_translations_by_pos(word, dictionary) 
		#translations.append('')

		for trans in translations:
			#print word,trans
			copy = []
			for translation_so_far in list_of_likely_translations:
				
				copy = list(translation_so_far)
				#print copy
				copy.append(trans)
				#print copy
				#print("XXXXXXXXXXXX")
				#print translation_so_far
				newList.append(copy)
	#print index,newList
	return newList
						
def rank_by_probability_and_discard_tail(list_of_likely_translations):
	k = min(len(list_of_likely_translations), 1000)
	indices = random.sample(range(len(list_of_likely_translations)), k)
	return [list_of_likely_translations[i] for i in sorted(indices)]


def likely_translations(spanish_sentence_list,dictionary):
	list_of_likely_translations=[]
	index=0
	while index<len(spanish_sentence_list):
		list_of_likely_translations =  append_next_words(list_of_likely_translations,index,spanish_sentence_list,dictionary)
		list_of_likely_translations = rank_by_probability_and_discard_tail(list_of_likely_translations)
		index+=1
	return list_of_likely_translations

def noun_adjective_switch(translation_list):
	switch = 1
	regex = "(.*) (\w*/NP?) (\w*)/ADJ(.*)"
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
	
	q = []
	q.append("I like to train.")
	q.append("I like to training.")
	q.append("He had been liking that training.")
	q.append("That trained is so much to my liking.")
	q.append("Cats are cute?")
	q.append("Cats are cute!")

	best = LM.n_most_likely(q, 4)
	
	for tup in best:
		print tup

	return

def main():
	global LM 


	#testLanguageModel()

	#tagged_corpus = cess_esp.tagged_sents()
	#size = int(len(tagged_corpus) * .9)
	#training = tagged_corpus[:size]
	
	#print "training HiddenMarkovModelTagger"
	#hmm_tagger = HiddenMarkovModelTagger.train(training)
	#print "finished training"

	dict_file = "./data/dictionary.txt"
	sentences_file = "./data/corpus.txt"
	tagged_corpus_file = "./data/tagged_sentences.txt"
	dictionary_lists = loadList(dict_file)
	sentences_lists = loadList(sentences_file)
	tagged_sentences = loadList(tagged_corpus_file)
	
	print "training LM..."
	trainingCorpus = HolbrookCorpus(brown.sents())
	LM = LanguageModel(trainingCorpus)
	print "finished training LM"
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
	#s = 0
	#for v in dictionary.values():
	#	s += v
	#s /= len(dictionary)
	#print "avg num values = " + str(s)
	#return

	# s = 0
	# for v in dictionary.values():
	# 	s += v
	# s /= len(dictionary)
	# print "avg num values = " + str(s)
	# get_translations_by_pos("momento/ncms000", {"momento": ['time/N', 'times/NP', 'moment/N', 'moments/NP']}) #testing tag method
	# return

	
	for idx, sentence in enumerate(sentences_lists):
		if sentence == "": continue

		#tagged_sentences.append(hmm_tagger.tag(sentence.split()))
		#print("")

		# tagged_sentences.append(hmm_tagger.tag(sentence.split()))
		print("")

		print("Sentence ",idx+1)

		# sentence_list = sentence.split()
		#tagged_list = hmm_tagger.tag(sentence.split())
		tagged_sentence = tagged_sentences[idx].split()
		
		#for pair in tagged_list:
		#	tagged_sentence.append("/".join(pair))
		#print tagged_sentence
		sentence_list = tagged_sentence

		
		demo_translation_list = []
		list_of_likely_translations = []
	
		list_of_likely_translations= likely_translations(sentence_list,dictionary)
		list_of_likely_translations_as_strings = []
		for lis in list_of_likely_translations:
			lis = noun_adjective_switch(lis)
			lis = noun_of_the_noun_switch(lis)
			clean_lis = remove_pos_tags_and_underscores(lis)
			
			string = ' '.join(clean_lis)
			list_of_likely_translations_as_strings.append(string)

		best = LM.n_most_likely(list_of_likely_translations_as_strings, 10)
		
		#print list_of_likely_translations
		##if idx==0:
		#	print list_of_likely_translations
			#for lis in list_of_likely_translations:
				#print lis

		for word in sentence.split():
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
				demo_translation_list.append(trans[(idx+17)%(len(trans))-1])
				
		#print demo_translation_list
		pos_free_translation_list = remove_pos_tags_and_underscores(demo_translation_list)
		print("Initial Translation: ",' '.join(pos_free_translation_list),)
		
		
	
		print("Final Translation: ",best[0])
		print "Top Ten: ",best

  


if __name__ == '__main__':
    main()

