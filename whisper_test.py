import os
import whisper

os.environ["PATH"] += r";C:\Users\RO\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-essentials_build\bin"

print("Loading model...")

model = whisper.load_model("base")

result = model.transcribe("output.wav")

print(result["text"])