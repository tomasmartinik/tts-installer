from gtts import gTTS
import os

text = "Ahoj, vítám tě u výuky biologie. Dnes si povíme o buňkách."
tts = gTTS(text=text, lang='cs')
tts.save("vyuka.mp3")
os.system("afplay vyuka.mp3")  # macOS
