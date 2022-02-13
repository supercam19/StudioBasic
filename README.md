# StudioBasic
 A small GUI-based video editor made in python with moviepy for a school project.

## Installation

 Requires python 3

 Download the zip file [here](https://www.github.com/supercam19/StudioBasic/releases). Extract the zip file once downloaded.

 Requirements:
  - moviepy (pip install moviepy)
  - Pillow (pip install PIL)
  - [ffmpeg](https://ffmpeg.org/download.html)

 If ffmpeg is not in your path, you can set the location by uncommenting line 5 and 6 in main.py and changing the file path string on line 6. You can also set it like you would set any other environment variable.

## Using the program
 
 To use the program run the main.py file directly. A window will pop up to prompt you to select a video file.

 ### Index:

  **Export button**
   * Exports the video with any edits made
   * Select an export format before exporting, else it will default to .mp4

  **Speed button**
   * Changes the speed/framerate of the video
   * Enter the desired values in the textboxes and press 'Apply'

  **Trim button**
   * Changes the start and end time of the video
   * Timestamps must be formatted properly, eg:
     * 01:35.16 (min:sec.ms)
   * The default values in the textboxes can be referenced for how to properly format the timestamp
   * If the timestamp is not properly formatted, the textbox will turn red and a log will be created to indicate it failed
   * The 'Apply' button must be pressed to apply the changes

  **Logs**
   * The logs are used to indicate whether or not a task was successful
   * Logs will appear on the left side of the window once needed

  **Pause/Restart buttons**
   * The pause button will pause the video player
   * The restart button will replay the video in the video player with all changes applied