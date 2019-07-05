# importação de bibliotecas
from gpiozero import LED, Button, LightSensor
from flask import Flask


# criação do servidor
app = Flask(__name__)

# definição de funções das páginas
@app.route("/led/<int:led>/<string:state>")
def change_led_to_state(led, state):
    if(state == "on"):
        leds[led].on()
    else:
        leds[led].off()
    return "LED " + str(led) + ": " + str(state)

# criação dos componentes
leds = [LED(21, active_high=False), LED(22, active_high=False), LED(23, active_high=False), LED(24, active_high=False), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
for i in range(4):
    botoes[i].when_pressed = leds[i].toggle

lightSensor = LightSensor(8)
lightSensor.when_dark = leds[4].on
lightSensor.when_light = leds[4].off

# rode o servidor
app.run(port=5000, debug=False)