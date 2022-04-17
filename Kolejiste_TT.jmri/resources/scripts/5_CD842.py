import jarray
import jmri

class cd_842(dcc_automated_routes) :
   
    def init(self):
        
        self.rychlost_stanice = 0.4
        self.rychlost_jizda = 0.6
        self.rychlost_koridor = 0.7

        self.smer = False #True - neotočený, False - otočený
        self.priority = 1

        self.zh_b_1 = 7000
        self.zh_b_2 = 7000
        self.zh_b_3 = 7000
        
        self.hz_a_1 = 7000
        self.hz_a_2 = 7000
        self.hz_a_3 = 7000

        self.adresa = 5
        self.sensor_1 = "IS66"
        self.sensor_2 = "IS67"

        self.z1wait = 8000
        self.z2wait = 8000
        self.z3wait = 8000
        self.z4wait = 7000
        self.z5wait = 6500
        self.z5bkwait = 2100

        self.h1wait = 1500
        self.h2wait = 6500
        self.h4wait = 7000
        
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

            self.hostejn_2_odj_a()
            self.autoblock_hz_a()
            self.zabreh_smer_a_13524()
            self.autoblock_zh_b()
            self.hostejn_2_vj_b()
            
            self.auto_s.setKnownState(INACTIVE)
        
            if (self.auto.getKnownState() == ACTIVE):
                return 1
                
            else:
                return 0
    
cd_842().start()
