import time

from .text import Text
from ..anchor import Anchor
from ..mainloop import MainLoop

class Timer(Text):
	def __init__(self, label: str = "{:0.2f}", x: int = 0, y: int = 0, anchor: Anchor = Anchor.CENTER):
		super().__init__(label, x, y, anchor)

		self.label = label
		self.start_time = time.time()

		MainLoop.On_Main_Loop.subscribe(self.tick)

	def tick(self):
		self.set_text(self.label.format(time.time() - self.start_time))