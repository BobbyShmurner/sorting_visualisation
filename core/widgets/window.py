from typing import Type
from ..renderable import Renderable
from ..mainloop import MainLoop
from ..prelude import *

class Window(Renderable):
	Active: Type['Window'] = None
	
	def __init__(self):
		super().__init__(None)

	def create(self):
		raise NotImplementedError()
	
	def render(self):
		super().render()
		
	def show(self):
		if (Window.Active != None): Window.Active.hide()
		Window.Active = self

		self.is_active = True

		MainLoop.On_Main_Loop.subscribe(self.render_internal)
		self.create()
		clear_screen()

	def hide(self):
		self.is_active = False
		Window.Active = None
		MainLoop.On_Main_Loop.unsubscribe(self.render_internal)
