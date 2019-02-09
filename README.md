El presente proyecto escrito en *Python* implementa un sistema de comunicación entre un *Arduino* y un ordenador, en este caso una *Raspberry Pi* para controlar la puerta de una casa para mascotas.

El objetivo es mantener monitoreado a la mascota.

El proyecto ejecuta un bot programado con la API Telegram, por lo que al ejecutar el proyecto podrás interactuar con el mediante una conversación en la aplicación Telegram.

El programa en Arduino se encarga de recolectar datos de sensores de movimiento y sonido que van dentro de la casa, los cuales se especifícan en el archivo *dogsHouse.ino*, el cual deberá compilarse en la tarjeta Arduino.

Deberás configurar las variables *TOKEN* y *my_chat_id* para que puedas interactuar con el bot. Revisa la documentación de la API de Telegram en la siguiente dirección: https://core.telegram.org/

Ejecutar: *bot_agent.py* para el **Bot Telegram** y *main.py* para el **monitoreo** de la mascota.

El ordenador donde se ejecuten los archivos de *Python* deberá tener conexión a internet.