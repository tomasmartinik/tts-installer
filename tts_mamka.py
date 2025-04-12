from tkinter import Tk, Button
from gtts import gTTS

def speak():
    tts = gTTS("Ahoj světe", lang='cs')
    tts.save("test.mp3")

root = Tk()
root.geometry("200x100")
btn = Button(root, text="Spustit", command=speak)
btn.pack(pady=30)
root.mainloop()
