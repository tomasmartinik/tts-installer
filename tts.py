import os
import threading
import fitz  # PyMuPDF
import customtkinter as ctk
from tkinter import filedialog, messagebox
from gtts import gTTS
from docx import Document

# -------------------------
# Funkce pro načtení textu ze souboru
# -------------------------
def load_text_from_file(path):
    if path.endswith(".docx"):
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    elif path.endswith(".pdf"):
        text = ""
        pdf = fitz.open(path)
        for page in pdf:
            text += page.get_text()
        return text
    else:
        raise ValueError("Nepodporovaný typ souboru.")

# -------------------------
# Funkce pro převod textu na řeč
# -------------------------
def convert_to_speech(input_path, output_path, button, progress_bar):
    try:
        button.configure(state="disabled")
        progress_bar.start()

        text = load_text_from_file(input_path)
        tts = gTTS(text=text, lang='cs')
        tts.save(output_path)

        messagebox.showinfo("Hotovo", f"Soubor byl uložen jako:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Chyba", f"Nastala chyba: {e}")
    finally:
        button.configure(state="normal")
        progress_bar.stop()

# -------------------------
# Procházení vstupu a výstupu
# -------------------------
def browse_input():
    path = filedialog.askopenfilename(filetypes=[
        ("Podporované dokumenty", "*.docx *.txt *.pdf"),
        ("Word dokumenty", "*.docx"),
        ("Textové soubory", "*.txt"),
        ("PDF dokumenty", "*.pdf")
    ])
    if path:
        input_entry.delete(0, "end")
        input_entry.insert(0, path)
        # Automatický návrh výstupu
        base_name = os.path.splitext(os.path.basename(path))[0] + ".mp3"
        output_path = os.path.join(os.path.dirname(path), base_name)
        output_entry.delete(0, "end")
        output_entry.insert(0, output_path)

def browse_output():
    path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 soubory", "*.mp3")])
    if path:
        output_entry.delete(0, "end")
        output_entry.insert(0, path)

# -------------------------
# Spuštění převodu ve vlákně
# -------------------------
def start_conversion():
    input_path = input_entry.get()
    output_path = output_entry.get()

    if not os.path.isfile(input_path):
        messagebox.showerror("Chyba", "Zadaný vstupní soubor neexistuje.")
        return
    if not output_path.endswith(".mp3"):
        messagebox.showerror("Chyba", "Výstupní soubor musí mít příponu .mp3")
        return

    thread = threading.Thread(target=convert_to_speech, args=(input_path, output_path, convert_button, progress_bar))
    thread.start()

# -------------------------
# GUI APLIKACE
# -------------------------
ctk.set_appearance_mode("system")  # nebo "dark" / "light"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🗣️ Převod dokumentu na MP3 – gTTS")
app.geometry("560x340")
app.resizable(False, False)

# Vstupní soubor
input_label = ctk.CTkLabel(app, text="📄 Vstupní soubor (.docx, .txt, .pdf):")
input_label.pack(anchor="w", padx=20, pady=(20, 5))
input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.pack(fill="x", padx=20)
input_entry = ctk.CTkEntry(input_frame)
input_entry.pack(side="left", fill="x", expand=True)
browse_input_btn = ctk.CTkButton(input_frame, text="Procházet", command=browse_input)
browse_input_btn.pack(side="left", padx=10)

# Výstupní soubor
output_label = ctk.CTkLabel(app, text="💾 Výstupní soubor (MP3):")
output_label.pack(anchor="w", padx=20, pady=(15, 5))
output_frame = ctk.CTkFrame(app, fg_color="transparent")
output_frame.pack(fill="x", padx=20)
output_entry = ctk.CTkEntry(output_frame)
output_entry.pack(side="left", fill="x", expand=True)
browse_output_btn = ctk.CTkButton(output_frame, text="Uložit jako", command=browse_output)
browse_output_btn.pack(side="left", padx=10)

# Tlačítko a progress bar
convert_button = ctk.CTkButton(app, text="▶️ Převést na MP3", width=200, command=start_conversion)
convert_button.pack(pady=20)
progress_bar = ctk.CTkProgressBar(app, mode="indeterminate")
progress_bar.pack(fill="x", padx=20, pady=(0, 15))

app.mainloop()
