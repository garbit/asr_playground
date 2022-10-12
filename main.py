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

speakers = {
    "SPEAKER_00": "P1_Nicole",
    "SPEAKER_01": "P1_Lilly",
    "SPEAKER_02": "P2_Dorothy",
    "SPEAKER_03": "P3_Ryan",
}

turns = []
for turn, _, speaker in diarization.itertracks(yield_label=True):
    turns.append({
        "start": turn.start,
        "end": turn.end,
        "speaker": speakers[speaker]
    })

for turn in turns:
    split_audio_at_timestamp(turn['start'], turn['end'], 'audio.wav', f'outputs/{turn["start"]}-{turn["end"]}-{turn["speaker"]}.wav')

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

with open('transcript.json', 'w') as f:
    f.write(json.dumps(transcriptions))
        
# print(f'Transcribed in {round(model_transcribe_end_time - model_transcribe_start_time)}secs')