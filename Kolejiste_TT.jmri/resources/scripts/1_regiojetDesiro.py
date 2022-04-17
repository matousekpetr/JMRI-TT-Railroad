import jarray
import jmri

class regiojet(dcc_automated_routes) :
   
    def init(self):
        
        self.rychlost_stanice = 0.6
        self.rychlost_jizda = 0.7
        self.rychlost_koridor = 0.8

        self.smer = False #True - neotočený, False - otočený
        self.priority = 1

        self.zh1 = 7500
        self.zh2 = 7500
        self.zh3 = 7500
        
        self.hz1 = 7500
        self.hz2 = 7500
        self.hz3 = 1200        
        
        self.adresa = 1
        self.sensor_1 = "IS54"
        self.sensor_2 = "IS55"

        self.sobotin_wait = 2400
        
        self.petrov1_zabreh_wait = 2700
        self.petrov2_zabreh_wait = 2900
        self.petrov1_sobotin_wait = 2200
        self.petrov2_sobotin_wait = 2400

        self.petrov_zabreh_wait = 10000

        self.petrov2k_wait = 2620

        self.z3wait = 4200
        self.z5wait = 3000
        self.zvswait = 6500

        self.h3wait = 4500

        self.throttle = self.getThrottle(self.adresa, False)
        
        self.auto = sensors.provideSensor(self.sensor_1)
        self.auto_s = sensors.provideSensor(self.sensor_2)
        return

    def handle(self):
      
        if (self.auto_s.getKnownState() == ACTIVE):
            return 0
            
        else:
            self.auto_s.setKnownState(ACTIVE)

            self.sobotin_1_odj()
            self.petrov_s_z()
            self.zabreh_3_vj_c()
            self.zabreh_3_odj_c()
            self.petrov_z_s()
            self.sobotin_1_vj()

            self.auto_s.setKnownState(INACTIVE)

            if (self.auto.getKnownState() == ACTIVE):
                return 1  
            else:
                return 0


regiojet().start()
