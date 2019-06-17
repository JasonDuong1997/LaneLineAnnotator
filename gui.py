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
    panel.bind("<Button-1>", lambda event,
               video=video, panel=panel: cb_lclick(event, video, panel))
    panel.bind("<MouseWheel>", lambda event,
               video=video, panel=panel: cb_scroll(event, video, panel))
    # Start main loop.
    window.mainloop()


if __name__ == "__main__":
    main()
