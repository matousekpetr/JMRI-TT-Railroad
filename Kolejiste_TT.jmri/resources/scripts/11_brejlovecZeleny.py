import jarray
import jmri

class brejlovec_zeleny(dcc_automated_routes):
    
    def init(self):
        
        self.rychlost_stanice = 0.4
        self.rychlost_jizda = 0.6
        self.rychlost_koridor = 0.65
        self.smer = False
        self.priority = 5

        self.zh_a_1 = 7000
        self.zh_a_2 = 9000
        self.zh_a_3 = 10000
        
        self.hz_b_1 = 5000
        self.hz_b_2 = 5000
        self.hz_b_3 = 5000

        self.h1wait = 6600
        self.z1wait = 10900

        self.adresa = 11
        self.sensor_1 = "IS50"
        self.sensor_2 = "IS51"
        
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

            self.zabreh_1_odj_a()
            self.autoblock_zh_a()
            self.hostejn_1_vj_a()
            self.hostejn_1_odj_b()
            self.autoblock_hz_b()
            self.zabreh_1_vj_b()
            
            self.auto_s.setKnownState(INACTIVE)
        
            if (self.auto.getKnownState() == ACTIVE and powermanager.getPower() == jmri.PowerManager.ON):
                return 1
            else:
                return 0

brejlovec_zeleny().start()
