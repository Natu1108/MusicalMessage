import tkinter as tk
from tkinter import messagebox, filedialog, dialog
from mido import Message, MidiFile, MidiTrack
import os

# Mido variables
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Converts the ASCII character to notes
def encode():
    msg = entry.get()

    for letter in msg:
        track.append(Message('note_on', note=ord(letter), time=32))

    name = tk.simpledialog.askstring("Save MIDI", "Enter a name for the file (no extenstion, aka .mid):")

    if not name:
        return

    mid.save(f"{name}.mid")
    messagebox.showinfo(message=f"Encoded message has been save as '{name}.mid'")

# Converts notes to ASCII characters
def decode():
    decodedMsg = ""
    for msg in MidiFile('output.mid').play():
        if msg.type in ('note_on', 'note_off'):
            decodedMsg += chr(msg.note)
    output.config(text=decodedMsg)

# Choose the .mid file
def chooseMid():
    f = filedialog.askopenfile(
        title="Select a file",
        filetypes=(
            ("MIDI files", "*.mid"),
            ("All files", "*.*")
        )
    )

    if f:
        chooseBtn.config(text=os.path.basename(f.name))

# Setup the window
root = tk.Tk()
root.title("Musical Messages")
root.geometry("512x256")

# Setup widgets
frame = tk.Frame(root)
label = tk.Label(root, text="Input a message: ")
entry = tk.Entry(root)
btn = tk.Button(root, text="Submit", command=encode)
btnDecode = tk.Button(root, text="Decode", command=decode)
chooseBtn = tk.Button(root, text="Choose a file", command=chooseMid)
labelDecode = tk.Label(root, text="Decode a message: ")
output = tk.Label(root, text="")

# Place widgets on screen
label.grid(row=0, column=0)
entry.grid(row=0, column=1)
btn.grid(row=0, column=3)
labelDecode.grid(row=1,column=0)
chooseBtn.grid(row=1, column=1)
btnDecode.grid(row=1, column=2)
output.grid(row=2)

# Run the app
root.mainloop()