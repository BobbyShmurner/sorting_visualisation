from typing import List

class Renderable:
	Ignore_Dirty = False

	def __init__(self, master: 'Renderable'):
		self.master = master
		self.is_dirty = True
		self.is_active = False
		self.is_active_self = True
		self.children: List['Renderable'] = []

		if (self.master != None): self.master.add_child(self)

	def add_child(self, child: 'Renderable'):
		self.children.append(child)
		
	def set_dirty(self):
		self.is_dirty = True

		if (self.master != None): self.master.set_dirty()

	def set_active(self, active: bool):
		self.is_active_self = active
		self.set_dirty()

	def render(self):
		pass

	def hide(self):
		pass
	
	def render_internal(self):
		if (not self.is_dirty) and (not Renderable.Ignore_Dirty): return
		self.is_dirty = False

		if (not self.is_active) or (not self.is_active_self):
			self.hide_internal()
			return

		self.render()

		for child in self.children:
			child.is_active = True
			child.render_internal()

	def hide_internal(self):
		self.hide()

		for child in self.children:
			child.hide_internal()