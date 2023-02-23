from .text import Text
from ..anchor import Anchor
from ..mainloop import MainLoop

class MovingText(Text):
	def __init__(self, text: str = "Moving Text", x: int = 0, y: int = 0, anchor: Anchor = Anchor.CENTER):
		super().__init__(text, x, y, anchor)

		MainLoop.On_Key_Press.subscribe(self.handle_movement)

	def handle_movement(self, key):
		if key == b'\x00\x4d':
			self.move(1, 0)
		elif key == b'\x00\x4b':
			self.move(-1, 0)
		elif key == b'\x00\x50':
			self.move(0, 1)
		elif key == b'\x00\x48':
			self.move(0, -1)