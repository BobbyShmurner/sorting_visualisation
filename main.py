import sys
import os
import msvcrt
import weakref

from enum import Enum, auto
from typing import List, Tuple

class Anchor(Enum):
	UPPER_LEFT = auto(),
	UPPER_CENTER = auto(),
	UPPER_RIGHT = auto(),
	
	LEFT = auto(),
	CENTER = auto(),
	RIGHT = auto(),
	
	LOWER_LEFT = auto(),
	LOWER_CENTER = auto(),
	LOWER_RIGHT = auto(),

def get_screen_size() -> Tuple[int, int]:
	screen_size = os.get_terminal_size()
	return (screen_size.columns + 1, screen_size.lines + 1)

def reset_screen():
	sys.stdout.write("\033c")
	sys.stdout.flush()

def clear_screen():
	sys.stdout.write("\033[2J")
	sys.stdout.flush()
    
def show_cursor():
	sys.stdout.write("\033[?25h")
	sys.stdout.flush()

def hide_cursor():
	sys.stdout.write("\033[?25l")
	sys.stdout.flush()

class Text:
	instances: List['Text'] = []
	Screen_size: Tuple[int, int] = get_screen_size()
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

		self.set_text(text)

	@classmethod
	def mainloop(cls):
		if get_screen_size() != cls.Screen_size:
			cls.Screen_size = get_screen_size()
			clear_screen()
			return

		should_flush = False

		for instance in cls.instances:
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
		for style_code in cls.STYLE_TABLE.values():
			line = line.replace(style_code, "")

		return len(line)

	def get_rel_pos(self, line_num: int) -> tuple[int, int]:
		screen_width, screen_height = self.__class__.Screen_size
		line_width = self.get_line_len(self.lines[line_num])

		if self.anchor == Anchor.UPPER_LEFT or self.anchor == Anchor.LEFT or self.anchor == Anchor.LOWER_LEFT:
			x = self.x
		elif self.anchor == Anchor.UPPER_CENTER or self.anchor == Anchor.CENTER or self.anchor == Anchor.LOWER_CENTER:
			x = screen_width // 2 - line_width // 2 + self.x
		else:
			x = screen_width - line_width - self.x

		if self.anchor == Anchor.UPPER_LEFT or self.anchor == Anchor.UPPER_CENTER or self.anchor == Anchor.UPPER_RIGHT:
			y = self.y + line_num + 1
		elif self.anchor == Anchor.LEFT or self.anchor == Anchor.CENTER or self.anchor == Anchor.RIGHT:
			y = screen_height // 2 - self.height // 2 + self.y + line_num
		else:
			y = screen_height - line_num - 1 - self.y

		self.prev_screen_width = screen_width
		self.prev_screen_height = screen_height

		delta_x = min(max(x, 1), screen_width - self.width) - x
		delta_y = min(max(y, line_num + 1), screen_height - self.height + line_num) - y

		self.x += delta_x
		self.y += delta_y

		return (x + delta_x, y + delta_y)

	def render(self):
		for i, line in enumerate(self.lines):
			(rel_x, rel_y) = self.get_rel_pos(i)
			sys.stdout.write(f"\033[{rel_y};{rel_x}f")
			sys.stdout.write(line)

	def clear(self):
		for i, line in enumerate(self.lines):
			(rel_x, rel_y) = self.get_rel_pos(i)
			sys.stdout.write(f"\033[{rel_y};{rel_x}f")
			sys.stdout.write(' ' * self.get_line_len(line))
		
	

def handle_input() -> bytes:
	if not msvcrt.kbhit(): return None

	key = msvcrt.getch()
	if msvcrt.kbhit():
		key += msvcrt.getch()
	
	return key

try:
	hide_cursor()
	clear_screen()

	hello_text = Text("""   _____            __  _                _    ___                  ___            __  _                  __
  / ___/____  _____/ /_(_)___  ____ _   | |  / (_)______  ______ _/ (_)________ _/ /_(_)___  ____  _____/ /
  \__ \/ __ \/ ___/ __/ / __ \/ __ `/   | | / / / ___/ / / / __ `/ / / ___/ __ `/ __/ / __ \/ __ \/ ___/ / 
 ___/ / /_/ / /  / /_/ / / / / /_/ /    | |/ / (__  ) /_/ / /_/ / / (__  ) /_/ / /_/ / /_/ / / / (__  )_/  
/____/\____/_/   \__/_/_/ /_/\__, /     |___/_/____/\__,_/\__,_/_/_/____/\__,_/\__/_/\____/_/ /_/____(_)   
                            /____/                                                                         """)
	
	key_display = Text("<b>[Key Display]", anchor=Anchor.LOWER_RIGHT)

	Text("<b>Bold</b> <i>Italics</i> <u>Underline</u> <s>Strikethrough</s>", anchor=Anchor.LOWER_CENTER)
	Text("<b><i><fg=red>RED TEXT</fg></i></b>", y=1, anchor=Anchor.LOWER_CENTER)

	while True:
		key = handle_input()

		if key != None:
			key_display.set_text("<b>0x" + key.hex())

		if key == b'\x00\x4d':
			hello_text.move(1, 0)
		elif key == b'\x00\x4b':
			hello_text.move(-1, 0)
		elif key == b'\x00\x50':
			hello_text.move(0, 1)
		elif key == b'\x00\x48':
			hello_text.move(0, -1)

		Text.mainloop()
except KeyboardInterrupt:
	pass
finally:
	show_cursor()
	print("\n")