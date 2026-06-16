from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

text = "Good morning everyone"

telugu = GoogleTranslator(
    source="en",
    target="te"
).translate(text)

roman = transliterate(
    telugu,
    sanscript.TELUGU,
    sanscript.ITRANS
)

print("English:")
print(text)

print("\nTelugu:")
print(telugu)

print("\nRoman Telugu:")
print(roman)