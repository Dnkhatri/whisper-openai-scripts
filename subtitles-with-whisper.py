###############################
# Editable Variables
EXT = "mp4"
WHISPER_MODEL = "base"
OUTPUTS = "txt,srt,vtt"
###############################

# Clear terminal and set title variables
import os

os.system("cls")
cwd = os.getcwd()
folder = os.path.basename(cwd)
os.system(
    f"title Subtitling {EXT}'s in {folder} ({cwd}) ^- OpenAI's Whisper ^& Seall^.DEV"
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


Loading libraries..."""
)
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
print(f"Loading model {WHISPER_MODEL}...")
# Load model
model = whisper.load_model(WHISPER_MODEL)
print(f"Searching for files with the extension {EXT}...")
for f in os.listdir(cwd):
    if f.endswith(EXT):
        filecount += 1
        files.append(f)
print(f"Found {str(filecount)} files with extension {EXT}!")
if filecount == 0:
    quit
print(f"Subtitling {str(filecount)} files...")
for f in files:
    # If subtitles already exist
    if os.path.exists(f"{f}.srt"):
        print(f"Subtitles for {f} already exist!")
        os.system(
            f"title Skipping {f} ({str(progcount)}/{str(filecount)}) ^- Subtitling {EXT}'s in {folder} ({cwd}) ^- OpenAI's Whisper ^& Seall^.DEV"
        )
        progcount += 1
    else: 
        # Generate subtitles
        print(f"Subtitling {f}...")
        os.system(
            f"title Working on {f} ({str(progcount)}/{str(filecount)}) ^- Subtitling {EXT}'s in {folder} ({cwd}) ^- OpenAI's Whisper ^& Seall^.DEV"
        )
        if not os.path.exists(f"{f}.temp"):
            r = model.transcribe(f)
            with open(f"{f}.temp", "w") as file:
                file.write(str(r))
                file.close()
            print(f"Subtitle data temp-written to {f}.temp")
        else:
            with open(f"{f}.temp", "r") as file:
                r = ast.literal_eval(file.read())
                file.close()
            print(f"Subtitle data read from {f}.temp!")
        ### TXT ###
        formatted_outputs = OUTPUTS.split(",")
        if len(formatted_outputs) == 1:
            formatted_outputs = "".join(formatted_outputs)
        else:
            formatted_outputs[len(formatted_outputs) - 1] = "and " + formatted_outputs[len(formatted_outputs) - 1]
            formatted_outputs = ", ".join(formatted_outputs)
        print(f"Making subtitle files to {formatted_outputs}...")
        if "txt" in OUTPUTS:
            with open(f"{f}.txt", "w") as file:
                for seg in r["segments"]:
                    file.write(f"{str(seg[TEXT])[1:len(str(seg[TEXT]))]}\n")
                file.close()
                print(f"Text subtitles written to {f}.txt!")
        ### SRT ###
        if "srt" in OUTPUTS or "vtt" in OUTPUTS:
            with open(f"{f}.srt", "w") as file:
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
                if "srt" in OUTPUTS:
                    print(f"Text subtitles written to {f}.srt!")
        ### WEBVTT ###
        if "vtt" in OUTPUTS:
            webvtt.from_srt(f"{f}.srt").save(output=f"{f}.vtt")
            if not "srt" in OUTPUTS:
                os.remove(f"{f}.srt")
            print(f"Text subtitles written to {f}.vtt!")
        ### FINISH ###
        print(f"Subtitles finished for {f}!")
        os.remove(f"{f}.temp")
        progcount += 1
