from PIL import ImageTk
import tkinter as tk
from video import Video
from time import sleep
from threading import Thread, Lock

DEBUG = True

forwarding = False
lock_display = Lock()

# UTILITIES


def _forward_frame(video: Video, panel: tk.Label) -> None:
    next_frame = video.get_next()
    next_frame = ImageTk.PhotoImage(next_frame)
    panel.configure(image=next_frame)
    panel.image = next_frame


def _reverse_frame(video: Video, panel: tk.Label) -> None:
    prev_frame = video.get_prev()
    prev_frame = ImageTk.PhotoImage(prev_frame)
    panel.configure(image=prev_frame)
    panel.image = prev_frame


def _annotate_frame(video: Video, y_coordinate: float, lane_distances: list) -> None:
    if y_coordinate < 0.0:
        y_coordinate = 0.0
    elif y_coordinate > 1.0:
        y_coordinate = 1.0
    y_coordinate = round(y_coordinate, 2)
    print("[", video.current.index, "]: ", "height = ", y_coordinate)

# CALLBACKS


def _annotate_loop(event: tk.Event, video: Video, panel: tk.Label, root: tk.Tk) -> None:
    with lock_display:
        if forwarding:
            mouse_rel_y = (
                video.shape[0] - (panel.winfo_pointery() - panel.winfo_rooty()))/video.shape[0]
            _annotate_frame(video, mouse_rel_y, [])
            _forward_frame(video, panel)
            root.after(1, _annotate_loop, event, video, panel, root)


def cb_lclick_pressed(event: tk.Event, video: Video, panel: tk.Label, root: tk.Tk) -> None:
    global forwarding

    with lock_display:
        forwarding = True
    _annotate_loop(event, video, panel, root)


def cb_lclick_released(event: tk.Event) -> None:
    global forwarding

    if DEBUG:
        print("Ending annotation loop")
    with lock_display:
        forwarding = False


def cb_rclick_pressed(event: tk.Event, video: Video, panel: tk.Label) -> None:
    if DEBUG:
        print("[{}]cb_reverse_frame: Next Frame: {}" .format(
            video.current.index, video.current.prev.index))
    _reverse_frame(video, panel)


def cb_scrolled(event: tk.Event, video: Video, panel: tk.Label) -> None:
    if event.delta > 0:
        _forward_frame(video, panel)
    else:
        _reverse_frame(video, panel)
