import bot_agent as TB
import time
import comunication as SS
import pickle
from bot_config_class import BotConfig

def main():
	while_flag = True
	bot_config = BotConfig()
	while while_flag:
		hora = TB.get_time()
		try:
			with open('bot_config.pkl', 'rb') as input:
			    bot_config = pickle.load(input)
			print("Recibiendo Datos")
			status = SS.start()
			print(status)
			print("Verificando")
			if bot_config.move_alert:
				if status['moving'] >= 1000:
					TB.send_move_alert()
					print("Movimiento Detectado", hora)
			if bot_config.sound_alert:
				if status['sound'] >= 1000:
					TB.send_sound_alert()
					print("Ladrido Detectado", hora)
			time.sleep(10)
		except:
			print("Error", hora)
			time.sleep(20)
			#while_flag = False

if __name__ == '__main__':
	main()
