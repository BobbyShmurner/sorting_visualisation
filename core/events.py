from typing import Callable, List

class Event:
	Invoke_queue : List[Callable] = []

	def __init__(self):
		self.subscribers: List[Callable] = []
	
	def subscribe(self, callback: Callable):
		self.subscribers.append(callback)

	def unsubscribe(self, callback: Callable, unsubscribe_all: bool = False):
		try:
			while (True):
				self.subscribers.remove(callback)
				if not unsubscribe_all: return
		except:
			return
		
	@classmethod
	def add_to_invoke_queue(cls, callback: Callable, args: tuple, kwargs: dict[str, any]):
		cls.Invoke_queue.append((callback, args, kwargs))

	@classmethod
	def handle_invoke_queue(cls):
		for callback, args, kwargs in cls.Invoke_queue:
			callback(*args, **kwargs)

		cls.Invoke_queue.clear()

	def invoke_instant(self, *args, **kwargs):
		for subscriber in self.subscribers:
			subscriber(*args, **kwargs)
		
	def invoke(self, *args, **kwargs):
		for subscriber in self.subscribers:
			self.__class__.add_to_invoke_queue(subscriber, args, kwargs)
