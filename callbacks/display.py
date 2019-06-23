from PIL import Image, ImageTk
import tkinter as tk
from video_tk import VideoTk
from time import sleep
from threading import Thread, Lock

DEBUG = True

forwarding = False
lock_display = Lock()

# UTILITIES


def _get_progress_bar_partition(partition: int, bar_width: int, bar_height: int, n_partitions: int) -> tuple:
    slice_width = bar_width/n_partitions
    return (partition*slice_width, 0, (partition+1)*slice_width, bar_height,)


def _update_progress_bar(progress_bar: tk.Canvas, video: VideoTk):
    coords = _get_progress_bar_partition(
        video.current.index, video.shape[1], 20, video.n_frames)
    progress_bar.create_rectangle(
        coords[0], coords[1], coords[2], coords[3], fill="green")


def _display_frame(frame: Image, panel: tk.Label) -> None:
    frame = ImageTk.PhotoImage(frame)
    panel.configure(image=frame)
    panel.image = frame


def _forward_frame(video: VideoTk, panel: tk.Label) -> None:
    next_frame = video.get_next()
    _display_frame(next_frame, panel)


def _reverse_frame(video: VideoTk, panel: tk.Label) -> None:
    prev_frame = video.get_prev()
    _display_frame(prev_frame, panel)


def _annotate_frame(video: VideoTk, y_coordinate: float, lane_distances: list, progress_bar: tk.Canvas) -> None:
    if y_coordinate < 0.0:
        y_coordinate = 0.0
    elif y_coordinate > 1.0:
        y_coordinate = 1.0
    y_coordinate = round(y_coordinate, 2)
    print("[", video.current.index, "]: ", "height = ", y_coordinate)
    _update_progress_bar(progress_bar, video)


def _annotate_loop(event: tk.Event, video: VideoTk, panel: tk.Label, root: tk.Tk, progress_bar: tk.Canvas) -> None:
    with lock_display:
        if forwarding:
            mouse_rel_y = (
                video.shape[0] - (panel.winfo_pointery() - panel.winfo_rooty()))/video.shape[0]
            _annotate_frame(video, mouse_rel_y, [], progress_bar)
            _forward_frame(video, panel)
            root.after(1, _annotate_loop, event, video,
                       panel, root, progress_bar)


def lclick_pressed(event: tk.Event, video: VideoTk, panel: tk.Label, root: tk.Tk, progress_bar: tk.Canvas) -> None:
    global forwarding

    with lock_display:
        forwarding = True
    _annotate_loop(event, video, panel, root, progress_bar)


def lclick_released(event: tk.Event) -> None:
    global forwarding

    if DEBUG:
        print("Ending annotation loop")
    with lock_display:
        forwarding = False


def rclick_pressed(event: tk.Event, video: VideoTk, panel: tk.Label) -> None:
    if DEBUG:
        print("[{}]cb_reverse_frame: Next Frame: {}" .format(
            video.current.index, video.current.prev.index))
    _reverse_frame(video, panel)


def scrolled(event: tk.Event, video: VideoTk, panel: tk.Label, n_frames_skip: int = 1) -> None:
    if event.delta > 0:
        for _ in range(n_frames_skip):
            video.move_next()
    else:
        for _ in range(n_frames_skip):
            video.move_prev()
    frame_current = video.get_curr()
    _display_frame(frame_current, panel)
