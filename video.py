import cv2
from PIL import Image, ImageTk
import time

DEBUG = True

# Node to hold each frame in the doubly-linked list.


class VideoNode:
    def __init__(self, frame: Image, index: int):
        self.frame = frame
        self. index = index
        self.next = None
        self.prev = None


# Doubly-Linked list to hold video.
class Video:
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

        total_n_frames = int(self.video_file.get(cv2.CAP_PROP_FRAME_COUNT))

        # Convert video file into doubly-linked list.
        for i in range(total_n_frames):
            self._append(self._get_frame(), i)
            self.n_frames += 1
        # Check if file converted successfully.
        if self.n_frames != total_n_frames:
            print("There was some error in reading the file")
            print("Video File Frames: {}, Video Object Frames: {}"
                  .format(total_n_frames, self.n_frames))

        if DEBUG:
            elapsed_time = round(time.time() - start_time, 2)
            print("video: Elapsed time: {} s"
                  .format(elapsed_time))
            # Free video file.
        self.video_file.release()

    ### Public Functions ###
    def get_next(self) -> Image:
        if self.current:
            self.current = self.current.next
            return self.current.frame
        else:
            self.current = self.head
            return self.current.frame

    def get_prev(self) -> Image:
        if self.current:
            self.current = self.current.prev
            return self.current.frame
        else:
            self.current = self.tail
            return self.current.frame

    ### Private Functions ###
    def _append(self, frame: Image, index: int) -> None:
        node = VideoNode(frame, index)
        if self.head:
            self.tail.prev = self.head
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        else:
            self.head = node
            self.tail = node

    def _get_frame(self) -> Image:
        success, frame = self.video_file.read()

        if not success:
            print("video(get_frame): End of Video!")
            return None

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        return img
