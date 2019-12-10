import os
import string

directory = "/Users/bradyrobinson/Desktop/Research_Project/txt_hand_transcribed"

# Make each transcribed all cap and output new .txt files for use in the force alignment
for text_file in os.listdir(directory):
  file = open("/Users/bradyrobinson/Desktop/Research_Project/txt_hand_transcribed/{}".format(text_file), "r+")
  new_file_name = text_file[0:len(text_file)-4]

  new_file = open("/Users/bradyrobinson/Desktop/Research_Project/all_cap_text/{}.lab".format(new_file_name), "w+")
  text = file.read()
  text_wo_punct = text.translate(str.maketrans('', '', string.punctuation))
  upper_text = text_wo_punct.upper()
  new_file.write(upper_text)