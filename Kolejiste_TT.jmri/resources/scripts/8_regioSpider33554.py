import jarray
import jmri

class regiospider2(dcc_automated_routes) :
    
    def init(self):

        self.rychlost_stanice = 0.75
        self.rychlost_jizda = 0.9
        self.rychlost_koridor = 0.95
        self.smer = False
        self.priority = 1

        self.adresa = 8
        self.sensor_1 = "IS70"
        self.sensor_2 = "IS71"

        self.sobotin_wait = 2400
        self.s2akwait = 1000
        
        self.petrov1_zabreh_wait = 1500
        self.petrov2_zabreh_wait = 2000
        self.petrov1_sobotin_wait = 1700
        self.petrov2_sobotin_wait = 1400

        self.petrov_zabreh_wait = 10000

        self.zh_a_1 = 3000
        self.zh_a_2 = 3000
        self.zh_a_3 = 3000
        
        self.hz_b_1 = 2000
        self.hz_b_2 = 3000
        self.hz_b_3 = 3000   

        self.h1wait = 2000
        self.h3wait = 2000                     

        self.z5wait = 3000
        self.z5bkwait = 1500

        self.zvswait = 6500

        self.pauza = 120000
        
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

            self.zabreh5bk_sobotin_zabreh5bk()           

            self.auto_s.setKnownState(INACTIVE)
        
            if (self.auto.getKnownState() == ACTIVE):
                return 1
            else:
                return 0
                
regiospider2().start()