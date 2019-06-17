from PIL import ImageTk
import tkinter as tk
from video import Video
from time import sleep
from threading import Thread, Lock

DEBUG = True


def annotate_frame(video: Video, y_coordinate: int, lane_distances: list) -> None:
    # Annotate current frame.
    print(video.current.index, "y: ", y_coordinate)

    # Move to next frame.
    forward_frame


def cb_scroll(event: tk.Event, video: Video, panel: tk.Label) -> None:
    if event.delta > 0:
        forward_frame(video, panel)
    else:
        reverse_frame(video, panel)


def cb_lclick(event: tk.Event, video: Video, panel: tk.Label) -> None:
    if DEBUG:
        print("[{}]cb_forward_frame: Next Frame: {}" .format(
            video.current.index, video.current.next.index))
    forward_frame(video, panel)


def cb_rclick(event: tk.Event, video: Video, panel: tk.Label) -> None:
    if DEBUG:
        print("[{}]cb_reverse_frame: Next Frame: {}" .format(
            video.current.index, video.current.prev.index))
    reverse_frame(video, panel)


def forward_frame(video: Video, panel: tk.Label) -> None:
    next_frame = video.get_next()
    next_frame = ImageTk.PhotoImage(next_frame)
    panel.configure(image=next_frame)
    panel.image = next_frame


def reverse_frame(video: Video, panel: tk.Label) -> None:
    prev_frame = video.get_prev()
    prev_frame = ImageTk.PhotoImage(prev_frame)
    panel.configure(image=prev_frame)
    panel.image = prev_frame
