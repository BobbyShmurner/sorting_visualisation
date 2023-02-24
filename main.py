import traceback

from core.prelude import *
from core.widgets import *

from core import MainLoop

def is_num(key: bytes) -> bool:
	return key.isdigit()

class TitleWindow(Window):
	def create(self):
		Text(self, r"""<b><fg=green> __            _   _                     _                 _ _           _   _                 
/ _\ ___  _ __| |_(_)_ __   __ _  /\   /(_)___ _   _  __ _| (_)___  __ _| |_(_) ___  _ __  ___ 
\ \ / _ \| '__| __| | '_ \ / _` | \ \ / / / __| | | |/ _` | | / __|/ _` | __| |/ _ \| '_ \/ __|
_\ \ (_) | |  | |_| | | | | (_| |  \ V /| \__ \ |_| | (_| | | \__ \ (_| | |_| | (_) | | | \__ \
\__/\___/|_|   \__|_|_| |_|\__, |   \_/ |_|___/\__,_|\__,_|_|_|___/\__,_|\__|_|\___/|_| |_|___/
                           |___/                                                               """
		)
		
		Text(self, "<b>Press <fg=green><u>Enter</u></fg> To Begin!</b>", y=5)

		input = InputField(self, "{}", y=10)
		input.on_stop_input.subscribe(InputWindow().show)
		input.get_input()

class InputWindow(Window):
	UNSORTED_BOX_LABEL = "<fg=black>[<b><fg=white>{}<fg=black></b>]</fg>"
	SORTED_BOX_LABEL = "<b><fg=green>[<fg=cyan>{}<fg=green>]</fg></b>"
	MIN_NUM_COUNT = 3

	def create(self):
		self.input = InputField(self, InputWindow.UNSORTED_BOX_LABEL, validate=is_num)
		self.input.on_stop_input.subscribe(self.setup_input_for_next_num)
		self.input.get_input()

		self.status_text = Text(self, "<b>Please Enter The Digits You Wish To Sort</b>", y=3)

		self.error_text = Text(self, f"<b><fg=red>You Must Enter At Least {InputWindow.MIN_NUM_COUNT} Number!</fg></b>", y=4)
		self.error_text.set_active(False)

		self.nums: List[int] = []

	def setup_input_for_next_num(self):
		self.error_text.set_active(False)

		if (self.input.data == ""): 
			if len(self.nums) < InputWindow.MIN_NUM_COUNT:
				self.error_text.set_active(True)
				self.input.get_input()
			else:
				self.input.set_label(self.input.label[:-len(InputWindow.UNSORTED_BOX_LABEL) -1] + "{}")

			return
		
		self.nums.append(int(self.input.data))
		self.input.set_label(self.input.label.format(self.input.data) + ' ' + InputWindow.UNSORTED_BOX_LABEL)
		self.input.get_input()

def main():
	TitleWindow().show()

	while True:
		if not MainLoop.mainloop(): break

if __name__ == '__main__':
	error = None

	try:
		main()
	except KeyboardInterrupt:
		pass
	except BaseException as e:
		error = traceback.format_exc()
	finally:
		clean_exit()

		if error != None:
			print(f"-- Error!!! --\n\n{error}")