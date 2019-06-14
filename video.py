import cv2
from PIL import Image, ImageTk

# Node to hold each frame in the doubly-linked list.


class VideoNode:
    def __init__(self, frame: ImageTk.PhotoImage):
        self.frame = frame
        self.next = None
        self.prev = None


# Doubly-Linked list to hold video.
class Video:
    def __init__(self, path: str):
        # Use video file to create doubly-linked list
        self.video_file = cv2.VideoCapture(path)
        self.head = None
        self.tail = None
        self.n_frames = 0

        total_n_frames = int(self.video_file.get(cv2.CAP_PROP_FRAME_COUNT))

        # Convert video file into doubly-linked list.
        for _ in range(total_n_frames):
            self._append(self._get_frame())
            self.n_frames += 1
        # Check if file converted successfully.
        if self.n_frames != total_n_frames:
            print("There was some error in reading the file")
            print("Video File Frames: {}, Video Object Frames: {}"
                  .format(total_n_frames, self.n_frames))
        # Free video file.
        self.video_file.release()

    def _append(self, frame: ImageTk.PhotoImage) -> None:
        node = VideoNode(frame)
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.prev = self.head
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def _get_frame(self) -> ImageTk.PhotoImage:
        success, frame = self.video_file.read()

        if not success:
            print("video(get_frame): End of Video!")
            return None

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        return img
