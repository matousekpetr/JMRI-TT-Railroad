import jarray
import jmri
import random

class hlaseni(dcc_automated_routes) :
   
    def init(self):

        self.sensor_1 = "IS76"
        self.sensor_2 = "IS77"

        self.poradi = 0
        
        self.auto = sensors.provideSensor(self.sensor_1)
        self.auto_s = sensors.provideSensor(self.sensor_2)
        
        return

    def handle(self):
      
        if (self.auto_s.getKnownState() == ACTIVE):
            return 0
            
        else:
            self.auto_s.setKnownState(ACTIVE)

            self.poradi = random.randint(1, 11)

            if(self.poradi == 1):
                jmri.jmrit.Sound("hlaseni/Hlaseni_Zabreh1.wav").play()

            elif(self.poradi == 2):
                jmri.jmrit.Sound("hlaseni/Hlaseni_Zabreh2.wav").play()

            elif(self.poradi == 3):
                jmri.jmrit.Sound("hlaseni/Hlaseni_Zabreh3.wav").play()

            elif(self.poradi == 4):
                jmri.jmrit.Sound("hlaseni/Hlaseni_Zabreh4.wav").play()

            elif(self.poradi == 5):
                jmri.jmrit.Sound("hlaseni/Hlaseni_Zabreh5.wav").play()

            elif(self.poradi == 6):
                jmri.jmrit.Sound("hlaseni/Hlaseni_Zabreh6.wav").play()

            elif(self.poradi == 7): 
                jmri.jmrit.Sound("hlaseni/Hlaseni_Zabreh7.wav").play()

            elif(self.poradi == 8):
                jmri.jmrit.Sound("hlaseni/Hlaseni_Zabreh8.wav").play()

            elif(self.poradi == 9):
                jmri.jmrit.Sound("hlaseni/Hlaseni_Zabreh9.wav").play()

            elif(self.poradi == 10):
                jmri.jmrit.Sound("hlaseni/Hlaseni_Zabreh10.wav").play()

            elif(self.poradi == 11):                                  
                jmri.jmrit.Sound("hlaseni/Hlaseni_Zabreh11.wav").play()                          
            
            self.waitMsec(1000)
            self.auto_s.setKnownState(INACTIVE)          

            if (self.auto.getKnownState() == ACTIVE):
                return 1
            else:
                return 0

hlaseni().start()


