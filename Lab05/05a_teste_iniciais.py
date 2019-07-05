# importação de bibliotecas
from gpiozero import LED,Button,MotionSensor,LightSensor,DistanceSensor
from threading import Timer
from requests import post

# definição de funções
def MotionDetected():
    led1.on()
    led2.on()
    global timer
    if timer != None:
        timer.cancel()
        timer =  None
def NoMotionDetected():
    led1.off()
    global timer
    timer = Timer(8.0,led2.off)
    timer.start()
def Documentacao():
    dados = {"value1": lightSensor.value*100, "value2": distSensor.distance*100}
    chave = "bFkpPSRk6m_HENoq8Yoh9p"
    evento = "button1_pressed"
    endereco = "https://maker.ifttt.com/trigger/"+ evento +"/with/key/" + chave
    resultado = post(endereco, json=dados)
    print(resultado.text)
# criação de componentes
timer = None
led1 = LED(21)
led2 = LED(22)
button1 = Button(11)
lightSensor = LightSensor(8)
distSensor = DistanceSensor(trigger=17, echo=18)
MovSensor = MotionSensor(27)
MovSensor.when_motion = MotionDetected
MovSensor.when_no_motion = NoMotionDetected
button1.when_pressed = Documentacao
# loop infinito
