import tkinter as tk
import cv2
from PIL import ImageTk, Image
import numpy as numpy

from callbacks import display
from video_tk import VideoTk
from progress_bar import ProgressBar


def main():
    # Declaring main window.
    window = tk.Tk(className="Main Window")

    # Display box. ------------------------------------
    display_frame = tk.Frame(window)
    display_frame.pack(side=tk.RIGHT)
    # Video + panel widget.
    video = VideoTk("test.mp4")
    img = video.get_curr()
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(display_frame, image=img)
    panel.pack()
    # Slider buffer.
    print(video.n_frames)
    slider = tk.Scale(display_frame, length=video.shape[1], sliderlength=video.shape[1]/video.n_frames,
                      orient=tk.HORIZONTAL, from_=0, to=video.n_frames - 1)
    slider.pack()
    # Progress bar widget.
    progress_bar = ProgressBar(
        display_frame, 20, video.shape[1], video.n_frames)
    progress_bar.pack()

    # Options box. ------------------------------------
    options_frame = tk.Frame(window, width=100, bg="red")
    options_frame.pack(side=tk.LEFT, fill=tk.BOTH)

    # Binding callbacks.
    panel.bind("<Button-1>", lambda event,
               video=video, panel=panel, root=window, progress_bar=progress_bar, slider=slider:
               display.lclick_pressed(event, video, panel, root, progress_bar, slider))
    panel.bind("<ButtonRelease-1>",
               lambda event, progress_bar=progress_bar: display.lclick_released(event, progress_bar))
    panel.bind("<MouseWheel>", lambda event,
               video=video, panel=panel, slider=slider, n_frames_skip=5:
               display.scrolled(event, video, panel, slider, n_frames_skip))
    slider.bind("<ButtonRelease-1>", lambda event, video=video, panel=panel, slider=slider:
                display.dragged_slider(event, video, panel, slider))
    # Start main loop.
    window.mainloop()


if __name__ == "__main__":
    main()
