from .prelude import *
from .events import Event
from .renderable import Renderable

from typing import Tuple

class MainLoop:
	Screen_Size: Tuple[int, int] = get_screen_size()
	Cursor_End_Pos = (0, 0)

	On_Main_Loop = Event()
	On_Key_Press = Event()

	@classmethod
	def set_cursor_pos_end(cls, x: int, y: int):
		cls.Cursor_End_Pos = (x, y)

	@classmethod
	def mainloop(cls):
		if get_screen_size() != cls.Screen_Size:
			cls.Screen_Size = get_screen_size()
			clear_screen()

		should_flush = False

		key_pressed = handle_input()
		if key_pressed != None:
			cls.On_Key_Press.invoke(key_pressed)

		cls.On_Main_Loop.invoke()
		Event.handle_invoke_queue()

		for instance in Renderable.Instances:
			if not instance.is_dirty: continue

			should_flush = True
			instance.render()

		cursor_x, cursor_y = cls.Cursor_End_Pos
		set_cursor_pos(cursor_x, cursor_y)
		if (should_flush): flush_screen()