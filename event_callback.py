from PIL import ImageTk
import tkinter as tk
from video import Video


def annotate_frame(event: tk.Event, video: Video, panel: tk.Label) -> None:
    next_frame = video.get_next()
    next_frame = ImageTk.PhotoImage(next_frame)
    panel.configure(image=next_frame)
    panel.image = next_frame


def forward_frame(event: tk.Event, video: Video, panel: tk.Label) -> None:
    next_frame = video.get_next()
    next_frame = ImageTk.PhotoImage(next_frame)
    panel.configure(image=next_frame)
    panel.image = next_frame


def reverse_frame(event: tk.Event, video: Video, panel: tk.Label) -> None:
    prev_frame = video.get_prev()
    prev_frame = ImageTk.PhotoImage(prev_frame)
    panel.configure(image=prev_frame)
    panel.image = prev_frame
