from .prelude import *
from .events import Event
from .renderable import Renderable

from typing import Tuple

class MainLoop:
	Screen_Size: Tuple[int, int] = get_screen_size()
	Exiting = False

	Cursor_End_Pos = (0, 0)
	Cursor_End_Active = False

	On_Main_Loop = Event()
	On_Key_Press = Event()

	@classmethod
	def set_cursor_pos(cls, x: int, y: int):
		cls.Cursor_End_Pos = (x, y)

	@classmethod
	def set_cursor_active(cls, active = bool):
		cls.Cursor_End_Active = active

	@classmethod
	def exit(cls):
		cls.Exiting = True

	@classmethod
	def mainloop(cls) -> bool:
		if get_screen_size() != cls.Screen_Size:
			cls.Screen_Size = get_screen_size()
			clear_screen()

		key_pressed = handle_input()
		if key_pressed != None:
			cls.On_Key_Press.invoke(key_pressed)

		cls.On_Main_Loop.invoke()
		Event.handle_invoke_queue()

		cursor_x, cursor_y = cls.Cursor_End_Pos

		set_cursor_pos(cursor_x, cursor_y)
		show_cursor() if cls.Cursor_End_Active else hide_cursor()

		flush_screen()

		return (not cls.Exiting) and (len(cls.On_Main_Loop.subscribers) != 0)