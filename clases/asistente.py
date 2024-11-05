
from time import sleep, time as timenow
from sys import exit

from clases.utils import *
from clases.audio_driver import *
from clases.google_driver import *
from clases.selenium_driver import *

from config import USER, PASSWORD

class Asistente():
    def __init__(self):        
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.url = "https://chat.openai.com"
        print(f'{azul}Iniciando Selenium Drivers...{gris}')
        # Carga el Driver del Navegador
        self.uc = SeleniumDriver()
        login = self.login_openai() # Login
        print()
        if not login:
            print(f'\33[K{rojo}INICIO FALLIDO{gris}')
            exit()

    def login_openai(self):
        print(f'\33[K{azul}Cargando Asistente...\n{gris}')  
        self.uc.Driver.get(self.url)
        self.uc.Driver.wait.load_start()
        #Login desde Cero
        if self.uc.Driver.ele('css:[data-testid="login-button"]'):
            self.uc.Driver.ele('css:[data-testid="login-button"]').click()
            self.uc.Driver.ele('css:social-logo').click()
            self.uc.Driver.ele('css:input[type="email"]',timeout=2).input(self.USER)
            self.uc.Driver.ele('css:#identifierNext').click()
            self.uc.Driver.ele('css:input[type="password"]',timeout=2).input(self.PASSWORD)
            self.uc.Driver.ele('css:#passwordNext').click()

        login = self.comprobar_login()
        # Verifica si se pudo logear correctamente
        if login:
            return login
        else:
            print(f'\33[K{azul}COOKIES: {rojo}FALLIDO{gris}')

    def comprobar_login(self, tmpo=3):

        login = False
        while tmpo > 0:
            try:
                self.uc.Driver('css:[data-testid="profile-button"]')  
                self.uc.Driver('css:#prompt-textarea').click()
                login = True
                break
            except:
                pass
            try:
                if self.uc.Driver.ele('tx=session has expired'):
                    cursor_arriba()
                    print(f'\33[K{amarillo}LA SESSION HA EXPIRADO{gris}')
                    print()
                    break
            except:
                pass
            cursor_arriba()
            print(f'\33[K{gris}Comprobando Login... {tmpo}{gris}')
            sleep(1)
            tmpo -= 1
        cursor_arriba()
        print('\33[K')
        cursor_arriba(2)
        return login

    def ultima_conversacion(self, tmpo=3):
        try:
            self.uc.Driver.ele('tx=Historial',  timeout=tmpo).click()            
        except:
            print(f'\33[K{amarillo}No se encontro Ultima Conversacion{gris}')

        
    def chatear(self, prompt = None):
        if prompt:
            # Intruduce texto en el promp o textbox
            self.uc.Driver.ele('#:prompt-textarea').input(prompt)
            self.uc.Driver.ele('css:[data-testid="send-button"]').click()
            respuesta = ''
            sleep(0.5)
            # Generando las respuestas
            inicio = timenow()
            while True:
                # Obtener el último elemento markdown y su texto
                markdown = self.uc.Driver.eles('css:.markdown',timeout=0.5)
                if markdown:
                    respuesta = markdown[-1].text            
                # Verificar si el botón de "Stop generating" todavía está presente
                boton_stop = self.uc.Driver.ele('css:[data-testid="stop-button"]', timeout=0.5)
                if not boton_stop and respuesta:
                    break  # Salir del bucle si el botón no está presente y ya hay respuesta generada            
                # Calcular el tiempo transcurrido
                segundos = int(timenow() - inicio)
                if segundos > 0:                
                    print(f'\33[K{azul2}Generando respuesta... {gris}{segundos} segundos ({len(respuesta)} caracteres{gris})')
                    sleep(1)
                    # Mantener el cursor en la misma línea
                    cursor_arriba()              
            try:   
                if segundos:
                    print(f'\33[K{magenta}Respuesta generada en... {blanco}{segundos} {magenta}segundos{gris}')
            except:
                pass            
            # Esperar antes de devolver la respuesta final
            sleep(2)
            # Devolver la respuesta completa
            markdown = self.uc.Driver.eles('css:.markdown', timeout=1)
            return markdown[-1].text
        else:
            return None
    
    def buscar_texto_en_navegador(self, texto_a_buscar):
        try: 
            texto_filtrado = texto_a_buscar.split("to_google ", 1)
            nav = GoogleDriver()
            nav.Driver.get("https://google.com")            
            nav.Driver.find_element("textarea").send_keys(texto_filtrado[1] + "\n")                   
        except:
            print("Ocurrió un error en la busqueda...")