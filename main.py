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
	def create(self):
		Text(self, "Super cool text >:D")

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