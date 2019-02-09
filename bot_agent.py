#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import comunication as SS
import time
import pickle
from bot_config_class import BotConfig

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logs = []

main_menu = [
		[telegram.KeyboardButton('/ESTADO'), telegram.KeyboardButton('/HISTORIAL')], 
		[telegram.KeyboardButton('/CONFIGURACION'), telegram.KeyboardButton('/PUERTA')],
	]
kb_main_menu = telegram.ReplyKeyboardMarkup(main_menu)

door_menu_ = [
		[telegram.KeyboardButton('/ABRIR_PUERTA'), telegram.KeyboardButton('/CERRAR_PUERTA')], 
	]
kb_door_menu = telegram.ReplyKeyboardMarkup(door_menu_)


TOKEN = "Ingresa aqui tu token"

my_chat_id = 11111 #Ingresa el id de tu chat en telegram

bot_config = BotConfig()

#Definición de Utilitarios
def get_user(update):
	first_name = update.message.from_user.first_name
	last_name = update.message.from_user.last_name
	first_name = str(first_name)
	last_name = str(last_name)
	user_text = first_name +  " " + last_name
	return user_text

def get_time():
	times = time.asctime(time.localtime(time.time()))
	return times

def put_log(log,update):
	user_text = get_user(update)
	hora = get_time()
	mensaje = hora + "::" + log + " " + user_text
	print(mensaje)
	global logs
	logs.append(mensaje)
	return mensaje

#Salvando Configuración
def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


#Seguridad
def verify_log(bot, update):
	if(update.message.chat_id == my_chat_id):
		return True
	else:
		update.message.reply_text("No tienes permiso de hacer esto :(")
		send_message_to_me(bot, put_log("Permiso no concedido a: ",update))
		return False


#Retornos de Configuración

def get_move_config():
	return bot_config.return_move_alert()

def get_sound_config():
	return bot_config.return_sound_alert()


#Definición de Menús
def start_menu(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Menú Principal", reply_markup=kb_main_menu)

def door_menu(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Menú Principal", reply_markup=kb_door_menu)

def config_alert_menu(bot, update):
	if verify_log(bot, update):
		kb = [
				[telegram.KeyboardButton('/CONFIGURACION_LADRIDO')],[telegram.KeyboardButton('/CONFIGURACION_MOVIMIENTO')]
			]
		kb_markup = telegram.ReplyKeyboardMarkup(kb)
		bot.send_message(chat_id=update.message.chat_id, text="Configuración de Alertas", reply_markup=kb_markup)

def move_config(bot, update):
	if verify_log(bot, update):
		kb = [
				[telegram.KeyboardButton('/MOVIMIENTO_ACTIVADO'), telegram.KeyboardButton('/MOVIMIENTO_DESACTIVADO')], 
			]
		kb_markup = telegram.ReplyKeyboardMarkup(kb)
		status = bot_config.return_move_alert()
		text = "Configuración de Alerta de Movimiento: {}".format(status)
		bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=kb_markup)

def sound_config(bot, update):
	if verify_log(bot, update):
		kb = [
				[telegram.KeyboardButton('/LADRIDO_ACTIVADO'), telegram.KeyboardButton('/LADRIDO_DESACTIVADO')], 
			]
		kb_markup = telegram.ReplyKeyboardMarkup(kb)
		status = bot_config.return_sound_alert()
		text = "Configuración de Alerta de Ladrido: {}".format(status)
		bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=kb_markup)

def move_on(bot, update):
	if verify_log(bot, update):
		update.message.reply_text('Alerta de Movimiento Activado')
		bot_config.def_move_alert()
		save_object(bot_config, 'bot_config.pkl')
		bot.send_message(chat_id=update.message.chat_id, text="Menú Principal", reply_markup=kb_main_menu)


def move_off(bot, update):
	if verify_log(bot, update):
		update.message.reply_text('Alerta de Movimiento Desactivado')
		bot_config.def_move_alert(False)
		save_object(bot_config, 'bot_config.pkl')
		bot.send_message(chat_id=update.message.chat_id, text="Menú Principal", reply_markup=kb_main_menu)


def sound_on(bot, update):
	if verify_log(bot, update):
		update.message.reply_text('Alerta de Ladrido Activado')
		bot_config.def_sound_alert()
		save_object(bot_config, 'bot_config.pkl')
		bot.send_message(chat_id=update.message.chat_id, text="Menú Principal", reply_markup=kb_main_menu)


def sound_off(bot, update):
	if verify_log(bot, update):
		update.message.reply_text('Alerta de Ladrido Desactivado')
		bot_config.def_sound_alert(False)
		save_object(bot_config, 'bot_config.pkl')
		bot.send_message(chat_id=update.message.chat_id, text="Menú Principal", reply_markup=kb_main_menu)


"""
Definición de Envíos
"""
def send_message_to_me(bot, mensaje):
	bot.send_message(chat_id=my_chat_id, text=mensaje)

def send_move_alert():
	bot = telegram.Bot(TOKEN)
	hora = get_time()
	mensaje = "Movimiento Detectado {}".format(hora)
	send_message_to_me(bot, mensaje)

def send_sound_alert():
	bot = telegram.Bot(TOKEN)
	hora = get_time()
	mensaje = "Ladrido Detectado {}".format(hora)
	send_message_to_me(bot, mensaje)

def return_logs(bot, update):
	if verify_log(bot, update):
		mensaje = ""
		for data in logs:
			mensaje = mensaje + data + "\n"
		update.message.reply_text(mensaje)

#Puertas
def open_door(bot, update):
	hora = get_time()
	mensaje = ""
	try:
		SS.send_data(bot_config.data['open_door'])
		mensaje = "Puerta Abierta {}".format(hora)
	except Exception as e:
		print(e)
		mensaje = "Error el Abrir Puerta {}".format(hora)
	send_message_to_me(bot, mensaje)

def close_door(bot, update):
	hora = get_time()
	mensaje = ""
	flag = True
	while(flag):
		if SS.send_data(bot_config.data['close_door']):
			mensaje = "Puerta Cerrada {}".format(hora)
			flag = False
	send_message_to_me(bot, mensaje)
#Menú Escencial

def start(bot, update):
	send_message_to_me(bot, put_log("Sesión iniciada por",update))
	update.message.reply_text('MeganHouse_Bot en línea, Ingresa al menú principal: /start_menu')

def help(bot, update):
	update.message.reply_text('Si necesitas ayuda llama al 105, si eres peruano ten en cuenta que no contestan')

def echo(bot, update):
	update.message.reply_text(update.message.text)

def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)


# PUERTA
# ABRIR_PUERTA
# CERRAR_PUERTA

def main():
	save_object(bot_config,'bot_config.pkl')
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	# dp.add_handler(CommandHandler("ESTADO", status))
	dp.add_handler(CommandHandler("start_menu", start_menu))
	dp.add_handler(CommandHandler("HISTORIAL", return_logs))
	dp.add_handler(CommandHandler("PUERTA", door_menu))
	dp.add_handler(CommandHandler("ABRIR_PUERTA", open_door))
	dp.add_handler(CommandHandler("CERRAR_PUERTA", close_door))
	dp.add_handler(CommandHandler("CONFIGURACION", config_alert_menu))
	dp.add_handler(CommandHandler("CONFIGURACION_MOVIMIENTO", move_config))
	dp.add_handler(CommandHandler("CONFIGURACION_LADRIDO", sound_config))
	dp.add_handler(CommandHandler("MOVIMIENTO_ACTIVADO", move_on))
	dp.add_handler(CommandHandler("MOVIMIENTO_DESACTIVADO", move_off))
	dp.add_handler(CommandHandler("LADRIDO_ACTIVADO", sound_on))
	dp.add_handler(CommandHandler("LADRIDO_DESACTIVADO", sound_off))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(MessageHandler(Filters.text, echo))
	dp.add_error_handler(error)
	print("Iniciando Sesión en MeganHouse_Bot, Telegram")
	updater.start_polling()
	print("Sesión Iniciada")
	updater.idle()

if __name__ == '__main__':
	main()
