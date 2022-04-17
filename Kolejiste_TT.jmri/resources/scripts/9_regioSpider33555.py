import jarray
import jmri

class regiospider(dcc_automated_routes) :
    
    def init(self):

        self.rychlost_stanice = 0.35
        self.rychlost_jizda = 0.5
        self.rychlost_koridor = 0.5
        self.smer = False
        self.priority = 1

        self.adresa = 9
        self.sensor_1 = "IS56"
        self.sensor_2 = "IS57"

        self.sobotin_wait = 4400
        
        self.petrov1_zabreh_wait = 3400
        self.petrov2_zabreh_wait = 3700
        self.petrov1_sobotin_wait = 3300
        self.petrov2_sobotin_wait = 3200

        self.petrov_zabreh_wait = 30000

        self.h1wait = 2000
        self.h3wait = 2000        

        self.z5wait = 3000
        self.z3wait = 3000
        self.z5akwait = 2200

        self.zvswait = 8000

        self.zh_a_1 = 3000
        self.zh_a_2 = 3000
        self.zh_a_3 = 3000
        
        self.hz_b_1 = 2000
        self.hz_b_2 = 3000
        self.hz_b_3 = 3000        

        self.pauza = 180000      
        
        self.throttle = self.getThrottle(self.adresa, False)
        
        self.auto = sensors.provideSensor(self.sensor_1)
        self.auto_s = sensors.provideSensor(self.sensor_2)
        
        return

    def handle(self):
      
        if (self.auto_s.getKnownState() == ACTIVE):
            return 0
            
        else:
            self.auto_s.setKnownState(ACTIVE)
            
            self.throttle.setF0(True)
            self.throttle.setF1(True)

            self.zabreh5ak_sobotin_zabreh5ak()

            self.auto_s.setKnownState(INACTIVE)
        
            if (self.auto.getKnownState() == ACTIVE):
                return 1
            else:
                return 0
   
regiospider().start()
