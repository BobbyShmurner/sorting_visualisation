from typing import List

class Renderable:
	Instances: List['Renderable'] = []
	
	def __init__(self):
		self.is_dirty = True
		self.Instances.append(self)
		
	def set_dirty(self):
		self.clear()
		self.is_dirty = True

	def render(self):
		raise NotImplementedError()