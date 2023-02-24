import time

from .text import Text
from ..anchor import Anchor
from ..mainloop import MainLoop
from ..renderable import Renderable

class Timer(Text):
	def __init__(self, master: Renderable, label: str = "{:0.2f}", x: int = 0, y: int = 0, anchor: Anchor = Anchor.CENTER):
		super().__init__(master, label, x, y, anchor)

		self.label = label
		self.start_time = time.time()

	def render(self):
		self.set_text(self.label.format(time.time() - self.start_time))
		super().render()