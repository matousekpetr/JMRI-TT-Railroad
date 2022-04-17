import jarray
import jmri

class traxx(dcc_automated_routes) :
   
    def init(self):

        self.rychlost_stanice = 0.4
        self.rychlost_jizda = 0.55
        self.rychlost_koridor = 0.6

        self.smer = True
        self.priority = 1

        self.zh_b_1 = 7500
        self.zh_b_2 = 7500
        self.zh_b_3 = 7500
        
        self.hz_a_1 = 7500
        self.hz_a_2 = 7500
        self.hz_a_3 = 7000

        self.h2wait = 8000
        self.h4wait = 9000
        self.z2wait = 9100
    
        self.adresa = 2
        self.sensor_1 = "IS62"
        self.sensor_2 = "IS63"
        
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

            self.zabreh_2_odj_b()
            self.autoblock_zh_b()
            self.hostejn_smer_b()
            self.autoblock_hz_a()
            self.zabreh_2_vj_a()

            self.auto_s.setKnownState(INACTIVE)
        
            if (self.auto.getKnownState() == ACTIVE):
                return 1
            else:
                return 0

traxx().start()


