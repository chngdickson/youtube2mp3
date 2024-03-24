import tkinter as tk
from ctypes import windll
from PIL import Image, ImageTk
from pytube import YouTube
import os
import re 
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
  
class Application(tk.Frame):
    def __init__(self, master=None):
        self.master = master if master else tk.Tk()
        super().__init__(self.master)
        # Update master
        self.bg = "#2c2c2c"
        self.font = ('Helvetica', 8)
        self.master.title("Youtube2mp3")
        # Get image
        self.master.iconphoto(False, ImageTk.PhotoImage(Image.open(resource_path("yt2mp3.png"))))
        self.windowFrame = tk.Frame(self.master, bg=self.bg,highlightcolor=self.bg, highlightthickness=0)
        self.windowFrame.pack(side="bottom", fill="both", expand=True)
        self.i = 0
        self.create_widgets()
        
    def create_widgets(self):
        # Static Label and input
        self.label = tk.Label(self.windowFrame, text="Youtube Link:", font=self.font,fg='white', bg=self.bg,highlightcolor=self.bg, highlightthickness=0)
        self.input = tk.Entry(self.windowFrame)
        self.input.insert(0, "Insert link here...")
        self.input.bind('<FocusIn>', self.clear_input)
        
        # Buttons
        self.mp3_button = tk.Button(self.windowFrame)
        self.mp3_button["text"] = "mp3"
        self.mp3_button["command"] = self.yt2mp3_mp3
        
        self.opus_button = tk.Button(self.windowFrame)
        self.opus_button["text"] = "opus"
        self.opus_button["command"] = self.yt2mp3_opus
        
        # Variable Labels
        self.output_label = tk.Label(self.windowFrame, text="", fg='white', bg=self.bg,highlightcolor=self.bg, highlightthickness=0)
        self.output_warn = tk.Label(self.windowFrame, text="", fg='red', bg=self.bg,highlightcolor=self.bg, highlightthickness=0)
        
        self.label.grid(row=0, column=0, sticky="news")
        self.input.grid(row=0, column=1, sticky="news")
        self.mp3_button.grid(row=0, column=2, sticky="news")
        self.opus_button.grid(row=0, column=3, sticky="news")
        self.output_label.grid(row=1, column=0, columnspan=4, sticky="news")
        self.output_warn.grid(row=2, column=0, columnspan=4, sticky="news")
        
        
    def yt2mp3_mp3(self):
        self.youtube2mp3(codec_mp3=True)
    
    def yt2mp3_opus(self):
        self.youtube2mp3(codec_mp3=False)
        
    def youtube2mp3(self, codec_mp3:bool):
        url = self.input.get()
        try:
            yt = YouTube(url)
            title = yt.title
            
            self.output_warn.config(fg='green')
            self.output_warn["text"] = "Good Job!"
        except Exception:
            self.i=0
            self.output_warn.config(fg='red')
            self.output_warn["text"] = "This is not a youtube link!"
            return
        title = re.sub(r'[^\w\s]', '', title)
        filetype = ".mp3" if codec_mp3 else ".opus"

        filtered = yt.streams.filter(only_audio=True)
        # Create empty dict
        desired_streams = {}

        for stream in filtered:
            curr_codec = 'mp4' if 'mp4' in stream.codecs[0] else stream.codecs[0]
            curr_abr = int(str(stream.abr).replace('kbps', ''))
            curr_tag = int(stream.itag)
            if curr_codec not in desired_streams.keys():
                desired_streams[curr_codec] = curr_abr, curr_tag
            else:
                if curr_abr > desired_streams[curr_codec][0]:
                    desired_streams[curr_codec] = curr_abr, curr_tag

        if len(desired_streams) > 1:
            self.output_label["text"] = 'Multiple codecs found, selecting the one with highest quality:'
            id_to_download = 0
            for key,value in desired_streams.items():
                if key == 'mp4':
                    continue
                else:
                    curr_bitrate, curr_id = value
                    mp4_bitrate , mp4_id = desired_streams['mp4']
                    id_to_download = curr_id if curr_bitrate < mp4_bitrate*2 else mp4_id
        else:
            vals = desired_streams.values()
            id_to_download = list(vals)[0][1]
            # print(f'Downloading stream with id: {id_to_download}')

        self.output_label["text"] = f"Begining Download . . ."
        stream = yt.streams.get_by_itag(id_to_download)
        stream.download(filename=title.strip(" | ")+filetype)
        self.output_label["text"] = f"Downloaded [{title}] "
    
    def clear_input(self, event):
        self.input.delete(0, 'end')

    def print_input(self):
        self.output_label["text"] = self.input.get()

if __name__ == '__main__':
    app = Application()
    app.mainloop()
    
    #For turning into exe:
    # pyinstaller --onefile -w -F --add-binary "yt2mp3.png;." yt2mp3_v2.py
    