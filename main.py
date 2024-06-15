import os
import librosa
import soundfile as sf
from moviepy.editor import VideoFileClip
import pyttsx3
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from deepmultilingualpunctuation import PunctuationModel
from pydub import AudioSegment
from moviepy.editor import AudioFileClip, concatenate_audioclips
from pydub.silence import split_on_silence
from test import add_comma


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 140)


def say(audio):
    engine.say(audio)
    engine.runAndWait()


def time_stretching(i, audio_file, lang, wav_conv_file):
    input_audio = AudioSegment.from_file(wav_conv_file, format="wav")
    audio, sr = librosa.load(audio_file, sr = 44100)
    current_duration = librosa.get_duration(y = audio, sr=sr)
    stretch_factor = current_duration/(len(input_audio)/1000)
    slow_audio = librosa.effects.time_stretch(y=audio, rate=stretch_factor)
    pitch = librosa.effects.pitch_shift(y=slow_audio, n_steps=-1, sr=sr)
    sf.write(f"cipam_{lang}{i}.wav", pitch, samplerate=44100, format="wav")

def merge(lang, i):
    mp3_files = []

    for a in range(1, i):
        audio = f"cipam_{lang}{a}.wav"
        mp3_files.append(audio)

    merged_audio = AudioFileClip(mp3_files[0])

    for mp3_file in mp3_files[1:]:
        audio_segment = AudioFileClip(mp3_file)
        end = AudioFileClip("chunk_12.wav")
        merged_audio = concatenate_audioclips([merged_audio, audio_segment])

    #final_audio = concatenate_audioclips([merged_audio, end])

    merged_audio.write_audiofile(f"cipam_{lang}.wav")

def final(audio_final, video_file, lang):
    new_audio_clip = AudioFileClip(audio_final)
    video_clip = video_file.set_audio(new_audio_clip)
    video_clip.write_videofile(f"cipam_{lang}_video.mp4", codec="libx264", audio_codec="aac")



def main_func(video_file, lang):

    video = VideoFileClip(video_file)
    convert_to_audio = video.audio
    convert_to_audio.write_audiofile("audio_file.wav", codec='pcm_s16le')

    audio_file = "audio_file.wav"

    chunk_length_ms = 120000
    
    say("Dividing video file into chunks!")

    audio = AudioSegment.from_file(audio_file, format="wav")
    start_time = 0
    end_time = chunk_length_ms

    output = "audio_chunks_cipam"
    os.makedirs(output, exist_ok=True)

    say("Processing")

    i = 1
    while start_time < len(audio):
        chunk = audio[start_time:end_time]
        output_file = os.path.join(output, f"chunk_{i}.wav")
        chunk.export(output_file, format="wav")

        com = sr.Recognizer()

        with sr.AudioFile(output_file) as source:
            print("Transcribing audio path...")
            com.pause_threshold = 10
            Audio = com.record(source)
            try:
                print(f"{i}. Recognizing...")
                say(f"Recognizing chunk {i}.")
                say("Wait for some time")
                command = com.recognize_google(Audio, language='en-in')
                model = PunctuationModel()
                sent = model.restore_punctuation(command)
                punct = add_comma(sent)
                say(f"Translating chunk {i}.")
                translator = Translator()
                text_translate = translator.translate(punct, src='en', dest=lang)
                translation = text_translate.text
                tts = gTTS(translation, lang=lang)
                tts.save(f"cipam_{lang}{i}.mp3")
                input_for_timesync = f"cipam_{lang}{i}.mp3"
            
                file = AudioFileClip(input_for_timesync)
                file.write_audiofile(f"cipam_{lang}{i}.wav")
                wav_conv_file = f"cipam_{lang}{i}.wav"


                if i==1:

                    original = AudioSegment.from_file(audio_file, format="wav")
                    #bgm = original[0:7300]
                    input_audio = AudioSegment.from_file(f"cipam_{lang}{i}.wav", format="wav")
                    segments = split_on_silence(input_audio, min_silence_len= 350,silence_thresh=-40)
                    pause_duration = 700  
                    pause = AudioSegment.silent(duration=pause_duration)
                    output_audio = AudioSegment.silent(duration=400)
                    for segment in segments:
                        output_audio += segment + pause
                    sync =  output_audio
                    sync.export(f"cipam_{lang}{i}.wav", format="wav")

                elif i == 6:

                    input_audio = AudioSegment.from_file(wav_conv_file, format="wav")
                    original = AudioSegment.from_file("audio_file.wav", format="wav")

                    bgm = original[705000:720000]

                    segments = split_on_silence(input_audio, min_silence_len= 400,silence_thresh=-40)  
                    pause_duration = 700
                    pause = AudioSegment.silent(duration=pause_duration)
                    output_audio = AudioSegment.silent(duration=0)

                    for segment in segments:
                        output_audio += segment + pause

                    synced = output_audio + bgm

                    synced.export(f"cipam_{lang}{i}.wav", format="wav")


                elif i == 7:

                    input_audio = AudioSegment.from_file(wav_conv_file, format="wav")
                    original = AudioSegment.from_file("audio_file.wav", format="wav")

                    bgm = original[720000:763000]

                    segments = split_on_silence(input_audio, min_silence_len= 500,silence_thresh=-40)  
                    pause_duration = 1200
                    pause = AudioSegment.silent(duration=pause_duration)
                    output_audio = AudioSegment.silent(duration=0)

                    for segment in segments:
                        output_audio += segment + pause

                    synced = bgm + output_audio 

                    synced.export(f"cipam_{lang}{i}.wav", format="wav")

                else:
                    input_audio = AudioSegment.from_file(wav_conv_file, format="wav")

                    if len(wav_conv_file) >= 80000 and len(wav_conv_file) < 85000 :

                        segments = split_on_silence(input_audio, min_silence_len= 300,silence_thresh=-40)  
                        pause_duration = 1500
                        pause = AudioSegment.silent(duration=pause_duration)
                        output_audio = AudioSegment.silent(duration=500)


                    if len(wav_conv_file) < 80000:

                        segments = split_on_silence(input_audio, min_silence_len= 275,silence_thresh=-40)  
                        pause_duration = 1500
                        pause = AudioSegment.silent(duration=pause_duration)
                        output_audio = AudioSegment.silent(duration=500)

                


                    elif len(wav_conv_file) >= 85000 and len(wav_conv_file) < 90000:

                        segments = split_on_silence(input_audio, min_silence_len= 325,silence_thresh=-40)  
                        pause_duration = 1300
                        pause = AudioSegment.silent(duration=pause_duration)
                        output_audio = AudioSegment.silent(duration=500)


                    elif len(wav_conv_file) >= 90000 and len(wav_conv_file) < 95000:

                        segments = split_on_silence(input_audio, min_silence_len=330,silence_thresh=-40)  
                        pause_duration = 1150
                        pause = AudioSegment.silent(duration=pause_duration) 
                        output_audio = AudioSegment.silent(duration=500)


                    elif len(wav_conv_file) >= 95000 and len(wav_conv_file) < 100000:

                        segments = split_on_silence(input_audio, min_silence_len=350,silence_thresh=-40)  
                        pause_duration = 1000
                        pause = AudioSegment.silent(duration=pause_duration) 
                        output_audio = AudioSegment.silent(duration=500)


                    elif len(wav_conv_file) >= 100000 and len(wav_conv_file) < 105000:

                        segments = split_on_silence(input_audio, min_silence_len=350,silence_thresh=-40)  
                        pause_duration = 1000
                        pause = AudioSegment.silent(duration=pause_duration) 
                        output_audio = AudioSegment.silent(duration=500)


                    elif len(wav_conv_file) >= 105000 and len(wav_conv_file) < 110000:

                        segments = split_on_silence(input_audio, min_silence_len=400,silence_thresh=-40)  
                        pause_duration = 800
                        pause = AudioSegment.silent(duration=pause_duration) 
                        output_audio = AudioSegment.silent(duration=500)


                    elif len(wav_conv_file) >= 105000 and len(wav_conv_file) < 110000:

                        segments = split_on_silence(input_audio, min_silence_len=500,silence_thresh=-40)  
                        pause_duration = 700
                        pause = AudioSegment.silent(duration=pause_duration) 
                        output_audio = AudioSegment.silent(duration=500)


                    else:
                        pause = AudioSegment.silent(duration=0)
                        output_audio = AudioSegment.silent(duration=500)


                    for segment in segments:
                        output_audio += segment + pause
                    output_audio.export(f"cipam_{lang}{i}.wav", format="wav")

                time_synced_audio = f"cipam_{lang}{i}.wav"

                time_stretching(i, time_synced_audio, lang, wav_conv_file=output_file)

                say(f"Translated chunk {i} ready.")
                


            except sr.UnknownValueError:
                print("I am unable to understand!")
                say("I am unable to understand!")
            except sr.RequestError:
                print("Error with speech recognition service!")
                say("Error with speech recognition service!")


        start_time = end_time
        end_time += chunk_length_ms
        i += 1

    say("Translated Chunks ready")
    merge(lang,i)
    final(f"cipam_{lang}.wav", video, lang)
    say("Processing completed! Output ready.")
    print("Output ready!")

'''
                if i==1:

                    original = AudioSegment.from_file(audio_file, format="wav")
                    bgm = original[0:7300]
                    input_audio = AudioSegment.from_file(f"cipam_{lang}{i}.wav", format="wav")
                    segments = split_on_silence(input_audio, min_silence_len= 350,silence_thresh=-40)
                    pause_duration = 900  
                    pause = AudioSegment.silent(duration=pause_duration)
                    output_audio = AudioSegment.silent(duration=400)
                    for segment in segments:
                        output_audio += segment + pause
                    sync = bgm + output_audio
                    sync.export(f"cipam_{lang}{i}.wav", format="wav")

                elif i == 6:

                    input_audio = AudioSegment.from_file(wav_conv_file, format="wav")
                    original = AudioSegment.from_file("audio_file.wav", format="wav")

                    bgm = original[705000:720000]

                    segments = split_on_silence(input_audio, min_silence_len= 400,silence_thresh=-40)  
                    pause_duration = 700
                    pause = AudioSegment.silent(duration=pause_duration)
                    output_audio = AudioSegment.silent(duration=0)

                    for segment in segments:
                        output_audio += segment + pause

                    synced = output_audio + bgm

                    synced.export(f"cipam_{lang}{i}.wav", format="wav")


                elif i == 7:

                    input_audio = AudioSegment.from_file(wav_conv_file, format="wav")
                    original = AudioSegment.from_file("audio_file.wav", format="wav")

                    bgm = original[720000:763000]

                    segments = split_on_silence(input_audio, min_silence_len= 500,silence_thresh=-40)  
                    pause_duration = 1200
                    pause = AudioSegment.silent(duration=pause_duration)
                    output_audio = AudioSegment.silent(duration=0)

                    for segment in segments:
                        output_audio += segment + pause

                    synced = bgm + output_audio 

                    synced.export(f"cipam_{lang}{i}.wav", format="wav")


'''