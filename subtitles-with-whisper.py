###############################
# Editable Variables
SEARCH_FOR_THIS_EXT = "mp4"
VERBOSE_SCRIPT = True
WHISPER_MODEL = "base"
WHISPER_VERBOSE = False
WHISPER_LANGUAGE = "English"
WHISPER_OUTPUTS = "txt,srt,vtt"
###############################

# Clear terminal and set title variables
import os
if os.name == 'nt':
    os.system("cls")
cwd = os.getcwd()
folder = os.path.basename(cwd)
if os.name == 'nt':
    os.system(
        f"title Subtitling {SEARCH_FOR_THIS_EXT}'s in {folder} ({cwd}) ^- OpenAI's Whisper ^& Seall^.DEV"
    )
print(
    """
  ____                                 _____  _       __          __ _      _                         
 / __ \                         /\    |_   _|( )      \ \        / /| |    (_)                        
| |  | | _ __    ___  _ __     /  \     | |  |/  ___   \ \  /\  / / | |__   _  ___  _ __    ___  _ __ 
| |  | || '_ \  / _ \| '_ \   / /\ \    | |     / __|   \ \/  \/ /  | '_ \ | |/ __|| '_ \  / _ \| '__|
| |__| || |_) ||  __/| | | | / ____ \  _| |_    \__ \    \  /\  /   | | | || |\__ \| |_) ||  __/| |   
 \____/ | .__/  \___||_| |_|/_/    \_\|_____|   |___/     \/  \/    |_| |_||_||___/| .__/  \___||_|   
        | |                                                                        | |                
        |_|                                                                        |_|  
Script by Seall.DEV

"""
)
if VERBOSE_SCRIPT == True:
    print("Loading libraries...")
# Load libraries
import whisper
import webvtt
import ast
from datetime import timedelta

# Define variable
filecount = 0
progcount = 1
files = []
START = "start"
END = "end"
TEXT = "text"
if VERBOSE_SCRIPT == True:
    print(f"Loading model {WHISPER_MODEL}...")
# Load model
model = whisper.load_model(WHISPER_MODEL)
if VERBOSE_SCRIPT == True:
    print(f"Searching for files with the extension {SEARCH_FOR_THIS_EXT}...")
for f in os.listdir(cwd):
    if f.endswith(SEARCH_FOR_THIS_EXT):
        filecount += 1
        files.append(f)
if VERBOSE_SCRIPT == True:
    print(f"Found {str(filecount)} files with extension {SEARCH_FOR_THIS_EXT}!")
if filecount == 0:
    quit
print(f"Subtitling {str(filecount)} files...")
def nosubs(progcount):
    if VERBOSE_SCRIPT == True:
        print(f"Subtitles for {f} already exist!")
    if os.name == 'nt':
        os.system(
            f"title Skipping {f} ({str(progcount)}/{str(filecount)}) ^- Subtitling {SEARCH_FOR_THIS_EXT}'s in {folder} ({cwd}) ^- OpenAI's Whisper ^& Seall^.DEV"
        )
    progcount += 1
for f in files:
    # If subtitles already exist
    if os.path.exists(f"{f}.srt") or os.path.exists(f"{f}.txt") or os.path.exists(f"{f}.vtt"):
        if "srt" in WHISPER_OUTPUTS:
            if os.path.exists(f"{f}.srt"):
                nosubs(progcount)
        elif "vtt" in WHISPER_OUTPUTS:
            if os.path.exists(f"{f}.vtt"):
                nosubs(progcount)
        elif "txt" in WHISPER_OUTPUTS:
            if os.path.exists(f"{f}.txt"):
                nosubs(progcount)
        progcount += 1
    else: 
        # Generate subtitles
        print(f"Subtitling {f}...")
        if os.name == 'nt':
            os.system(
                f"title Working on {f} ({str(progcount)}/{str(filecount)}) ^- Subtitling {SEARCH_FOR_THIS_EXT}'s in {folder} ({cwd}) ^- OpenAI's Whisper ^& Seall^.DEV"
            )
        if not os.path.exists(f"{f}.temp"):
            r = model.transcribe(f,language=WHISPER_LANGUAGE,verbose=WHISPER_VERBOSE)
            with open(f"{f}.temp", "w", encoding="utf-8") as file:
                file.write(str(r))
                file.close()
            if VERBOSE_SCRIPT == True:
                print(f"Subtitle data temporarily written to {f}.temp incase of failure.")
        else:
            with open(f"{f}.temp", "r", encoding="utf-8") as file:
                r = ast.literal_eval(file.read())
                file.close()
            if VERBOSE_SCRIPT == True:
                print(f"Subtitle data read from {f}.temp!")
        ### TXT ###
        formatted_outputs = WHISPER_OUTPUTS.split(",")
        if len(formatted_outputs) == 1:
            formatted_outputs = "".join(formatted_outputs)
        else:
            formatted_outputs[len(formatted_outputs) - 1] = "and " + formatted_outputs[len(formatted_outputs) - 1]
            formatted_outputs = ", ".join(formatted_outputs)
        if VERBOSE_SCRIPT == True:
            print(f"Making subtitle files to {formatted_outputs}...")
        if "txt" in WHISPER_OUTPUTS:
            with open(f"{f}.txt", "w", encoding="utf-8") as file:
                for seg in r["segments"]:
                    file.write(f"{str(seg[TEXT])[1:len(str(seg[TEXT]))]}\n")
                file.close()
                if VERBOSE_SCRIPT == True:
                    print(f"Text subtitles written to {f}.txt!")
        ### SRT ###
        if "srt" in WHISPER_OUTPUTS or "vtt" in WHISPER_OUTPUTS:
            with open(f"{f}.srt", "w", encoding="utf-8") as file:
                for seg in r["segments"]:
                    id = int(seg["id"]) + 1
                    seg[START] = str("{:.3f}".format(float(seg[START])))
                    start = timedelta(seconds=int(str(seg[START]).split(".")[0]))
                    startdec = str(seg[START]).split(".")[1]
                    seg[END] = str("{:.3f}".format(float(seg[END])))
                    end = timedelta(seconds=int(str(seg[END]).split(".")[0]))
                    enddec = str(seg[END]).split(".")[1]
                    text = str(seg[TEXT])[1 : len(str(seg[TEXT]))]
                    file.write(
                        f"{str(id)}\n{str(start)},{str(startdec)} --> {str(end)},{str(enddec)}\n{text}\n\n"
                    )
                file.close()
                if "srt" in WHISPER_OUTPUTS:
                    if VERBOSE_SCRIPT == True:
                        print(f"Text subtitles written to {f}.srt!")
        ### WEBVTT ###
        if "vtt" in WHISPER_OUTPUTS:
            webvtt.from_srt(f"{f}.srt").save(output=f"{f}.vtt")
            if not "srt" in WHISPER_OUTPUTS:
                os.remove(f"{f}.srt")
            if VERBOSE_SCRIPT == True:
                print(f"Text subtitles written to {f}.vtt!")
        ### FINISH ###
        os.remove(f"{f}.temp")
        if VERBOSE_SCRIPT == True:
            print(f"{f}.temp removed.")
        print(f"Subtitles finished for {f}!")
        progcount += 1
