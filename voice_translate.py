import speech_recognition as sr
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

recognizer = sr.Recognizer()

with sr.Microphone(device_index=1) as source:
    print("Speak something...")

    recognizer.adjust_for_ambient_noise(source, duration=1)

    audio = recognizer.listen(source)

try:
    english_text = recognizer.recognize_google(audio)

    print("\nEnglish:")
    print(english_text)

    telugu_text = GoogleTranslator(
        source="en",
        target="te"
    ).translate(english_text)

    roman_telugu = transliterate(
        telugu_text,
        sanscript.TELUGU,
        sanscript.ITRANS
    )

    print("\nTelugu:")
    print(telugu_text)

    print("\nRoman Telugu:")
    print(roman_telugu)

except sr.UnknownValueError:
    print("Could not understand audio")

except sr.RequestError as e:
    print("Speech Recognition Error:", e)