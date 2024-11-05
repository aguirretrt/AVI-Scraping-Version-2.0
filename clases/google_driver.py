from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from sbvirtualdisplay import Display
from seleniumbase import Driver

class GoogleDriver():       
    def __init__(self):
        
        self.virtual_display = Display(visible=1, size=(800, 600))            
        self.virtual_display.start()

        self.Driver = Driver(
            uc=True,
            headless=False,
            chromium_arg="--force-device-scale-factor=0.70",
        )
        self.Driver.maximize_window()
        self.wait = WebDriverWait(self.Driver, 5)
        
    
    def detener(self):
        self.Driver.quit()
        if self.virtual_display:
            self.virtual_display.stop()