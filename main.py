# Studio Basic video editor
# By: Cameron Labelle
# Date: 01/17/2022

#import os
#os.environ["FFMPEG_BINARY"] = "P:/ffmpeg/bin/ffmpeg.exe"

import tkinter as tk, tkvideo
from tkinter import filedialog
from time import sleep

FONT = ("Arial", 20)
video_playing = True
loaded_menu = 'none'
log_count = 0


def main(window):
    global log_count
    # Updates the visuals of the pause/play button
    def play_button_update():
        global video_playing
        if video_playing:
            video_playing = False
            pause_button['text'] = '\u23F5'
        else:
            video_playing = True
            pause_button['text'] = '\u23F8'
        player.update_video_play_state(video_playing)

    def replay_video(player):
        player.send_thread_kill_command()
        player = tkvideo.TkVideo(backend.get_current_clip(), video_label, loop=1, size=(500, 300), hz=clip.fps)
        player.play()

    # Create the frame on the right of the window
    Rmaster_frame.pack_propagate(0)
    Rmaster_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    
    Lmaster_frame.pack_propagate(0)
    Lmaster_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    
    # Frame that holds the video
    video_frame = tk.Frame(master=Rmaster_frame, width=500, height=300, bg='gray')
    video_frame.pack_propagate(0)
    video_frame.pack(side=tk.TOP, anchor='n', padx=5, expand=False)

    # Loads the video (video is a Label)
    video_label = tk.Label(video_frame)
    video_label.pack(side=tk.RIGHT, anchor="n", pady=10, padx=10)
    player = tkvideo.TkVideo(clip, video_label, loop=1, size=(500, 300), hz=clip.fps)
    player.play()

    # Widget definitions and packing
    video_control_frame = tk.Frame(master=Rmaster_frame)
    video_control_frame.pack()

    replay_button = tk.Button(master=video_control_frame, text='\u21BB', font=("Arial", 15), highlightthickness=0, bd=0, command=lambda: replay_video(player))
    replay_button.pack(side=tk.LEFT)

    pause_button = tk.Button(master=video_control_frame, text='\u23F8', font=("Arial", 15), highlightthickness=0, bd=0, command=play_button_update)
    pause_button.pack(side=tk.LEFT)
    
    button_frame = tk.Frame(master=Lmaster_frame, height=250, width=100, bg="gray")
    button_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    
    logging_frame.pack_propagate(0)
    logging_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

    export_button = tk.Button(master=button_frame, text="Export", font=FONT, command=export_window)
    export_button.pack(side=tk.TOP, padx=5, pady=5)
    
    speed_button = tk.Button(master=button_frame, text="Speed", font=FONT, command=lambda: load_speed_menu(control_frame))
    speed_button.pack(side=tk.TOP, padx=5, pady=5)
    
    trim_button = tk.Button(master=button_frame, text=" Trim ", font=FONT, command=lambda: load_trim_menu(control_frame))
    trim_button.pack(side=tk.TOP, padx=5, pady=5)

    control_frame.pack_propagate(0)
    control_frame.pack(side=tk.TOP, anchor='s', expand=False)

    log_count = 1
    log("Editor Started", logging_frame)
    # Creates the tkinter window thread and closes the clip when done
    window.mainloop()
    clip.close()


def export_window():
    # Creates the export window
    window = tk.Tk()
    window.geometry("200x200")
    window.title("Studio Basic - Export")
    
    # The list of options for the dropdown menu
    export_options = [".mp4", ".mov", ".gif"]
    
    # Sets what the default option is in the dropdown menu (Choose Format)
    clicked = tk.StringVar(window)
    clicked.set("Choose Format")
    
    # Creates and packs the dropdown menu
    format_dropdown = tk.OptionMenu(window, clicked, *export_options)
    format_dropdown.pack(side=tk.TOP, pady=10)
    
    # Creates and packs the export button
    export_button = tk.Button(window, text="Export", font=FONT, command=lambda: backend.export(clicked.get()))
    export_button.pack(side=tk.BOTTOM, pady=10)

    window.mainloop()
    

def log(msg, frame):
    global log_count
    if log_count % 2 == 0: colour = 'lavender'
    else: colour = 'lightgray'
    new_frame = tk.Frame(master=frame, bg=colour, height=19)
    new_frame.pack_propagate(0)
    new_frame.pack(side=tk.TOP, fill=tk.X, expand=False, padx=5)
    new_log = tk.Label(master=new_frame, text=msg, font=("Arial", 11), justify=tk.LEFT, bg=colour)
    new_log.pack(anchor='w')
    log_count += 1
    

def create_frames(frame, frame_count):
    frame_list = []
    for i in range(frame_count):
        frame_list.append(tk.Frame(master=frame, width=200, height=20, bg='lightgray'))
        frame_list[i].pack_propagate(0)
        frame_list[i].pack(side=tk.TOP, pady=5, expand=False, anchor='w')
    return frame_list
    

def load_speed_menu(frame):
    global loaded_menu
    font = ("Arial", 10)
    
    if loaded_menu != 'speed':
        for child in control_frame.winfo_children():
            child.destroy()

        frame_list = create_frames(frame, 2)
        
        speed_multiplier_label = tk.Label(master=frame_list[0], font=font, text="Video Speed Multiplier: ", bg='lightgray')
        speed_multiplier_label.pack(side=tk.LEFT)
        
        speed_multiplier_textbox = tk.Entry(master=frame_list[0], font=font)
        speed_multiplier_textbox.pack(side=tk.LEFT)
        
        frame_rate_label = tk.Label(master=frame_list[1], font=font, text="Video Frame Rate:       ", bg='lightgray')
        frame_rate_label.pack(side=tk.LEFT)
        
        frame_rate_textbox = tk.Entry(master=frame_list[1], font=font)
        frame_rate_textbox.pack(side=tk.RIGHT)
        
        apply_button = tk.Button(master=frame, text='Apply', font=("Arial", 15), command=lambda: backend.apply_speed_changes(speed_multiplier_textbox.get(), frame_rate_textbox.get()))
        apply_button.pack(side=tk.BOTTOM, pady=5)
    loaded_menu = 'speed'
    

def load_trim_menu(frame):
    global loaded_menu, clip
    font = ("Arial", 10)
    
    if loaded_menu != "trim":
        for child in control_frame.winfo_children():
            child.destroy()

        frame_list = create_frames(frame, 2)

        video_start_label = tk.Label(master=frame_list[0], font=font, text="Video Start Time: ", bg='lightgray')
        video_start_label.pack(side=tk.LEFT)
        
        video_start_textbox = tk.Entry(master=frame_list[0], font=font)
        video_start_textbox.pack(side=tk.LEFT)
        video_start_textbox.insert(0, "00:00.00")
        
        video_end_label = tk.Label(master=frame_list[1], font=font, text="Video End Time:   ", bg='lightgray')
        video_end_label.pack(side=tk.LEFT)
        
        video_end_textbox = tk.Entry(master=frame_list[1], font=font)
        video_end_textbox.pack(side=tk.RIGHT)
        video_end_textbox.insert(0, backend.get_clip_duration())

        apply_button = tk.Button(master=frame, text='Apply', font=("Arial", 15), command=lambda: backend.apply_trim_changes(video_start_textbox.get(), video_end_textbox.get(), video_start_textbox, video_end_textbox))
        apply_button.pack(side=tk.BOTTOM, pady=5)
    
    loaded_menu = 'trim'


if __name__ == '__main__':
    import backend
    # Create Window
    window = tk.Tk()
    window.geometry("800x500")
    window.title("Studio Basic")
    window.resizable(False, False)
    
    # Loading screen
    text_label = tk.Label(master=window, text="Loading your video, please wait.", font=FONT)
    text_label.pack(pady=180)

    # Prompts user for video file input - loads it
    video_path = filedialog.askopenfilename(filetypes=[("Video files", ".mp4 .mov .gif")])    
    clip = backend.load_video(video_path)
    
    # Unloads the loading screen
    text_label.pack_forget()
    # Creates frames that need to be global variables
    Rmaster_frame = tk.Frame(master=window, width=530)
    control_frame = tk.Frame(master=Rmaster_frame, width=500, height=150, bg='lightgray')
    Lmaster_frame = tk.Frame(master=window, width=270)
    logging_frame = tk.Frame(master=Lmaster_frame, width=150)
    backend.get_vital_widgets(logging_frame)
    # Unfocuses and refocuses the window so that the entry boxes work
    window.overrideredirect(True)
    window.overrideredirect(False)
    main(window)

