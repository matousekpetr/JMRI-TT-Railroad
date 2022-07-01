import jarray
import jmri

class bardotka(dcc_automated_routes):
   
    def init(self):

        self.rychlost_stanice = 0.3
        self.rychlost_jizda = 0.4
        self.rychlost_koridor = 0.45
        self.smer = True #True - neotočený, False - otočený
        self.priority = 1

        self.zh_a_1 = 6000
        self.zh_a_2 = 6000
        self.zh_a_3 = 6000
        
        self.hz_b_1 = 6000
        self.hz_b_2 = 6000
        self.hz_b_3 = 6000

        self.h3wait = 4600
        self.z1wait = 8500
        self.z2wait = 5500        
        self.z3wait = 6000
        self.z4wait = 4500         
        self.z5wait = 1700
       
        self.adresa = 10
        self.sensor_1 = "IS64"
        self.sensor_2 = "IS65"
        
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
            self.hostejn_3_odj_b()
            self.autoblock_hz_b()
            self.zabreh_smer_b_24351()
            self.autoblock_zh_a()
            self.hostejn_3_vj_a()            

            self.auto_s.setKnownState(INACTIVE)
        
            if (self.auto.getKnownState() == ACTIVE and powermanager.getPower() == jmri.PowerManager.ON):
                return 1
            else:
                return 0   
       
bardotka().start()

