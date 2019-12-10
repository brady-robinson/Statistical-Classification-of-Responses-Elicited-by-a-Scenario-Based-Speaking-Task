from praatio import tgio
import parselmouth
import glob
import os.path
import pandas as pd
import os
import string
import statistics

# Citation: reading in .csv and analyzing soundwaves https://buildmedia.readthedocs.org/media/pdf/parselmouth/latest/parselmouth.pdf
pronunciation_features = pd.read_csv("/Users/bradyrobinson/Desktop/Research_Project/fluency_features.csv")
directory = "/Users/bradyrobinson/Desktop/Research_Project/forced_alignment_output/files_for_force_align"
file_name = ""

# Extract and output a series of pronunciation related features
def get_pronunciation_features(row):
      output = []
      helper = row['Speech_File']
      path = "/Users/bradyrobinson/Desktop/Research_Project/forced_alignment_output/files_for_force_align/{}.TextGrid".format(helper)
      tg = tgio.openTextgrid(path)
      entryList = tg.tierDict["phones"].entryList
      entryList_2 = tg.tierDict["words"].entryList

      words = []
      time = entryList_2[-1][1]
      letters = []
      letters_flat = []
      vowels = ['AA', 'AE', 'AH', 'AO', 'AW', 'AX', 'AXR', 'AY', 'EH', 'ER', 'EY', 'IH',
                  'IX', 'IY', 'OW', 'OY', 'UH', 'UW', 'UX']

      for word in entryList_2:
        words.append(word[2])

      for word in words:
        letters.append(list(word))

      for sub_array in letters:
        for letter in sub_array:
          letters_flat.append(letter)

      num_letters = len(letters_flat)
      speaking_rate = num_letters/time
      output.append(speaking_rate)

      tot_vowel_dur = 0
      num_vowels = 0
      avg_vowel_dur = 0
      stdev_vowel_dur = 0
      for phone in entryList:
        current_duration = phone[1] - phone[0]
        if phone[2][0:2] in vowels:
          tot_vowel_dur += current_duration
          num_vowels += 1

      output.append(num_vowels)

      avgvoweldur = tot_vowel_dur/num_vowels

      output.append(avgvoweldur)

      return output

pronunciation_features['pronunciation_features'] = pronunciation_features.apply(get_pronunciation_features, axis='columns')
pronunciation_features.to_csv("pronunciation_features_output.csv", index=False)
