import tkinter as tk

DEBUG = True


class ProgressBar(object):
    def __init__(self, root: tk.Tk, height: int, width: int, n_slices: int):
        self.height = height
        self.width = width
        self.n_slices = n_slices
        self.slice_width = width/n_slices
        self.slices_annotated = [False for _ in range(self.n_slices)]
        self.bar = tk.Canvas(root, height=self.height, width=self.width,
                             bg="grey", relief=tk.SUNKEN)

    def pack(self) -> None:
        self.bar.pack()

    def _get_slice_rect(self, slice: int) -> tuple:
        return (slice*self.slice_width, 0, (slice+1)*self.slice_width, self.height,)

    def add_progress(self, slice: int) -> None:
        if not self.slices_annotated[slice]:
            coords = self._get_slice_rect(slice)
            self.bar.create_rectangle(
                coords[0], coords[1], coords[2], coords[3], fill="green")
            self.slices_annotated[slice] = True

    def is_complete(self) -> bool:
        if False not in self.slices_annotated:
            if DEBUG:
                print("ProgressBar(is_complete): Finished annotating!")
            return True
        else:
            return False
