
## Setup
### Open AI Whisper
Install ffmpeg and Rust to install.


```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

M1 Mac:
```
brew install ffmpeg
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip install git+https://github.com/openai/whisper.git
```

### Pyannote-audio
This package uses [https://github.com/pyannote/pyannote-audio](https://github.com/pyannote/pyannote-audio) for speaker diarization.

```
pip install torch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0
pip install pyannote.audio
```

### Poetry
[Poetry](https://python-poetry.org/) is used for dependancy management

```
poetry shell
poetry install
```

# Running
You can run the script using:

```
python main.py
```

# Useful commands
## youtube-dl
It's useful to be able to download youtube audio clips using [youtube-dl](https://github.com/ytdl-org/youtube-dl) and run:
```
youtube-dl -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 "https://www.youtube.com/watch?v=RDr0Id_y15M"
```

# Output Files
I'm using a couple of videos to explore the capabilities of the script. 

There's two output files that have been parsed:

## Large in-person discussion (13 people, cross-talk, distant mic)
[https://www.youtube.com/watch?v=utW1ItcMeJw](https://www.youtube.com/watch?v=utW1ItcMeJw)

[transcript-in-person-discussion-13-people.json](transcript-in-person-discussion-13-people.json)
```
[{
  "file": "outputs/305.0240625-308.3315625-SPEAKER_02.wav",
  "text": " I think we just have to have the discussion if we don't establish that.",
  "start": 305.0240625,
  "end": 308.3315625,
  "speaker": "SPEAKER_02",
  "url": "https://youtu.be/utW1ItcMeJw?t=305"
}]
```

## Small Zoom group conversation (4 people, clean turn taking, close mic)
[https://www.youtube.com/watch?v=RDr0Id_y15M](https://www.youtube.com/watch?v=RDr0Id_y15M)

[transcript-zoom-4-people.json](transcript-zoom-4-people.json)
```
[{
  "file": "outputs/251.27718750000003-253.8928125-P1_Lilly.wav",
  "text": " So determination and persistence is important.",
  "start": 251.27718750000003,
  "end": 253.8928125,
  "speaker": "P1_Lilly",
  "url": "https://youtu.be/RDr0Id_y15M?t=251"
}]
```

