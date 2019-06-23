from PIL import Image, ImageTk
import tkinter as tk
from video_tk import VideoTk
from time import sleep
from threading import Thread, Lock
from progress_bar import ProgressBar

DEBUG = True

forwarding = False
lock_display = Lock()

# UTILITIES


def _display_frame(frame: Image, panel: tk.Label) -> None:
    frame = ImageTk.PhotoImage(frame)
    panel.configure(image=frame)
    panel.image = frame


def _forward_frame(video: VideoTk, panel: tk.Label, slider: tk.Scale) -> None:
    slider.set(video.current.index)
    next_frame = video.get_next()
    _display_frame(next_frame, panel)


def _reverse_frame(video: VideoTk, panel: tk.Label) -> None:
    prev_frame = video.get_prev()
    _display_frame(prev_frame, panel)


def _jump_to_frame(video: VideoTk, panel: tk.Label, slider: tk.Scale, dest_frame: int) -> None:
    n_frames_skip = dest_frame - video.current.index
    if n_frames_skip > 0:
        for _ in range(n_frames_skip):
            video.move_next()
    elif n_frames_skip < 0:
        for _ in range(abs(n_frames_skip)):
            video.move_prev()
    frame_current = video.get_curr()
    _display_frame(frame_current, panel)
    slider.set(video.current.index)


def _annotate_frame(video: VideoTk, y_coordinate: float, lane_distances: list, progress_bar: ProgressBar) -> None:
    if y_coordinate < 0.0:
        y_coordinate = 0.0
    elif y_coordinate > 1.0:
        y_coordinate = 1.0
    y_coordinate = round(y_coordinate, 2)
    print("[", video.current.index, "]: ", "height = ", y_coordinate)
    progress_bar.add_progress(video.current.index)


def _annotate_loop(event: tk.Event, video: VideoTk, panel: tk.Label, root: tk.Tk, progress_bar: ProgressBar, slider: tk.Scale) -> None:
    with lock_display:
        if forwarding:
            mouse_rel_y = (
                video.shape[0] - (panel.winfo_pointery() - panel.winfo_rooty()))/video.shape[0]
            _annotate_frame(video, mouse_rel_y, [], progress_bar)
            _forward_frame(video, panel, slider)
            root.after(1, _annotate_loop, event, video,
                       panel, root, progress_bar, slider)


def lclick_pressed(event: tk.Event, video: VideoTk, panel: tk.Label, root: tk.Tk, progress_bar: tk.Canvas, slider: tk.Scale) -> None:
    global forwarding

    with lock_display:
        forwarding = True
    _annotate_loop(event, video, panel, root, progress_bar, slider)


def lclick_released(event: tk.Event, progress_bar: ProgressBar) -> None:
    global forwarding

    with lock_display:
        forwarding = False
    progress_bar.is_complete()


def rclick_pressed(event: tk.Event, video: VideoTk, panel: tk.Label) -> None:
    if DEBUG:
        print("[{}]cb_reverse_frame: Next Frame: {}" .format(
            video.current.index, video.current.prev.index))
    _reverse_frame(video, panel)


def scrolled(event: tk.Event, video: VideoTk, panel: tk.Label, slider: tk.Scale, n_frames_skip: int = 1) -> None:
    if event.delta > 0:
        for _ in range(n_frames_skip):
            video.move_next()
    else:
        for _ in range(n_frames_skip):
            video.move_prev()
    frame_current = video.get_curr()
    _display_frame(frame_current, panel)
    slider.set(video.current.index)


def dragged_slider(event: tk.Event, video: VideoTk, panel: tk.Label, slider: tk.Scale) -> None:
    dest_frame = slider.get()
    _jump_to_frame(video, panel, slider, dest_frame)
