import customtkinter as tk
from tkinter import messagebox, filedialog
from mido import Message, MidiFile, MidiTrack
import os, pygame, time

# Mido variables
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)
fp = ""

# Converts the ASCII character to notes
def encode():
    global fp
    msg = entry.get()

    for letter in msg:
        track.append(Message('note_on', note=ord(letter), time=32))

    dialog = tk.CTkInputDialog(title="Save MIDI", text="Enter a name for the file (no extenstion, aka .mid):")

    name = dialog.get_input()

    if not name:
        return

    mid.save(f"{name}.mid")
    messagebox.showinfo(message=f"Encoded message has been save as '{name}.mid'")

# Converts notes to ASCII characters
def decode():
    global fp
    decodedMsg = ""
    for msg in MidiFile(fp).play():
        if msg.type in ('note_on', 'note_off'):
            decodedMsg += chr(msg.note)
    output.configure(text=decodedMsg)

# Choose the .mid file
def chooseMid():
    global fp
    f = filedialog.askopenfile(
        title="Select a file",
        filetypes=(
            ("MIDI files", "*.mid"),
            ("All files", "*.*")
        )
    )

    if f:
        chooseBtn.configure(text=os.path.basename(f.name))
        fp = os.path.basename(f.name)

# Plays the .mid file to show what the audio sounds like
def playMid():
    global fp
    pygame.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()

    # Keep the script running while the music plays
    while pygame.mixer.music.get_busy():
        time.sleep(1)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

# Setup the window
root = tk.CTk()
root.title("Musical Messages")
root.geometry("512x256")

# Setup widgets
frame = tk.CTkFrame(root)
label = tk.CTkLabel(root, text="Input a message: ")
entry = tk.CTkEntry(root)
btn = tk.CTkButton(root, text="Submit", command=encode)
btnDecode = tk.CTkButton(root, text="Decode", command=decode)
chooseBtn = tk.CTkButton(root, text="Choose a file", command=chooseMid)
labelDecode = tk.CTkLabel(root, text="Decode a message: ")
btnPlay = tk.CTkButton(root, text="Play the audio", command=playMid)
output = tk.CTkLabel(root, text="", anchor="w")

# Place widgets on screen
label.grid(row=0, column=0)
entry.grid(row=0, column=1)
btn.grid(row=0, column=3)
labelDecode.grid(row=1,column=0)
chooseBtn.grid(row=1, column=1)
btnDecode.grid(row=1, column=2)
btnPlay.grid(row=2)
output.grid(row=2, column=2, columnspan=3)

# Run the app
root.mainloop()
