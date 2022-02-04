import jarray
import jmri

class hektor(dcc_automated_routes) :
    
    def init(self):

        self.rychlost_stanice = 0.5
        self.rychlost_jizda = 0.6
        self.rychlost_koridor = 0.8
        self.priority = 1

        self.adresa = 13
        self.sensor_1 = "IS68"
        self.sensor_2 = "IS69"

        self.smer = False

        self.zh_b_1 = 7000
        self.zh_b_2 = 7000
        self.zh_b_3 = 7000
        
        self.hz_a_1 = 7000
        self.hz_a_2 = 7000
        self.hz_a_3 = 7000

        self.h4wait = 9000
        self.z1wait = 9000
        self.z2wait = 9000
        self.z3wait = 9000
        self.z4wait = 10000
        self.z5wait = 9000

        
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

            self.hostejn_4_odj_a()
            self.autoblock_hz_a()
            self.zabreh_smer_a_1324()
            self.autoblock_zh_b()
            self.hostejn_4_vj_b()
            
            self.auto_s.setKnownState(INACTIVE)
        
            if (self.auto.getKnownState() == ACTIVE):
                return 1
            else:
                return 0


       
hektor().start()
