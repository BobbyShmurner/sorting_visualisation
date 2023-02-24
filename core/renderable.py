from typing import List

class Renderable:
	def __init__(self, master: 'Renderable'):
		self.master = master
		self.is_dirty = True
		self.is_active = False
		self.children: List['Renderable'] = []

		if (self.master != None): self.master.add_child(self)

	def add_child(self, child: 'Renderable'):
		self.children.append(child)
		
	def set_dirty(self):
		self.is_dirty = True

		if (self.master != None): self.master.set_dirty()

	def render(self):
		pass
	
	def render_internal(self):
		if (not self.is_active) or (not self.is_dirty): return

		self.render()

		for child in self.children:
			child.is_active = True
			child.render_internal()

		self.is_dirty = False