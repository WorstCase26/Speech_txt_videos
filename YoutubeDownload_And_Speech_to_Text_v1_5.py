# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 14:35:14 2021

@author: HawaiiDive
@author: Marcus

This code will take a link from Youtube, download the video at the highest
resolution possible to the folder where this script is located, then it will
attempt to extract the text from the video into a transcript text file.

"""
import time
t0 = time.time() # Start the Time Variable

import os
from pytube import YouTube
import speech_recognition as sr #pip install SpeechRecognition
import moviepy.editor as mp #pip install moviepy --user
import wave #pip install wave
import contextlib
import pandas as pd

def create_out_dir(dir_name):
    file_path = os.getcwd()
    download_folder = file_path + '\\' + dir_name
    if not os.path.isdir(download_folder):
        os.mkdir(download_folder)
        download_folder = download_folder + '\\'
    else:
        download_folder = download_folder + '\\'
    print("Download_folder "+ download_folder)
    return download_folder

def download_youtube(link):
    yt = YouTube(link)
        
    #Showing details of the video
    print()
    print("Title: ", yt.title)
    title = yt.title
    print("Number of views: ",yt.views)
    views = yt.views
    print("Length of video: ",yt.length)
    length = yt.length
    print("Rating of video: ",yt.rating)
    rating = yt.rating
    
    special_chars = ["$",',','.', '/', "\\", ':', '*', '?','"','<','>',"|","(",")","[","]","{",'}']
    title = str(yt.title)
    title = title.replace(" ", "_")
    for char in special_chars:
        title = title.replace(char, "")
    filen = title + ".mp4"
    print("file name is " + filen)
    
    #Getting the highest resolution possible
    ys = yt.streams.get_highest_resolution()
    
    #prep dir
    download_folder = create_out_dir("Youtube_Downloads")
            
    #Starting download
    print()
    print("Downloading...")
    ys.download(filename= filen, output_path=download_folder) # Saves the video in a folder for you
    print("Download completed!!")
    filen = download_folder + filen
    return title, views, length, rating, filen
    
def create_youtube_attr_df(lst_links):
    #initiate containers to hold vars
    title_lst, views_lst, length_lst, rating_lst, filen_lst = [], [], [], [], []
    if type(lst_links) == str:
        print("Only 1 link was passed to process")
        title, views, length, rating, filen = download_youtube(link)
        title_lst.append(title)
        views_lst.append(views)
        length_lst.append(length)
        rating_lst.append(rating)
        filen_lst.append(filen)
    elif type(lst_links) == list:
        #loop through each link
        for each in lst_links:
            try:
                title, views, length, rating, filen = download_youtube(each)
                title_lst.append(title)
                views_lst.append(views)
                length_lst.append(length)
                rating_lst.append(rating)
                filen_lst.append(filen)
            except:
                title_lst.append('')
                views_lst.append('')
                length_lst.append('')
                rating_lst.append('')
                filen_lst.append('')
                print()
                print('Something is wrong with your link or connection')
    #=Pause between download and transcribe======================================
    print()
    print('Pausing code for 30 seconds to allow for the video to download')
    time.sleep(30) # 30 second pause to allow the video to fully download
    #============================================================================
    return title_lst, views_lst, length_lst, rating_lst, filen_lst

def get_vid_len(wav_name):
    with contextlib.closing(wave.open(wav_name,'r')) as video:
        frames = video.getnframes()
        rate = video.getframerate()
        duration = int(frames / float(rate))
    return duration

def convert_2_wav(vid_name):
    #prep the file names for the conversion
    video = mp.VideoFileClip(vid_name)
    path_p1 = create_out_dir("wav_files")
    wav_name = vid_name.split(".")[0] + ".wav"
    wav_name = path_p1 + wav_name.split("\\")[-1]
    
    #start the conversions
    print("\n")
    print("Converting video file to .wav file type...")
    video.audio.write_audiofile(wav_name)
    return wav_name
    
def get_video_text(wav_name):
    if wav_name.split(".")[-1] != "wav":
        wav_name = convert_2_wav(wav_name)
    #initialize variables
    txt_name = wav_name.split(".")[0] + ".txt"
    rec = sr.Recognizer()
    
    #Prepare the variables to segment the videos for passing to Google's API (max length is 60 seconds per segment)
    video_audio = sr.AudioFile(wav_name)
    total_len = get_vid_len(wav_name) #get the length of the input video
    time_dur = 50 #set the time per segment
    durations = total_len // time_dur #set the number of segments to pass as the # of iterations for the loop 
    last_duration = total_len - (durations * time_dur) #calculate the unique duration length for the last duration
    
    #initialize variable to hold all text from the video
    text = ""
    
    #prep the audio
    for d in range(durations + 1):
        print("Processing part " +str(d + 1)+" out of "+ str(durations +1)+" total parts")
        off = d * time_dur
        try:
            if d == durations:
                with video_audio as source:
                    just_audio = rec.record(source, duration = last_duration, offset=off)
            else:
                with video_audio as source:
                    just_audio = rec.record(source, duration = time_dur, offset=off)
            #Start the Google's Text recognition
            print('Converting speech to text...')
            text += rec.recognize_google(just_audio)
        except:
            print('Error Procesing part ' +str(d+1))
            text += "___________Error Parsing video from second "+str(off)+" to "+str(off + time_dur)+" ________"

    #Output the text to a text file
    print("Creating Text out folder")
    print(txt_name)
    text_folder = create_out_dir("Output") + txt_name.split("\\")[-1]
    print()
    print("Now writing the video text to the output file")
    with open(text_folder, mode='w') as file:
        file.write("Video Transcript:")
        file.write("\n")
        file.write(text)

    print()    
    print("Text file with transcript is now ready")
    return txt_name, text

def main_youtube_s2t(links):
    title_lst, views_lst, length_lst, rating_lst, filenames_lst = create_youtube_attr_df(links)
    txt_name_lst, text_lst = [], []
    for youtube in filenames_lst:
        print("Now getting transcript for " + youtube.split("\\")[-1])
        try:
            txt_name, text = get_video_text(youtube)
            txt_name_lst.append(txt_name)
            text_lst.append(text)
        except:
            print("Error occured while conducting speech to text conversion")
            txt_name, text = "", ""
            txt_name_lst.append(txt_name)
            text_lst.append(text)
    out_df = pd.DataFrame({"Title":title_lst, "# of Views":views_lst, "Length of Video (seconds)":length_lst, 
                           "Rating of Video":rating_lst, "Video File Link": filenames_lst, "Text Output Link":txt_name_lst,
                           "Transcription of Video":text_lst})
    out_folder = create_out_dir("Output")
    out_df.to_excel(out_folder+"Speech_to_text.xlsx")
    return out_df


if __name__ == "__main__":
   link = ["https://youtu.be/TBuIGBCF9jc"]
   out_df = main_youtube_s2t(link)
        
   # Printing the computational times for the calculations above based on your system
   #=============================================================================
   # We want to evaluate a program's efficiency when the input is very large
   import platform
   my_system = platform.uname()

   #=============================================================================
   print()
   print("Time: It took your computer", round(time.time() - t0, 2) , "seconds to completely run all calcualations.")
   print("Power: You computer is using", os.cpu_count(), "cores to process this data")
   print()
   
   print("Current PC Specs:")
   print(f"-System: {my_system.system}")
   print(f"-Machine: {my_system.machine}")
   print(f"-Processor: {my_system.processor}")
   print()
   
   #C:\\Users\\Marcus\\OneDrive\\Desktop\\Similarity\\Video_to_text\\Youtube_Downloads\\Admiral_McRaven_Leaves_the_Audience_SPEECHLESS__One_of_the_Best_Motivational_Speeches.mp4"
