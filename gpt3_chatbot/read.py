from datetime import datetime
import subprocess
from playsound import playsound

def read_story(story: str, voice: str, filename: str = None, read_out_loud: bool = True):
    if filename == None:
        # Set the filename to the current date with seconds
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp3"
    with open(f"{filename}.txt", "w", encoding="utf-8") as f:
        f.write(story)
    command = f'edge-tts --file "{filename}.txt" --write-media "{filename}.mp3" --voice {voice}'
    res = subprocess.check_output(command, shell=True)
    # Play the mp3 file
    if read_out_loud:
        playsound(filename + ".mp3")

