import jarray
import jmri

class regiojet_vectron(dcc_automated_routes) :
   
    def init(self):

        self.rychlost_stanice = 0.25
        self.rychlost_jizda = 0.4
        self.rychlost_koridor = 0.5

        self.smer = True
        self.priority = 1

        self.zh_b_1 = 5000
        self.zh_b_2 = 5000
        self.zh_b_3 = 5000
        
        self.hz_a_1 = 5000
        self.hz_a_2 = 5000
        self.hz_a_3 = 5000

        self.h2wait = 7000
        self.h4wait = 8000
        self.z4wait = 9000
    
        self.adresa = 7
        self.sensor_1 = "IS58"
        self.sensor_2 = "IS59"
        
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

            self.zabreh_4_odj_b()
            self.autoblock_zh_b()
            self.hostejn_smer_b()
            self.autoblock_hz_a()
            self.zabreh_4_vj_a()
            self.auto_s.setKnownState(INACTIVE)
        
            if (self.auto.getKnownState() == ACTIVE):
                return 1
            else:
                return 0

regiojet_vectron().start()


