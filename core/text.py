import sys
import re

from .prelude import *
from .anchor import *

from typing import Callable, List, Tuple

class Text:
	instances: List['Text'] = []
	Screen_size: Tuple[int, int] = get_screen_size()

	ESCAPE_RE = "\033\[\d{1,3}m"

	STYLE_TABLE = {
		"</r>": "\033[0m",

		"<b>": "\033[1m",
		"</b>": "\033[22m",
		"<i>": "\033[3m",
		"</i>": "\033[23m",
		"<u>": "\033[4m",
		"</u>": "\033[24m",
		"<s>": "\033[9m",
		"</s>": "\033[29m",
		"<fg=": "\033[3",
		"<bg=": "\033[4",
		"<bfg=": "\033[9",
		"<bbg=": "\033[10",
		"</fg>": "\033[39m",
		"</bg>": "\033[49m",
		"</bfg>": "\033[39m",
		"</bbg>": "\033[49m",
	}
	COLOUR_TABLE = {
		"black": '0m',
		"red": '1m',
		"green": '2m',
		"yellow": '3m',
		"blue": '4m',
		"magenta": '5m',
		"purple": '5m',
		"cyan": '6m',
		"white": '7m',
	}

	def __init__(self, text: str, x: int = 0, y: int = 0, anchor: Anchor = Anchor.CENTER):
		self.__class__.instances.append(self)
		
		self.x = x
		self.y = y
		self.anchor = anchor
		self.lines: List[str] = []
		self.is_dirty = True

		self.on_main_loop: List[Callable] = []
		self.on_key_press: List[Callable[[bytes], any]] = []

		self.set_text(text)

	def add_main_loop_even(self, event: Callable):
		self.on_main_loop.append(event)

	def add_key_press_event(self, event: Callable[[bytes], any]):
		self.on_key_press.append(event)

	@classmethod
	def mainloop(cls):
		if get_screen_size() != cls.Screen_size:
			cls.Screen_size = get_screen_size()
			clear_screen()

		should_flush = False
		key_pressed = handle_input()

		for instance in cls.instances:
			if key_pressed != None:
				for event in instance.on_key_press:
					event(key_pressed)

			for event in instance.on_main_loop:
				event()

			if not instance.is_dirty: continue

			should_flush = True
			instance.render()

		if (should_flush): sys.stdout.flush()

	def set_text(self, text: str):
		self.set_dirty()

		text += "</r>"

		for key, value in self.__class__.COLOUR_TABLE.items():
			start_index = -1
			while True:
				start_index = text.find(key, start_index + 1)
				if start_index == -1: break

				if start_index <= 0: continue
				if start_index > len(text) - len(key) - 1: continue
				if text[start_index-1] != '=': continue
				if text[start_index + len(key)] != ">": continue

				text = text[:start_index] + value + text[start_index + len(key) + 1:]

		for key, value in self.__class__.STYLE_TABLE.items():
			text = text.replace(key, value)

		self.lines = text.split('\n')
		self.calculate_dimensions()

	def set_pos(self, x: int, y: int):
		self.set_dirty()
		
		self.x = x
		self.y = y

	def move(self, x: int, y: int):
		self.set_dirty()
		
		self.x += x
		self.y += y

	def set_dirty(self):
		self.clear()
		self.is_dirty = True

	def calculate_dimensions(self):
		self.height = len(self.lines)
		self.width = 0

		for line in self.lines:
			line_len = self.get_line_len(line)

			if line_len > self.width:
				self.width = line_len

	@classmethod
	def get_line_len(cls, line: str) -> int:
		escape_len = 0

		for match in re.finditer(cls.ESCAPE_RE, line):
			escape_len += match.end() - match.start()

		return len(line) - escape_len

	def get_rel_pos(self, line_num: int) -> tuple[int, int]:
		screen_width, screen_height = self.__class__.Screen_size
		line_width = self.get_line_len(self.lines[line_num])

		if self.anchor == Anchor.UPPER_LEFT or self.anchor == Anchor.LEFT or self.anchor == Anchor.LOWER_LEFT:
			x = self.x + 1
		elif self.anchor == Anchor.UPPER_CENTER or self.anchor == Anchor.CENTER or self.anchor == Anchor.LOWER_CENTER:
			x = screen_width // 2 - line_width // 2 + self.x
		else:
			x = screen_width - line_width - self.x

		if self.anchor == Anchor.UPPER_LEFT or self.anchor == Anchor.UPPER_CENTER or self.anchor == Anchor.UPPER_RIGHT:
			y = self.y + line_num + 1
		elif self.anchor == Anchor.LEFT or self.anchor == Anchor.CENTER or self.anchor == Anchor.RIGHT:
			y = screen_height // 2 - self.height // 2 + self.y + line_num
		else:
			y = screen_height + line_num - self.height - self.y

		delta_x = min(max(x, 1), screen_width - self.width) - x
		delta_y = min(max(y, line_num + 1), screen_height - self.height + line_num) - y

		self.x += delta_x
		self.y += delta_y

		return (x, y)

	def render(self):
		self.print_internal()

	def clear(self):
		self.print_internal(True)

	def print_internal(self, clear: bool = False):
		for i, line in enumerate(self.lines):
			(rel_x, rel_y) = self.get_rel_pos(i)

			sys.stdout.write(f"\033[{rel_y};{rel_x}f")
			sys.stdout.write(' ' * self.get_line_len(line) if clear else line)