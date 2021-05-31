from pydub import AudioSegment
from moviepy.editor import *
from pytube import YouTube
import os
import tkinter
from tkinter.filedialog import asksaveasfile
import datetime

def save():
    files = [('MP4', '*.mp4'),('All Files', '*.*')]
    dt = datetime.date.today()
    return asksaveasfile(filetypes = files, defaultextension = files, initialfile = "Vendredi "+ str(dt.day)+"-"+str(dt.month))

def video():
    global root, lienvidéo, timecode, vidéotext, texttimecode, launch

    extrait = timecode.get().split(":")
    if len(extrait) != 2: texttimecode.config(text = "Merci de respecter le format min:sec ! (exemple: 02:03 )");return
    try:
        min = int(extrait[0])
        sec = int(extrait[1])
    except: texttimecode.config(text = "Merci de respecter le format min:sec ! (exemple: 02:03 )");return

    extrait = (min*60+sec)*1000
    extrait_fin = extrait + 5000

    try: yt = YouTube(lienvidéo.get())
    except: vidéotext.config(text = "Merci de mettre un lien de vidéo youtube valide !"); return

    out_file = yt.streams.filter(file_extension="mp4").first().download("mps")

    try: os.remove("mps\\custom.mp4")
    except:pass
    try: os.remove("mps\\custom.mp3")
    except:pass

    os.rename(out_file, "mps\\custom.mp4")
    my_clip = VideoFileClip("mps\\custom.mp4")
    my_clip.audio.write_audiofile("mps\\custom.mp3")
    
    sound = AudioSegment.from_mp3("mps\\custom.mp3")
    bonjourA = AudioSegment.from_mp3("mps\\bonjour.mp3")

    if len(sound) < extrait_fin: texttimecode.config(text = "Merci d'indiquer un timecode d'au moins 5 secondes avant la fin de la vidéo !");return

    sound = bonjourA + sound[extrait:extrait_fin]
    sound.export("mps\\custom.mp3", format="mp3")

    clip = VideoFileClip("mps\\bonjour.mp4")
    audioclip = AudioFileClip("mps\\custom.mp3")
    videoclip = clip.set_audio(audioclip)
    videoclip.write_videofile(save().name)

    launch["state"] = "disabled"
    launch.config(text = "Vous pouvez maintenant fermer cette fenêtre.")

root = tkinter.Tk()
root.grid()
root.title("Bonjour.")
jour = datetime.datetime.today().weekday()

#jour = 4 #RETIRER LE PREMIERE "#" POUR RENDRE L'APPLICATION ACCESSIBLE MÊME LORSQUE NOUS NE SOMMES PAS VENDREDI

jours = {0 : "Nous serons vendredi dans 4 jours.",
1: "Nous serons vendredi dans 3 jours.",
2: "Nous serons vendredi dans 2 jours.",
3: "Nous serons vendredi dans 1 jour.",
5: "Nous serons vendredi dans 6 jours.",
6: "Nous serons vendredi dans 5 jours.",
}

if jour != 4: lejour = jours.get(jour)
else: lejour = "Nous sommes vendredi."

jourdelasemaine = tkinter.Label(root, text = lejour); jourdelasemaine.pack()
espace1 = tkinter.Label(root, text = " "); espace1.pack()
vidéotext = tkinter.Label(root, text = "Lien de la vidéo :"); vidéotext.pack()
lienvidéo = tkinter.Entry(root); lienvidéo.pack()
espace2 = tkinter.Label(root, text = " "); espace2.pack()
texttimecode = tkinter.Label(root, text = "Time code de la musique (format min:sec):"); texttimecode.pack()
timecode = tkinter.Entry(root); timecode.pack()
espace3 = tkinter.Label(root, text = ""); espace3.pack()
if jour != 4: launch = tkinter.Button(root, text = "Nous ne sommes pas vendredi",state = "disabled", command = video); launch.pack()
else: launch = tkinter.Button(root, text = "Créer et sauvegarder", command = video); launch.pack()

root.mainloop()