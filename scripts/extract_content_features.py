from praatio import tgio
import parselmouth
import glob
import os.path
import pandas as pd
import os
import string
import statistics
import nltk
import re
from nltk.corpus import stopwords 
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


# Function allows for synonyms to be taken from WordNet
def get_synonyms(lemma):
    # Part 1
    possible_synonyms_1 = []
    for lem in wn.lemmas(lemma):
        for lexeme in lem.synset().lemmas():
            possible_synonyms_1.append(lexeme.name())

    possible_synonyms_2 = []
    for element in possible_synonyms_1:
        if possible_synonyms_2.count(element) == 0 and element != lemma:
            possible_synonyms_2.append(element)

    #citation: https://stackoverflow.com/questions/52638661/how-to-modify-strings-in-a-list
    possible_synonyms = []
    for element in possible_synonyms_2:
        possible_synonyms.append(element.replace("_", " "))

    return possible_synonyms

# Function allows for hypernyms to be taken from Wordnet
def get_hypernyms(word):
  hyps = []
  lems = []
  output_hyps = []
  synsets = wn.synsets(word)
  for syn in synsets:
    hyps.append(syn.hypernyms())

  for sub_list in hyps:
    for syn in sub_list:
      lems.append(syn.lemmas())

  for sub_list in lems:
    for element in sub_list:
      output_hyps.append(element.name())

  return output_hyps

# Function allows for hyponyms to be taken from WordnNet
def get_hyponyms(word):
  hyps = []
  lems = []
  output_hyps = []
  synsets = wn.synsets(word)
  for syn in synsets:
    hyps.append(syn.hyponyms())

  for sub_list in hyps:
    for syn in sub_list:
      lems.append(syn.lemmas())

  for sub_list in lems:
    for element in sub_list:
      output_hyps.append(element.name())

  return output_hyps

# Citation: reading in .csv and analyzing soundwaves https://buildmedia.readthedocs.org/media/pdf/parselmouth/latest/parselmouth.pdf
content_features = pd.read_csv("/Users/bradyrobinson/Desktop/Research_Project/content_features.csv")
stop_words = set(stopwords.words('english'))

# Import custom corpus, remove stop words and punctuation, and then create a series of different corpora for the different features
all_corp = open("/Users/bradyrobinson/Desktop/Research_Project/content_corpus.txt", "r+")
all_corp_text = all_corp.read()
all_corp_wo_punct = all_corp_text.translate(str.maketrans('', '', string.punctuation))
all_corp_wo_punct_lower = all_corp_wo_punct.lower()
all_corp_toks = word_tokenize(all_corp_wo_punct_lower)

all_corp_filtered = []
for w in all_corp_toks: 
  if w not in stop_words: 
    all_corp_filtered.append(w)

all_corp_filtered_lems = []
for word in all_corp_filtered:
  all_corp_filtered_lems.append(lemmatizer.lemmatize(word))

all_corp_filtered_lems_syns = []

for lem in all_corp_filtered_lems:
  all_corp_filtered_lems_syns.append(get_synonyms(lem))

flat_all_corp_filtered_lems_w_syns = []
for sub_list in all_corp_filtered_lems_syns:
  for element in sub_list:
    flat_all_corp_filtered_lems_w_syns.append(element)

for element in all_corp_filtered_lems:
  flat_all_corp_filtered_lems_w_syns.append(element)

all_corp_filtered_lems_hyps = []
for element in all_corp_filtered_lems:
  all_corp_filtered_lems_hyps.append(get_hypernyms(element))

flat_all_corp_filtered_lems_w_hyps = []
for sub_list in all_corp_filtered_lems_hyps:
  for element in sub_list:
    flat_all_corp_filtered_lems_w_hyps.append(element)

for element in all_corp_filtered_lems:
  flat_all_corp_filtered_lems_w_hyps.append(element)

all_corp_filtered_lems_hypos = []
for element in all_corp_filtered_lems:
  all_corp_filtered_lems_hypos.append(get_hyponyms(element))

flat_all_corp_filtered_lems_w_hypos = []
for sub_list in all_corp_filtered_lems_hypos:
  for element in sub_list:
    flat_all_corp_filtered_lems_w_hypos.append(element)

for element in all_corp_filtered_lems:
  flat_all_corp_filtered_lems_w_hypos.append(element)

all_lems_syns_hyps_hypos = []
all_lems_syns_hyps_hypos = all_lems_syns_hyps_hypos + all_corp_filtered_lems + flat_all_corp_filtered_lems_w_syns + flat_all_corp_filtered_lems_w_hyps + flat_all_corp_filtered_lems_w_hypos

all_lems_syns_hyps_hypos
all_corp_filtered_lems
flat_all_corp_filtered_lems_w_syns
flat_all_corp_filtered_lems_w_hyps
flat_all_corp_filtered_lems_w_hypos


# Calculate the overlap values for each spoken response
def get_content_features(row):
      output = []
      helper = row['Text_File']
      path = "/Users/bradyrobinson/Desktop/Research_Project/txt_hand_transcribed/{}.txt".format(helper)
      file = open(path, "r+")
      text = file.read()
      text_wo_punct = text.translate(str.maketrans('', '', string.punctuation))
      text_wo_punct_lower = text_wo_punct.lower()
      tags = []

      word_tokens = word_tokenize(text_wo_punct_lower)

      filtered_sentence = []
  
      for w in word_tokens: 
        if w not in stop_words: 
          filtered_sentence.append(w)

      filtered_sentence_lems = []

      for word in filtered_sentence:
        filtered_sentence_lems.append(lemmatizer.lemmatize(word))

      length_current_text = len(filtered_sentence_lems)
      count_all_lems_syns_hyps_hypos = 0
      count_all_corp_filtered_lems = 0
      count_flat_all_corp_filtered_lems_w_syns = 0
      count_flat_all_corp_filtered_lems_w_hyps = 0
      count_flat_all_corp_filtered_lems_w_hypos = 0

      for word in filtered_sentence_lems:
        if word in all_lems_syns_hyps_hypos:
          count_all_lems_syns_hyps_hypos += 1
        if word in all_corp_filtered_lems:
          count_all_corp_filtered_lems += 1
        if word in flat_all_corp_filtered_lems_w_syns:
          count_flat_all_corp_filtered_lems_w_syns += 1
        if word in flat_all_corp_filtered_lems_w_hyps:
          count_flat_all_corp_filtered_lems_w_hyps += 1
        if word in flat_all_corp_filtered_lems_w_hypos:
          count_flat_all_corp_filtered_lems_w_hypos += 1
      
      lemmas = count_all_corp_filtered_lems / length_current_text
      cov_wn_syns = count_flat_all_corp_filtered_lems_w_syns / length_current_text
      cov_wn_hyper = count_flat_all_corp_filtered_lems_w_hyps / length_current_text
      cov_wn_hypo = count_flat_all_corp_filtered_lems_w_hypos / length_current_text
      cov_all = count_all_lems_syns_hyps_hypos / length_current_text

      presence_adj = 0
      num_adj = 0
      presence_adv = 0
      num_adv = 0

      tags = nltk.pos_tag(filtered_sentence_lems)
      for tag in tags:
        if tag[1] == 'JJ':
          presence_adj += 1
          num_adj += 1
        if tag[1] == 'JJR':
          presence_adj += 1
          num_adj += 1
        if tag[1] == 'JJS':
          presence_adj += 1
          num_adj += 1
        if tag[1] == 'RB':
          presence_adv += 1
          num_adv += 1
        if tag[1] == 'RBR':
          presence_adv += 1
          num_adv += 1
        if tag[1] == 'RBS':
          presence_adv += 1
          num_adv += 1
        if tag[1] == 'WRB':
          presence_adv += 1
          num_adv += 1

      if presence_adj > 0:
        presence_adj = 1

      if presence_adv > 0:
        presence_adv = 1

      keywords = ["good exchange rate", "bilingual tour guide", "easy to travel by bike", 
                  "floating market", "wet summer weather", "changes to tour times",
                  "slow boat rides", "eat traditional food", "swim in the dead sea",
                  "monuments of petra", "roman ruins in jerash", "expensive", 
                  "very hot and dry", "not enough time"]

      keywords_sub = ["good", "echange", "rate", "bilingual", "tour", "guide", "easy", "travel",
                      "bike", "floating", "market", "wet", "summer", "weather", "changes",
                      "tour", "times", "slow", "boat", "rides", "eat", "traditional", "food",
                      "swim", "dead", "sea", "monuments", "petra", "roman", "ruins", "jerash",
                      "expensive", "very", "hot", "dry", "enough", "time"]


      list_keyword_matches = ""
      for phrase in keywords:
        list_keyword_matches = re.findall(phrase, text_wo_punct_lower)

      num_keywords = len(list_keyword_matches)
      percent_keywords = (num_keywords / len(keywords))*100

      num_sub_keywords = 0
      for word in keywords_sub:
        if word in filtered_sentence:
          num_sub_keywords += 1

      percent_sub_keywords = (num_sub_keywords / len(keywords_sub))*100

      output.append(lemmas)
      output.append(cov_wn_syns)
      output.append(cov_wn_hyper)
      output.append(cov_wn_hypo)
      output.append(cov_all)
      output.append(presence_adj)
      output.append(num_adj)
      output.append(presence_adv)
      output.append(num_adv)
      output.append(num_keywords)
      output.append(percent_keywords)
      output.append(num_sub_keywords)
      output.append(percent_sub_keywords)

      return output

content_features['content_features'] = content_features.apply(get_content_features, axis='columns')
content_features.to_csv("content_features_output.csv", index=False)
