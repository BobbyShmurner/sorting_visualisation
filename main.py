from time import time

from core import *

class Timer(Text):
	def __init__(self, label: str = "{:0.2f}", x: int = 0, y: int = 0, anchor: Anchor = Anchor.CENTER):
		super().__init__(label, x, y, anchor)

		self.label = label
		self.start_time = time()

		self.add_main_loop_even(self.tick)

	def tick(self):
		self.set_text(self.label.format(time() - self.start_time))

class MovingText(Text):
	def __init__(self, text: str = "Moving Text", x: int = 0, y: int = 0, anchor: Anchor = Anchor.CENTER):
		super().__init__(text, x, y, anchor)

		self.add_key_press_event(self.handle_movement)

	def handle_movement(self, key):
		if key == b'\x00\x4d':
			self.move(1, 0)
		elif key == b'\x00\x4b':
			self.move(-1, 0)
		elif key == b'\x00\x50':
			self.move(0, 1)
		elif key == b'\x00\x48':
			self.move(0, -1)

class KeyDisplay(Text):
	def __init__(self, label: str = "0x{}", x: int = 0, y: int = 0, anchor: Anchor = Anchor.CENTER, default_text: str = None):
		if default_text == None:
			default_text = label.format("00")

		super().__init__(default_text, x, y, anchor)

		self.label = label
		self.add_key_press_event(self.on_press_callback)

	def on_press_callback(self, key):
		self.set_text(self.label.format(key.hex()))

class Input(Text):
	def __init__(self, label: str = "{}", x: int = 0, y: int = 0, anchor: Anchor = Anchor.CENTER):
		super().__init__(label, x, y, anchor)

		self.label = label

		self.add_main_loop_even(self.display_typing)

	def display_typing(self):
		self.set_text(self.label.format(time() - self.start_time))

def main():
	hide_cursor()
	clear_screen()

	MovingText("""<b><fg=green>    _____            __  _                _    ___                  ___            __  _                  __
  / ___/____  _____/ /_(_)___  ____ _   | |  / (_)______  ______ _/ (_)________ _/ /_(_)___  ____  _____/ /
  \__ \/ __ \/ ___/ __/ / __ \/ __ `/   | | / / / ___/ / / / __ `/ / / ___/ __ `/ __/ / __ \/ __ \/ ___/ / 
 ___/ / /_/ / /  / /_/ / / / / /_/ /    | |/ / (__  ) /_/ / /_/ / / (__  ) /_/ / /_/ / /_/ / / / (__  )_/  
/____/\____/_/   \__/_/_/ /_/\__, /     |___/_/____/\__,_/\__,_/_/_/____/\__,_/\__/_/\____/_/ /_/____(_)   
                            /____/                                                                         """)
	
	KeyDisplay("<b>[0x{}]</b>", default_text="<b>[Key Display]</b>", anchor=Anchor.LOWER_RIGHT)

	Timer("<b>Random Timer: <fg=cyan>{:0.2f}</fg></b>", anchor=Anchor.UPPER_CENTER)

	Text("<b>Bold</b> <i>Italics</i> <u>Underline</u> <s>Strikethrough</s>", anchor=Anchor.LOWER_CENTER)
	Text("<b><i><fg=red>RED TEXT</fg></i></b>", y=1, anchor=Anchor.LOWER_CENTER)

	while True:
		Text.mainloop()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass
	finally:
		show_cursor()
		print("\n")