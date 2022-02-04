import jarray
import jmri
    
class on_off(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        return

    def handle(self):

        if(sensors.provideSensor("IS1").getState() == ACTIVE):
            powermanager.setPower(jmri.PowerManager.OFF)
 
        elif(sensors.provideSensor("IS1").getState() == INACTIVE):
            powermanager.setPower(jmri.PowerManager.ON)

        return 0

on_off().start()