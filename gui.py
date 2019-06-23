import tkinter as tk
import cv2
from PIL import ImageTk, Image
import numpy as numpy

from callbacks import display
from video_tk import VideoTk


def main():
    # Declaring main window.
    window = tk.Tk(className="Main Window")

    # Read in video.
    video = VideoTk("test.mp4")

    # Declaring widgets.
    img = video.get_curr()
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(window, image=img)
    panel.pack()

    progress_bar = tk.Canvas(
        window, height=20, width=video.shape[1], bg="grey", relief=tk.SUNKEN)
    progress_bar.pack()

    # Binding callbacks.
    panel.bind("<Button-1>", lambda event,
               video=video, panel=panel, root=window, progress_bar=progress_bar: display.lclick_pressed(event, video, panel, root, progress_bar))
    panel.bind("<ButtonRelease-1>",
               lambda event: display.lclick_released(event))
    panel.bind("<MouseWheel>", lambda event,
               video=video, panel=panel, n_frames_skip=5: display.scrolled(event, video, panel, n_frames_skip))
    # Start main loop.
    window.mainloop()


if __name__ == "__main__":
    main()
