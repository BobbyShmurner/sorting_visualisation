from .text import Text
from ..anchor import Anchor
from ..mainloop import MainLoop
from ..events import Event
from ..prelude import *

from typing import Callable

class InputField(Text):
	Current_input: 'Text' = None

	def __init__(self, label: str = "{}", x: int = 0, y: int = 0, anchor: Anchor = Anchor.CENTER, validate: Callable[[bytes], bool] = None):
		self.data = ""
		self.typing = False
		self.validate = validate if (validate != None) else self.basic_validate

		self.on_stop_input = Event()

		super().__init__(label, x, y, anchor)

		self.set_text(label)

	def get_input(self):
		if self.__class__.Current_input != None:
			self.__class__.Current_input.stop_input()

		MainLoop.On_Key_Press.subscribe(self.on_key_press_callback)

		self.__class__.Current_input = self
		self.typing = True
		self.data += ' '
		show_cursor()

		self.set_text()
		self.update_cursor()

	def stop_input(self):
		self.__class__.Current_input = None
		self.typing = False
		self.data  = self.data[:-1]

		MainLoop.On_Key_Press.unsubscribe(self.on_key_press_callback)

		self.set_text()
		hide_cursor()

		self.on_stop_input.invoke()

	def basic_validate(self, key: bytes) -> bool:
		return key != b'\x09' and not key.startswith(b'\x00')

	def set_text(self, label: str = None):
		if (label != None):
			self.label = label
			self.set_format_location()

		super().set_text(self.label.format(self.data))

	def set_format_location(self):
		for y, line in enumerate(self.label.split('\n')):
			x = line.find("{}")
			if x != -1:
				self.format_pos = (x + len(self.data) - 1, y)

	def update_cursor(self):
		format_x, format_line = self.format_pos

		x, y = self.get_line_pos(format_line)
		x += format_x + len(self.data)
		
		MainLoop.set_cursor_pos_end(x, y)

	def on_key_press_callback(self, key: bytes):
		if (key == b'\x0d' or key == b'\x1b'): # Newline / Escape
			self.stop_input()
			return
		
		self.data = self.data[:-1]
		
		if (key == b'\x08'): # Backspace
			self.data = self.data[:-1]
		elif self.validate(key):
			try:
				self.data += key.decode()
			except:
				pass

		self.data += ' '
		self.set_text()
		self.update_cursor()