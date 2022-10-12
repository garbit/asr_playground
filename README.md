
## Setup
### Open AI Whisper
Install ffmpeg and Rust to install.
```
brew install ffmpeg
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
pip install git+https://github.com/openai/whisper.git
```

### Pyannote-audio
This package uses [https://github.com/pyannote/pyannote-audio](https://github.com/pyannote/pyannote-audio) for speaker diarization.

Poetry is used for dependancy management

# Useful commands
## youtube-dl
```
youtube-dl -f bestaudio --extract-audio --audio-format mp3 --audio-quality 0 "https://www.youtube.com/watch?v=RDr0Id_y15M"
```