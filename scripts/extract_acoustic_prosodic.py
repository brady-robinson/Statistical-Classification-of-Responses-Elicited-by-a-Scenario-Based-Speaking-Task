import parselmouth
import glob
import os.path
import pandas as pd

# Citation: reading in .csv and analyzing soundwaves https://buildmedia.readthedocs.org/media/pdf/parselmouth/latest/parselmouth.pdf
msp_data = pd.read_csv("/Users/bradyrobinson/Desktop/Research_Project/acoustic_prosodic_features.csv")

def get_min_pitch(row):
    speech_file = row['Speech_File']
    filepath = "/Users/bradyrobinson/Desktop/Research_Project/trimmed_samples/{}.wav".format(speech_file)    
    sound = parselmouth.Sound(filepath)
    pitch = parselmouth.praat.call(sound, "To Pitch...", 0.0, 75.0, 600.0)
    min_pitch = parselmouth.praat.call(pitch, "Get minimum", 0.0, 0.0, "Hertz", "None")

    return min_pitch

def get_max_pitch(row):
    speech_file = row['Speech_File']
    filepath = "/Users/bradyrobinson/Desktop/Research_Project/trimmed_samples/{}.wav".format(speech_file)
    sound = parselmouth.Sound(filepath)
    pitch = parselmouth.praat.call(sound, "To Pitch...", 0.0, 75.0, 600.0)
    max_pitch = parselmouth.praat.call(pitch, "Get maximum", 0.0, 0.0, "Hertz", "None")
    return max_pitch

def get_mean_pitch(row):
    speech_file = row['Speech_File']
    filepath = "/Users/bradyrobinson/Desktop/Research_Project/trimmed_samples/{}.wav".format(speech_file)
    sound = parselmouth.Sound(filepath)
    pitch = parselmouth.praat.call(sound, "To Pitch...", 0.0, 75.0, 600.0)
    mean_pitch = parselmouth.praat.call(pitch, "Get mean", 0.0, 0.0, "Hertz")
    return mean_pitch

def get_sd_pitch(row):
    speech_file = row['Speech_File']
    filepath = "/Users/bradyrobinson/Desktop/Research_Project/trimmed_samples/{}.wav".format(speech_file)
    sound = parselmouth.Sound(filepath)
    pitch = parselmouth.praat.call(sound, "To Pitch...", 0.0, 75.0, 600.0)
    sd_pitch = parselmouth.praat.call(pitch, "Get standard deviation", 0.0, 0.0, "Hertz")
    return sd_pitch

def get_min_intensity(row):
    speech_file = row['Speech_File']
    filepath = "/Users/bradyrobinson/Desktop/Research_Project/trimmed_samples/{}.wav".format(speech_file)
    sound = parselmouth.Sound(filepath)
    intensity = sound.to_intensity()
    min_intensity = parselmouth.praat.call(intensity, "Get minimum", 0.0, 0.0, "None")
    return min_intensity

def get_max_intensity(row):
    speech_file = row['Speech_File']
    filepath = "/Users/bradyrobinson/Desktop/Research_Project/trimmed_samples/{}.wav".format(speech_file)
    sound = parselmouth.Sound(filepath)
    intensity = sound.to_intensity()
    max_intensity = parselmouth.praat.call(intensity, "Get maximum", 0.0, 0.0, "None")
    return max_intensity

def get_mean_intensity(row):
    speech_file = row['Speech_File']
    filepath = "/Users/bradyrobinson/Desktop/Research_Project/trimmed_samples/{}.wav".format(speech_file)
    sound = parselmouth.Sound(filepath)
    intensity = sound.to_intensity()
    mean_intensity = parselmouth.praat.call(intensity, "Get mean", 0.0, 0.0)
    return mean_intensity

def get_sd_intensity(row):
    speech_file = row['Speech_File']
    filepath = "/Users/bradyrobinson/Desktop/Research_Project/trimmed_samples/{}.wav".format(speech_file)
    sound = parselmouth.Sound(filepath)
    intensity = sound.to_intensity()
    sd_intensity = parselmouth.praat.call(intensity, "Get standard deviation", 0.0, 0.0)
    return sd_intensity

def get_jitter(row):
    speech_file = row['Speech_File']
    filepath = "/Users/bradyrobinson/Desktop/Research_Project/trimmed_samples/{}.wav".format(speech_file)
    sound = parselmouth.Sound(filepath)
    pitch = sound.to_pitch()
    point_process = parselmouth.praat.call(pitch, "To PointProcess")
    jitter_local = parselmouth.praat.call(point_process, "Get jitter (local)", 0.0, 0.0, 0.0001, 0.02, 1.3)
    return jitter_local

# Citation: shimmer extraction https://stackoverflow.com/questions/54707734/parselmouth-batch-full-voice-report
def get_shimmer(row):
    speech_file = row['Speech_File']
    filepath = "/Users/bradyrobinson/Desktop/Research_Project/trimmed_samples/{}.wav".format(speech_file)
    sound = parselmouth.Sound(filepath)
    pitch = sound.to_pitch()
    pulses = parselmouth.praat.call([sound, pitch], "To PointProcess (cc)")
    shimmer_local = parselmouth.praat.call([sound, pulses], "Get shimmer (local)", 0.0, 0.0, 0.0001, 0.02, 1.3, 1.6)
    return shimmer_local

# Citation: HNR https://buildmedia.readthedocs.org/media/pdf/parselmouth/latest/parselmouth.pdf
def get_hnr(row):
    speech_file = row['Speech_File']
    filepath = "/Users/bradyrobinson/Desktop/Research_Project/trimmed_samples/{}.wav".format(speech_file)
    sound = parselmouth.Sound(filepath)
    harmonicity = sound.to_harmonicity()
    harmonicity_cc = parselmouth.praat.call(sound, "To Harmonicity (cc)...", 0.01, 75.0, 0.1, 1.0)
    hnr = harmonicity_cc.values[harmonicity.values != -200].mean()
    return hnr

# Citation: outputting to .csv https://buildmedia.readthedocs.org/media/pdf/parselmouth/latest/parselmouth.pdf
msp_data['Min_Pitch'] = msp_data.apply(get_min_pitch, axis='columns')
msp_data['Max_Pitch'] = msp_data.apply(get_max_pitch, axis='columns')
msp_data['Mean_Pitch'] = msp_data.apply(get_mean_pitch, axis='columns')
msp_data['Sd_Pitch'] = msp_data.apply(get_sd_pitch, axis='columns')
msp_data['Min_Inensity'] = msp_data.apply(get_min_intensity, axis='columns')
msp_data['Max_Inensity'] = msp_data.apply(get_max_intensity, axis='columns')
msp_data['Mean_Inensity'] = msp_data.apply(get_mean_intensity, axis='columns')
msp_data['Sd_Inensity'] = msp_data.apply(get_sd_intensity, axis='columns')
msp_data['Jitter'] = msp_data.apply(get_jitter, axis='columns')
msp_data['Shimmer'] = msp_data.apply(get_shimmer, axis='columns')
msp_data['HNR'] = msp_data.apply(get_hnr, axis='columns')

msp_data.to_csv("acoustic_prosodic_features_output.csv", index=False)
