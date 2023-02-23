import sys
import os
import msvcrt

from typing import Tuple

def set_cursor_pos(x: int, y: int):
	sys.stdout.write(f"\033[{y};{x}f")

def get_screen_size() -> Tuple[int, int]:
	Screen_Size = os.get_terminal_size()
	return (Screen_Size.columns + 1, Screen_Size.lines + 1)

def clean_exit():
	set_cursor_pos(0, get_screen_size()[1])

	reset_style()
	show_cursor()
	flush_screen()

	print('\n')

def flush_screen():
	sys.stdout.flush()

def reset_screen():
	sys.stdout.write("\033c")

def reset_style():
	sys.stdout.write("\033[0m")

def clear_screen():
	sys.stdout.write("\033[2J")
    
def show_cursor():
	sys.stdout.write("\033[?25h")

def hide_cursor():
	sys.stdout.write("\033[?25l")

def handle_input() -> bytes:
	if not msvcrt.kbhit(): return None

	key = msvcrt.getch()
	if msvcrt.kbhit():
		key += msvcrt.getch()
	
	return key