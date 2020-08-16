from tkinter import *
from tkinter import messagebox, filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import os
import time
import threading

mixer.init()

root = Tk()
root.iconbitmap(r"img/music-player.ico")
root.title("Mp3 Player")

# Creating the menu bar
menubar = Menu(root)
root.config(menu=menubar)


def browse_file():
    global filename
    filename = filedialog.askopenfilename()


def exit_player():
    root.destroy()


# Creating the submenus
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=exit_player)


def about_us():
    messagebox.showinfo("About Mp3 Player", "This is an Mp3 Player made by It guys in Pycharm.")


submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About Us", command=about_us)


def show_details():

    file_data = os.path.splitext(filename)

    if file_data[1] == ".mp3":
        audio = MP3(filename)
        total_length = audio.info.length
    else:
        a = mixer.Sound(filename)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = "{:02d}:{:02d}".format(mins, secs)
    length_label["text"] = "Total length" + " - " + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = "{:02d}:{:02d}".format(mins, secs)
            currentTime_label["text"] = "Time covered" + " - " + timeformat

            time.sleep(1)
            current_time += 1

def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar["text"] = "Music resumed"
        paused = FALSE     # Otherwise we can't pause the music again
    else:    # we want to play some music
        try:
            mixer.music.load(filename)
            mixer.music.play()
            statusbar["text"] = "Playing music" + " - " + os.path.basename(filename)
            show_details()
        except:
              messagebox.showerror("File not found",
                                   "Mp3 Player could not find the file specified. Please open an existing file.")

def stop_music():
    mixer.music.stop()
    statusbar["text"] = "Music stopped"

paused = FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar["text"] = "Music paused"

def rewind_music():
    play_music()
    statusbar["text"] = "Music rewinded"

def set_vol(val):
    volume = int(val)/100
    mixer.music.set_volume(volume)

muted = False

def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutephoto)
        scale.set(0)
        muted = TRUE


mutes = FALSE

length_label = Label(root, text="Total Length: --:--")
length_label.configure(font=("Corbel", 13, "normal"))
length_label.pack(padx=10, pady=10)

currentTime_label = Label(root, text="Time Covered: --:--")
currentTime_label.configure(font=("Corbel", 13, "normal"))
currentTime_label.pack(padx=10, pady=10)

middleFrame = Frame(root)
middleFrame.pack(padx=30, pady=30)

stopPhoto = PhotoImage(file="img/stop.png")
stopBtn = Button(middleFrame, image=stopPhoto, borderwidth=0, command=stop_music)
stopBtn.grid(row=0, column=0, padx=10)

playPhoto = PhotoImage(file="img/play.png")
playBtn = Button(middleFrame, image=playPhoto, borderwidth=0, command=play_music)
playBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file="img/pause.png")
pauseBtn = Button(middleFrame, image=pausePhoto, borderwidth=0, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

bottomFrame = Frame(root)
bottomFrame.pack()

rewindPhoto = PhotoImage(file="img/rewind.png")
rewindBtn = Button(bottomFrame, image=rewindPhoto, borderwidth=0, command=rewind_music)
rewindBtn.grid(row=0, column=0, pady=30)

mutephoto = PhotoImage(file="img/mute.png")

volumePhoto = PhotoImage(file="img/volume.png")
volumeBtn = Button(bottomFrame, image=volumePhoto, command=mute_music, borderwidth=0)
volumeBtn.grid(row=0, column=1, pady=30)

scale = Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, padx=30, pady=30)

statusbar = Label(root, text="Welcome to Mp3 Player!", anchor="w")
statusbar.configure(bg="white")
statusbar.pack(side=BOTTOM, fill=X)

statusbarPhoto = PhotoImage(file="img/statusbar_image.png")
statusbarLabel = Label(root, image=statusbarPhoto)
statusbarLabel.configure(bg="white")
statusbarLabel.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
