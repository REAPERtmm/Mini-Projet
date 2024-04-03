
class Event:
	def __init__(self, CallBack, *args):
		self.callback = CallBack
		self.args = args

	def trigger(self):
		self.callback(*self.args)