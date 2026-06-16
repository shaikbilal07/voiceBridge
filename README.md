# voiceBridge
# VoiceBridge

## Real-Time Multilingual Language Conversion Platform

VoiceBridge is an AI-powered application that captures English speech, converts it into text, translates it into multiple Indian languages, generates subtitles, and provides synthesized audio output.

The project is designed for real-time language conversion during meetings, presentations, online training sessions, and educational environments.

---

## Features

### Speech Recognition

* Captures voice input using microphone
* Converts speech to text using OpenAI Whisper

### Multilingual Translation

Supports multiple Indian languages:

* Telugu
* Hindi
* Tamil
* Kannada
* Malayalam
* Marathi
* Gujarati
* Punjabi
* Bengali

### Subtitle Generation

* Displays translated subtitles instantly
* Large caption display for better readability

### Telugu Romanization

* Converts Telugu script into English letters
* Useful for users who cannot read Telugu script

### Audio Synthesis

* Generates translated speech output
* Plays translated audio directly in the application

### Activity History

* Stores recent translation sessions
* Displays source and translated content

### Export Support

* Download translated transcripts as text files

---

## Technology Stack

### Frontend

* Streamlit

### Speech Recognition

* OpenAI Whisper

### Translation Engine

* Deep Translator (Google Translate)

### Text-to-Speech

* Google Text-to-Speech (gTTS)

### Transliteration

* Indic Transliteration Library

### Audio Processing

* FFmpeg

---

## System Architecture

Voice Input
↓
Whisper Speech Recognition
↓
English Text Extraction
↓
Translation Engine
↓
Target Language Generation
↓
Subtitle Rendering
↓
Audio Synthesis
↓
Output Audio Playback

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd VoiceBridge
```

### Install Dependencies

```bash
pip install streamlit
pip install openai-whisper
pip install audio-recorder-streamlit
pip install deep-translator
pip install gtts
pip install indic-transliteration
```

### Install FFmpeg

Download FFmpeg and add it to your system PATH.

Verify installation:

```bash
ffmpeg -version
```

---

## Run Application

```bash
python -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Project Workflow

1. User selects a target language.
2. User records speech.
3. Whisper converts speech into English text.
4. Translation engine translates text.
5. Application displays subtitles.
6. Audio is generated in the selected language.
7. User can listen or download transcript.

---

## Example

### Input

```text
Good morning everyone.
```

### Telugu Output

```text
అందరికీ శుభోదయం
```

### Roman Telugu

```text
Andariki Subhodayam
```

---

## Future Enhancements

* Real-time streaming translation
* Meeting transcript storage
* User authentication
* Cloud deployment
* AI meeting summarization
* Live caption overlays
* Additional language support

---

## Author

Developed as an AI-based multilingual communication platform for academic and demonstration purposes.

---

## Version

VoiceBridge v1.0
