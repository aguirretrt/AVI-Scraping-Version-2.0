from DrissionPage import ChromiumPage, ChromiumOptions
from sbvirtualdisplay import Display

from config import VISIBLE

class SeleniumDriver():       
    def __init__(self, visible=VISIBLE):   
        self.virtual_display = Display(visible=visible, size=(740, 470))
        self.virtual_display.start()

        self.opciones = ChromiumOptions().headless(False)
        self.opciones.set_argument("--blink-settings=imagesEnabled,false")
        self.opciones.set_argument("--disable-gpu")
        self.opciones.set_argument("--force-device-scale-factor=0.70")
        
        self.Driver = ChromiumPage(self.opciones) 
        self.Driver.set.window.full()
        
    def __del__(self):
        self.Driver.quit()
        self.virtual_display.stop()
    