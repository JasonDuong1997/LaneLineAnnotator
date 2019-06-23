import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time

DEBUG = True

# Node to hold each frame in the doubly-linked list.


class VideoTkNode:
    def __init__(self, frame: Image, index: int):
        self.frame = frame
        self. index = index
        self.next = None
        self.prev = None


# Doubly-Linked list to hold video.
class VideoTk:
    def __init__(self, path: str):
        global DEBUG

        start_time = 0
        if DEBUG:
            print("video: Creating Video Object...")
            start_time = time.time()

        # Use video file to create doubly-linked list
        self.video_file = cv2.VideoCapture(path)
        self.head = None
        self.current = None
        self.tail = None
        self.n_frames = 0
        self.shape = (0, 0,)  # height, width

        # Convert video file into doubly-linked list.
        total_n_frames = int(self.video_file.get(cv2.CAP_PROP_FRAME_COUNT))
        for i in range(total_n_frames):
            self._append(self._get_frame(), i)
            self.n_frames += 1
        # Check if file converted successfully.
        if self.n_frames != total_n_frames:
            print("There was some error in reading the file")
            print("Video File Frames: {}, Video Object Frames: {}"
                  .format(total_n_frames, self.n_frames))
        self.current = self.head
        if DEBUG:
            elapsed_time = round(time.time() - start_time, 2)
            print("video: Elapsed time: {} s"
                  .format(elapsed_time))
            # Free video file.
        self.video_file.release()

    ### Public Functions ###
    def get_prev(self) -> Image:
        if self.current.prev:
            self.current = self.current.prev
            return self.current.frame
        else:
            return self.current.frame

    def get_curr(self) -> Image:
        return self.current.frame

    def get_next(self) -> Image:
        if self.current.next:
            self.current = self.current.next
            return self.current.frame
        else:
            return self.current.frame

    def move_next(self) -> None:
        if self.current.next:
            self.current = self.current.next

    def move_prev(self) -> None:
        if self.current.prev:
            self.current = self.current.prev

    ### Private Functions ###

    def _append(self, frame: Image, index: int) -> None:
        node = VideoTkNode(frame, index)
        if self.head:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        else:
            self.head = node
            self.tail = node
            # update height, width
            self.shape = (node.frame.height, node.frame.width)

    def _get_frame(self) -> Image:
        success, frame = self.video_file.read()
        if not success:
            print("video(get_frame): End of Video!")
            return None
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        return img
