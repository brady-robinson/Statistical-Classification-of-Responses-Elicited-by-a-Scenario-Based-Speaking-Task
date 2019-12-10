from praatio import tgio
import parselmouth
import glob
import os.path
import pandas as pd
import os
import string
import statistics

# Citation: reading in .csv and analyzing soundwaves https://buildmedia.readthedocs.org/media/pdf/parselmouth/latest/parselmouth.pdf
rhythm_features = pd.read_csv("/Users/bradyrobinson/Desktop/Research_Project/rhythm_features.csv")
directory = "/Users/bradyrobinson/Desktop/Research_Project/forced_alignment_output/files_for_force_align"
file_name = ""

# Extract and output a series of rhythm features
def get_rhythm_features(row):
      output = []
      helper = row['Speech_File']
      path = "/Users/bradyrobinson/Desktop/Research_Project/forced_alignment_output/files_for_force_align/{}.TextGrid".format(helper)
      tg = tgio.openTextgrid(path)
      entryList = tg.tierDict["phones"].entryList
      entryList_2 = tg.tierDict["words"].entryList
      list_phones = []
      list_word_start_stops = []

      words = []
      time = entryList_2[-1][1]
      vowels = ['AA', 'AE', 'AH', 'AO', 'AW', 'AX', 'AXR', 'AY', 'EH', 'ER', 'EY', 'IH',
                  'IX', 'IY', 'OW', 'OY', 'UH', 'UW', 'UX']

      for phone in entryList:
        list_phones.append(phone[2])

      vocalic_int_durs = []
      consonant_int_durs = []
      current_voc_int_dur = 0
      current_cons_int_dur = 0
      next_phone = ""
      phone_list_count = 0

      for phone in entryList:

        if phone[2][0:2] in vowels:
          current_phone = phone[2][0:2]
        else:
          current_phone = phone[2]

        current_duration = phone[1] - phone[0]

        if phone_list_count < len(list_phones)-1:
          if list_phones[phone_list_count + 1][0:2] in vowels:
            next_phone = list_phones[phone_list_count + 1][0:2]
          else:
            next_phone = list_phones[phone_list_count + 1]

        if phone_list_count < len(list_phones)-1:
          if current_phone in vowels:
            continue_vowel = True
            continue_consonant = False
          else:
            continue_vowel = False
            continue_consonant = True
        else:
          continue_vowel = False
          continue_consonant = False

        while continue_vowel:
          current_voc_int_dur += current_duration
          continue_vowel = False

        while continue_consonant:
          current_cons_int_dur += current_duration
          continue_consonant = False

        if current_phone in vowels and next_phone in vowels:
          next
        elif current_phone in vowels and next_phone not in vowels:
          if phone_list_count == len(list_phones)-2:
            next
          else:
            vocalic_int_durs.append(current_voc_int_dur)
            current_voc_int_dur = 0
        elif current_phone not in vowels and next_phone not in vowels:
          next
        elif current_phone not in vowels and next_phone in vowels:
          if phone_list_count == len(list_phones)-2:
            next
          else:
            consonant_int_durs.append(current_cons_int_dur)
            current_cons_int_dur = 0

        phone_list_count += 1

      prop_voc_int = (sum(vocalic_int_durs)/(sum(vocalic_int_durs)+sum(consonant_int_durs)))
      stdev_voc_int = statistics.stdev(vocalic_int_durs)
      stdev_cons_int = statistics.stdev(consonant_int_durs)

      output.append(prop_voc_int)
      output.append(stdev_voc_int)
      output.append(stdev_cons_int)

      return output

rhythm_features['rhythm_features'] = rhythm_features.apply(get_rhythm_features, axis='columns')
rhythm_features.to_csv("rhythm_features_output.csv", index=False)
