from .text import Text
from ..anchor import Anchor
from ..mainloop import MainLoop

class KeyDisplay(Text):
	def __init__(self, label: str = "0x{}", x: int = 0, y: int = 0, anchor: Anchor = Anchor.CENTER, default_text: str = None):
		if default_text == None:
			default_text = label.format("00")

		super().__init__(default_text, x, y, anchor)

		self.label = label
		MainLoop.On_Key_Press.subscribe(self.on_press_callback)

	def on_press_callback(self, key):
		self.set_text(self.label.format(key.hex()))