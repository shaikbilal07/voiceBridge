import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone(device_index=1) as source:
    print("Speak something...")

    recognizer.adjust_for_ambient_noise(source, duration=1)

    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("\nDetected Text:")
    print(text)

except sr.UnknownValueError:
    print("Could not understand audio")

except sr.RequestError as e:
    print("Speech Recognition Error:", e)