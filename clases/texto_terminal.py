
from threading import Thread

class TextoTerminal():
    texto_ingresado = ""

    def __init__(self):
        self.texto_ingresado = ""
        self.hilo_texto = Thread(target=self.input_thread)
        self.hilo_texto.daemon = True
        self.hilo_texto.start()
        
    def input_thread(self):        
        while True:
            self.texto_ingresado = input()

    def __del__(self):
        self.hilo_texto.stop()
