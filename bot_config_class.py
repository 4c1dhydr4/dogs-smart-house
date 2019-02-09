
class BotConfig:
	move_alert = True
	sound_alert = True
	data = {
		'open_door': "ODN\n",
		'close_door': "CDN\n",
	}
	
	def __init__(self):
		self.move_alert = True
		self.sound_alert = True
		self.data = data= {'open_door': "ODN\n",'close_door': "CDN\n"}

	def def_move_alert(self, definition=True):
		self.move_alert = definition

	def def_sound_alert(self, definition=True):
		self.sound_alert = definition

	def return_move_alert(self):
		return self.move_alert

	def return_sound_alert(self):
		return self.sound_alert