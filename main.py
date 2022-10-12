import whisper
import wave
import time
from pathlib import Path
import json

from pyannote.audio import Pipeline

def load_json(path):
    return json.load(open(path))

def split_audio_at_timestamp(start_in_sec, end_in_sec, audio_file, output_file):
    # file to extract the snippet from
    with wave.open(audio_file, "rb") as infile:
        # get file data
        nchannels = infile.getnchannels()
        sampwidth = infile.getsampwidth()
        framerate = infile.getframerate()
        # set position in wave to start of segment
        infile.setpos(int(start_in_sec * framerate))
        # extract data
        data = infile.readframes(int((end_in_sec - start_in_sec) * framerate))

    # write the extracted data to a new file
    with wave.open(output_file, 'w') as outfile:
        outfile.setnchannels(nchannels)
        outfile.setsampwidth(sampwidth)
        outfile.setframerate(framerate)
        outfile.setnframes(int(len(data) / sampwidth))
        outfile.writeframes(data)

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")

# https://www.youtube.com/watch?v=RDr0Id_y15M
# youtube_url = "https://www.youtube.com/watch?v=RDr0Id_y15M"
diarization = pipeline("audio.wav")

turns = []
for turn, _, speaker in diarization.itertracks(yield_label=True):
    turns.append({
        "start": turn.start,
        "end": turn.end,
        "speaker": speaker
    })

print("Splitting Audio")
split_count = 0
for turn in turns:
    split_count = split_count + 1
    split_audio_at_timestamp(turn['start'], turn['end'], 'audio.wav', f'outputs/{turn["start"]}-{turn["end"]}-{turn["speaker"]}.wav')
    print(f"Split {split_count}/{len(turns)}")

print('Transcribing Audio')
# load asr
model = whisper.load_model("base")
model_transcribe_start_time = time.time()

transcriptions = []
for turn in turns:
    result = model.transcribe(f'outputs/{turn["start"]}-{turn["end"]}-{turn["speaker"]}.wav')
    model_transcribe_end_time = time.time()
    transcriptions.append({
        "file": f'outputs/{turn["start"]}-{turn["end"]}-{turn["speaker"]}.wav',
        "text": result["text"],
        "start": turn["start"],
        "end": turn["end"],
        "speaker": turn["speaker"],
        "url": f"https://youtu.be/RDr0Id_y15M?t={int(turn['start'])}"
    })
    print(f"transcribed {len(transcriptions)}/{len(turns)}")

with open('transcript.json', 'w') as f:
    f.write(json.dumps(transcriptions))

print("Outputfile: transcript.json")
# print(f'Transcribed in {round(model_transcribe_end_time - model_transcribe_start_time)}secs')