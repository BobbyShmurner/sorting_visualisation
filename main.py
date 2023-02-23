import traceback

from core.prelude import *
from core.widgets import *

from core import Anchor
from core import MainLoop
		
def is_num(key: bytes) -> bool:
	return key.isdigit()

def main():
	hide_cursor()
	clear_screen()

	MovingText(r"""<b><fg=green> __            _   _                     _                 _ _           _   _                 
/ _\ ___  _ __| |_(_)_ __   __ _  /\   /(_)___ _   _  __ _| (_)___  __ _| |_(_) ___  _ __  ___ 
\ \ / _ \| '__| __| | '_ \ / _` | \ \ / / / __| | | |/ _` | | / __|/ _` | __| |/ _ \| '_ \/ __|
_\ \ (_) | |  | |_| | | | | (_| |  \ V /| \__ \ |_| | (_| | | \__ \ (_| | |_| | (_) | | | \__ \
\__/\___/|_|   \__|_|_| |_|\__, |   \_/ |_|___/\__,_|\__,_|_|_|___/\__,_|\__|_|\___/|_| |_|___/
                           |___/                                                               """)
	
	KeyDisplay("<b>[0x{}]</b>", default_text="<b>[Key Display]</b>", anchor=Anchor.LOWER_RIGHT)

	Timer("<b>Random Timer: <fg=cyan>{:0.2f}</fg></b>", anchor=Anchor.UPPER_CENTER)

	Text("<b><i><fg=red>RED TEXT</fg></i></b>\nhuh?\n<b>Bold</b> <i>Italics</i> <u>Underline</u> <s>Strikethrough</s>", anchor=Anchor.LOWER_CENTER)

	input_text = InputField("Input: [{}]", y=5)
	input_num = InputField("Num Input: [{}]", y=6, validate=is_num)

	input_text.on_stop_input.subscribe(input_num.get_input)
	input_text.get_input()

	while True:
		MainLoop.mainloop()

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