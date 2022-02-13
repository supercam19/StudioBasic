# Backend for Studio Basic
# By: Cameron Labelle
# Date: 01/17/2022

from moviepy.editor import *
import moviepy.video.fx.all as vfx
from tkinter.filedialog import asksaveasfilename
import main
from re import split


def load_video(video_path):
    """
    Loads the video at the start of the program
    """
    global clip
    try:
        clip = VideoFileClip(video_path)
    except OSError:
        exit()
    return clip


def get_current_clip():
    """
    Gets the current clip with its changes applied
    Called upon video replay
    """
    global clip
    return clip


def get_vital_widgets(frame):
    """
    Used to pass vital objects into the backend
    Necessary for logging
    """
    global logging_frame
    logging_frame = frame


def export(ex_format):
    """
    Exports the video
    Uses selected format from dropdown to determine how to export
    """
    global clip
    # If no format was selected, default to .mp4
    if ex_format == "Choose Format":
        ex_format = '.mp4'
    # Prompts the user where to save the video
    file_path = asksaveasfilename(filetypes=[("Video files", ".mp4 .mov .gif")], initialfile='MyVideo' + ex_format)
    # Gifs need to be exported differently than .mp4 or .mov
    if not ex_format == '.gif':
        main.log("Video Processing", logging_frame)
        clip.write_videofile(file_path)
        main.log("Video Exported", logging_frame)
    else:
        main.log("Video Processing", logging_frame)
        clip.write_gif(file_path)
        main.log("Video Exported", logging_frame)


def is_valid_input(input):
    """
    Checks if the value in the speed changes textboxes are valid input
    """
    try:
        float(input)
    except ValueError:
        return False
    return True


def apply_speed_changes(multiplier, fps):
    """
    Apply the video speed multiplier and framerate changes
    """
    global clip
    if is_valid_input(multiplier):
        clip = vfx.speedx(clip, float(multiplier))
        main.log("Speed Changed", logging_frame)
    if is_valid_input(fps):
        clip = clip.set_fps(float(fps))
        main.log("Framerate Changed", logging_frame)
    # Log if error
    if not is_valid_input(multiplier) and multiplier != "": main.log("Speed Failed", logging_frame)
    if not is_valid_input(fps) and fps != "": main.log("Framerate Failed", logging_frame)


def apply_trim_changes(start_pos, end_pos, start_label, end_label):
    """
    Applies video trim
    Creates a subclip starting at the start_pos and ending at the end_pos
    """
    global clip, logging_frame
    success = True
    # Tries to create the float for start and end time of clip, if fails then alert user
    try:
        start_time = split('\:|\.', start_pos)
        start_time_float = float(start_time[0]) * 60 + float(start_time[1]) + float(start_time[2]) / 100
    except:
        start_label['bg'] = 'red'
        main.log("Invalid Start Pos", logging_frame)
        success = False
    
    try:
        end_time = split('\:|\.', end_pos)
        end_time_float = float(end_time[0]) * 60 + float(end_time[1]) + float(end_time[2]) / 100
    except:
        end_label['bg'] = 'red'
        main.log("Invalid End Pos", logging_frame)
        success = False

    # Runs code if the start and end time are valid
    if success:
        clip = clip.subclip(start_time_float, end_time_float)
        main.log("Video Trimmed", logging_frame)
        start_label['bg'] = 'white'
        end_label['bg'] = 'white'


def get_clip_duration():
    """
    Gets the duration of the clip and converts it into
    min:sec.ms
    """
    global clip
    duration = clip.duration
    # Calculates minutes, seconds and miliseconds length of video
    duration_S = int(duration)
    duration_ms = duration - duration_S
    duration_ms *= 100
    duration_ms = int(duration_ms)
    duration_min = duration_S // 60
    duration_sec = duration % 60
    duration_sec = int(duration_sec)
    # If the number is 1 digit long, adds a zero in front of it
    if len(str(duration_sec)) == 1: duration_sec = '0' + str(duration_sec)
    if len(str(duration_min)) == 1: duration_min = '0' + str(duration_min)
    if len(str(duration_ms)) == 1: duration_ms = '0' + str(duration_ms)
    return f"{str(duration_min)}:{str(duration_sec)}.{str(duration_ms)}"
