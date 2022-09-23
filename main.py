import whisper
import time

model = whisper.load_model("base")

# model_transcribe_start_time = time.time()

# options = whisper.DecodingOptions(language="en", without_timestamps=False, fp16=False)

# audio = whisper.load_audio("test.mp3")
# audio = whisper.pad_or_trim(audio)
# mels = whisper.log_mel_spectrogram(audio).to(model.device)

# results = model.decode(mels, options)

result = model.transcribe("test.mp3")
# model_transcribe_end_time = time.time()

print(result)
# print(f'Transcribed in {round(model_transcribe_end_time - model_transcribe_start_time)}secs')