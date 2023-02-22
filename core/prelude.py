import sys
import os
import msvcrt

from typing import Tuple

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

def handle_input() -> bytes:
	if not msvcrt.kbhit(): return None

	key = msvcrt.getch()
	if msvcrt.kbhit():
		key += msvcrt.getch()
	
	return key