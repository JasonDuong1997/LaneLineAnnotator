import tkinter as tk
import cv2
from PIL import ImageTk, Image
import numpy as numpy

from callbacks import display
from video import Video


def main():
    # Declaring main window.
    window = tk.Tk(className="Main Window")

    # Read in video.
    video = Video("test.mp4")

    # Declaring widgets.
    img = video.get_curr()
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(window, image=img)
    panel.pack()

    # Binding callbacks.
    panel.bind("<Button-1>", lambda event,
               video=video, panel=panel, root=window: display.lclick_pressed(event, video, panel, root))
    panel.bind("<ButtonRelease-1>",
               lambda event: display.lclick_released(event))
    panel.bind("<MouseWheel>", lambda event,
               video=video, panel=panel, n_frames_skip=5: display.scrolled(event, video, panel, n_frames_skip))
    # Start main loop.
    window.mainloop()


if __name__ == "__main__":
    main()
