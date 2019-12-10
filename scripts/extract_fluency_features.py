from praatio import tgio
import parselmouth
import glob
import os.path
import pandas as pd
import os
import string
import statistics

# Citation: reading in .csv and analyzing soundwaves https://buildmedia.readthedocs.org/media/pdf/parselmouth/latest/parselmouth.pdf
fluency_features = pd.read_csv("/Users/bradyrobinson/Desktop/Research_Project/fluency_features.csv")
directory = "/Users/bradyrobinson/Desktop/Research_Project/forced_alignment_output/files_for_force_align"
file_name = ""

# Extract and output a series of fluency related features
def get_fluency_features(row):
      output = []
      helper = row['Speech_File']
      path = "/Users/bradyrobinson/Desktop/Research_Project/forced_alignment_output/files_for_force_align/{}.TextGrid".format(helper)
      tg = tgio.openTextgrid(path)
      entryList = tg.tierDict["phones"].entryList
      entryList_2 = tg.tierDict["words"].entryList

      count_of_sp = 0
      duration_all_sp = 0
      lengths_all_sp = []

      num_long_p = 0
      dur_long_p = 0
      lengths_all_lp = []

      count_fp = 0
      dur_fp = 0
      lengths_all_fp = []

      for element in entryList:
          current_duration = element[1] - element[0]
          if element[2] == "sp":
            count_of_sp += 1
            duration_all_sp += current_duration
            lengths_all_sp.append(current_duration)
          if element[2] == "sp" and current_duration >= 0.5:
            num_long_p += 1
            dur_long_p += current_duration
            lengths_all_lp.append(current_duration)

      for element_2 in entryList_2:
          current_duration_2 = element_2[1] - element_2[0]
          if element_2[2] == "um" or element_2[2] == "uh":
            count_fp += 1
            dur_fp += current_duration
            lengths_all_fp.append(current_duration_2)

      stdevsil = statistics.stdev(lengths_all_sp)
      meansil = statistics.mean(lengths_all_sp)
      numsil = len(lengths_all_sp)
      totdursil = duration_all_sp

      stdevlongp = statistics.stdev(lengths_all_lp)
      meanlongp = statistics.mean(lengths_all_lp)
      numlongp = len(lengths_all_lp)
      totdurlongp = dur_long_p

      numfp = count_fp
      if len(lengths_all_fp) == 0:
        meandurfp = 0
      else:
        meandurfp = statistics.mean(lengths_all_fp)

      if len(lengths_all_fp) < 2:
        print(lengths_all_fp)
        stdevfp = 0
      else:
        stdevfp = statistics.stdev(lengths_all_fp)

      totdurfp = dur_fp

      output.append(numsil)
      output.append(meansil)
      output.append(stdevsil)
      output.append(totdursil)
      output.append(numlongp)
      output.append(meanlongp)
      output.append(stdevlongp)
      output.append(totdurlongp)
      output.append(numfp)
      output.append(meandurfp)
      output.append(stdevfp)
      output.append(totdurfp)

      return output

fluency_features['fluency_features'] = fluency_features.apply(get_fluency_features, axis='columns')
fluency_features.to_csv("fluency_features_output.csv", index=False)
