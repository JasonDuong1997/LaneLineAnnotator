import tkinter as tk
import cv2
from PIL import ImageTk, Image
import numpy as numpy
from event_callback import *

from video import Video


def test():
    print("test")


def test2(event: tk.Event):
    print(event.x, event.y)


def image_read(path: str):
    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
    return ImageTk.PhotoImage(Image.fromarray(img))


def main():
    # Initializing Tkinter.
    # root = tk.Tk()

    # Read in video.
    video = Video("test.mp4")

    # Declaring main window.
    window = tk.Tk(className="Main Window")

    # Declaring widgets.
    button = tk.Button(window, text="test",)
    button.pack()

    img = video.get_next()
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(window, image=img)
    panel.pack()

    # Binding callbacks.
    button.bind("<Button-1>", test2)
    panel.bind("<Button-1>", lambda event,
               video=video,  panel=panel: annotate_frame(event, video, panel))
    panel.bind("<B1-Motion>", lambda event,
               video=video, panel=panel: annotate_frame(event, video, panel))
    panel.bind("<Button-4>", lambda event,
               video=video, panel=panel: forward_frame(event, video, panel))
    panel.bind("<B2-Pressed>", lambda event,
               video=video, panel=panel: reverse_frame(event, video, panel))
    # Start main loop.
    window.mainloop()


if __name__ == "__main__":
    main()
