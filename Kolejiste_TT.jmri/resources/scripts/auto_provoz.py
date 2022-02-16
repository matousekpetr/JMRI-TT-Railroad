# Definuji se vsechny trasy a chovani pro automaticky provoz

import jmri
import jarray

# Trida pro definici automatizovanych zakladnich algoritmu a postupu
class dcc_basic_methods(jmri.jmrit.automat.AbstractAutomaton):

    def setTurnout(self, turnout, state):
        for i in range(len(turnout)):
            while(XT[turnout[i]].getState() != (state[i])):
                XT[turnout[i]].setState(state[i])
                self.waitMsec(cekani_vyhybka)

    def reserveBlock(self, block, withPriority = False, enable = default_enable, en = False):
        free = True
        a = 0
        if(withPriority):
            b = self.priority
        else:
            b = 1

        while a < b:
            self.waitMsec(zpozdeni_while)
            free = True
            while free:
                self.waitMsec(zpozdeni_while)
                free = False
                for i in range(len(block)):
                    if(XS[block[i]].getKnownState() == ACTIVE or IS[block[i]].getKnownState() == ACTIVE or powermanager.getPower() != jmri.PowerManager.ON or (enable.getKnownState() == ACTIVE and en == True)):
                        free = True
                        self.throttle.setSpeedSetting(0)
                        a = 0
                        break
                    else:
                        a = a+1

        for i in range(len(block)):
            IS[block[i]].setKnownState(ACTIVE)
        
        if en:
            enable.setKnownState(ACTIVE)
            
    def train(self, direction, speed, dir_inv):
        if dir_inv:
            if direction:
                self.throttle.setIsForward(False)
            else:
                self.throttle.setIsForward(True)
        else:
            self.throttle.setIsForward(direction)
        self.throttle.setSpeedSetting(speed)       

    def permission(self, number, direction):
        if(direction == 1):
            DIR_IN[number].setKnownState(ACTIVE)
        elif(direction == 0):
            DIR_OUT[number].setKnownState(ACTIVE)
        else:
            DIR_STOP[number].setKnownState(ACTIVE)       

    def blockFree(self, sensor, enable = default_enable, en = False):
        for i in range(len(sensor)):
            self.waitSensorActive(XS[sensor[i]])
            IS[sensor[i]].setKnownState(INACTIVE)
        
        if en:
            enable.setKnownState(INACTIVE)

    def stopWithDelay(self, time, stop):
        self.waitMsec(time)
        if stop:
            self.throttle.setSpeedSetting(0)

    def trainOut(self, turnouts, turnouts_states, blocks, permission, dir_inv, delay = 0, enable = default_enable, en = False):
        self.reserveBlock(blocks, True, enable, en)
        self.permission(permission, 0)
        self.setTurnout(turnouts, turnouts_states)
        self.train(self.smer, self.rychlost_stanice, dir_inv)
        self.blockFree(blocks, enable, en)
        self.permission(permission, 2)
        self.waitMsec(delay)

    def trainIn(self, turnouts, turnouts_states, blocks, permission, dir_inv, stop_time = 2000, stop = True, enable = default_enable, en = False):
        self.reserveBlock(blocks, False, enable, en)
        self.permission(permission, 1)
        self.setTurnout(turnouts, turnouts_states)
        self.train(self.smer, self.rychlost_stanice, dir_inv)
        self.blockFree(blocks, enable, en)
        self.permission(permission, 2)
        self.stopWithDelay(stop_time, stop)
        if stop:
            self.waitMsec(cekani_stanice)          

    def trainDeadTrack(self, turnouts, turnouts_states, blocks, dir_inv, stop_time):
        self.reserveBlock(blocks)
        self.setTurnout(turnouts, turnouts_states)
        self.train(self.smer, self.rychlost_stanice, dir_inv)
        self.blockFree(blocks)
        self.stopWithDelay(stop_time, True)

    def trainPass(self, turnouts1, turnouts_states1, blocks1, turnouts2, turnouts_states2, blocks2, permissionIn, permissionOut, dir_inv, stop_time = 2000, enable = default_enable):
        self.trainIn(turnouts1, turnouts_states1, blocks1, permissionIn, dir_inv, stop_time, False, enable)
        self.trainOut(turnouts2, turnouts_states2, blocks2, permissionOut, dir_inv, 0, enable)

    def trainAutoblock(self, blocks, dir_inv, stop_time1 = 1000, stop_time2 = 1000, stop_time3 = 1000):
        self.train(self.smer, self.rychlost_koridor, dir_inv)
        self.blockFree([blocks[0]])
        self.waitMsec(stop_time1)
        
        self.reserveBlock([blocks[1]])
        self.train(self.smer, self.rychlost_koridor, dir_inv)
        self.blockFree([blocks[1]])
        self.waitMsec(stop_time2)

        self.reserveBlock([blocks[2]])
        self.train(self.smer, self.rychlost_koridor, dir_inv)
        self.blockFree([blocks[2]])
        self.waitMsec(stop_time3)    

    def signal_logic(self, block, signal, target_signal):
        if (XS[block].getKnownState() == ACTIVE):
            signal.setAspect("Stůj".decode("UTF-8")) 
        
        elif (target_signal.getAspect() == ("Stůj".decode("UTF-8"))):
            signal.setAspect("Výstraha".decode("UTF-8"))
            
        else:
            signal.setAspect("Volno".decode("UTF-8"))
               
    def trackSelect(self, block, vj, odj):
        free = True
        while free:
            self.waitMsec(zpozdeni_while)
            free = True
            for i in range(len(block)):
                if(XS[block[i]].getKnownState() != ACTIVE and IS[block[i]].getKnownState() != ACTIVE and powermanager.getPower() == jmri.PowerManager.ON):
                    free = False 
                    a = i
                    break
                else:
                    self.throttle.setSpeedSetting(0)

        vj[a]()
        odj[a]()
        
        
# Trida pro definici konkretnich kolejovych useku s konkretnimi snimaci, radici a vyhybkami
class dcc_basic_routes(dcc_basic_methods):

    dir_sobotin = 0
    dir_zabreh  = 0
    zabreh_5 = False
    zabreh_3 = False

 # Zabreh - smer A
    # odjezd
    def zabreh_1_odj_a(self): self.trainOut([3, 1],       [CLOSED, CLOSED],           [15, 29], 1, False, 0)
    def zabreh_2_odj_a(self): self.trainOut([2, 1],       [CLOSED, THROWN],           [16, 29], 1, False, 0, zabreh_kriz, True)
    def zabreh_3_odj_a(self): self.trainOut([4, 3, 1],    [THROWN, THROWN, CLOSED],   [15, 29], 1, False, 0)
    def zabreh_4_odj_a(self): self.trainOut([2, 1],       [THROWN, THROWN],           [16, 29], 1, False, 0, zabreh_kriz, True)
    def zabreh_5_odj_a(self): self.trainOut([4, 3, 1],    [CLOSED, THROWN, CLOSED],   [15, 29], 1, False, 0)
    # prijezd
    def zabreh_1_vj_a(self): self.trainIn([1, 3],         [THROWN, CLOSED],           [15, 5],    2, True, self.z1wait, True, zabreh_kriz, True)
    def zabreh_2_vj_a(self): self.trainIn([1, 2],         [CLOSED, CLOSED],           [16, 4],    2, True, self.z2wait, True)
    def zabreh_3_vj_a(self): self.trainIn([1, 3, 4],      [THROWN, THROWN, THROWN],   [15, 6],    2, True, self.z3wait, True, zabreh_kriz, True)
    def zabreh_4_vj_a(self): self.trainIn([1, 2],         [CLOSED, THROWN],           [16, 3],    2, True, self.z4wait, True)      
    def zabreh_5_vj_a(self): self.trainIn([1, 3, 4],      [THROWN, THROWN, CLOSED],   [15, 7],    2, True, self.z5wait, True, zabreh_kriz, True)
    # prujezd
    def zabreh_1_pjz(self): self.trainPass([1, 3],        [THROWN, CLOSED],           [15, 5],    [11, 10, 9],  [CLOSED, THROWN, CLOSED],   [34, 33, 28], True, self.z1wait) 
               
 # Zabreh - smer B
    # odjezd
    def zabreh_1_odj_b(self): self.trainOut([11, 10, 9],  [CLOSED, THROWN, CLOSED],   [34, 33, 28], 4, True)
    def zabreh_2_odj_b(self): self.trainOut([14, 10, 9],  [CLOSED, CLOSED, CLOSED],   [33, 28], 4, True)
    def zabreh_3_odj_b(self): self.trainOut([16, 15, 11, 10, 9],  [CLOSED, THROWN, THROWN, THROWN, CLOSED],   [37, 34, 28], 4, True)
    def zabreh_4_odj_b(self): self.trainOut([14, 10, 9],  [THROWN, CLOSED, CLOSED],   [33, 28], 4, True)
    def zabreh_5_odj_b(self): self.trainOut([17, 12,  16, 15, 11, 10, 9],    [CLOSED, THROWN, THROWN, THROWN, THROWN, THROWN, CLOSED], [37, 34, 28], 4, True)
    # vjezd
    def zabreh_1_vj_b(self): self.trainIn([9, 10, 11],    [CLOSED, CLOSED, CLOSED],   [34, 5],    3, False, self.z1wait)
    def zabreh_2_vj_b(self): self.trainIn([9, 10, 14],    [THROWN, CLOSED, CLOSED],   [33, 4],    3, False, self.z2wait)
    def zabreh_3_vj_b(self): self.trainIn([9, 10, 11, 15, 16], [CLOSED, CLOSED, THROWN, THROWN, CLOSED],   [34, 37, 6],    3, False, self.z3wait)
    def zabreh_4_vj_b(self): self.trainIn([9, 10, 14],     [THROWN, CLOSED, THROWN],           [33, 3],    3, False, self.z4wait)      
    def zabreh_5_vj_b(self): self.trainIn([9, 10, 11, 15, 16, 12, 17],[CLOSED, CLOSED, THROWN, THROWN, THROWN, THROWN, CLOSED],   [34, 37, 7],    3, False, self.z5wait)   
    # prujezd

 # Zabreh - smer C
    #odjezd
    def zabreh_3_odj_c(self): self.trainOut([16, 15, 17], [CLOSED, CLOSED, CLOSED], [37, 40, 18], 9, True)
    def zabreh_5_odj_c(self): self.trainOut([17, 12, 16, 15], [CLOSED, THROWN, THROWN, CLOSED], [37, 40, 18], 9, True)
    #prijezd
    def zabreh_3_vj_c(self): self.trainIn([15, 16], [CLOSED, CLOSED], [40, 37, 6], 9, False, self.z3wait)
    def zabreh_5_vj_c(self): self.trainIn([15, 16, 12, 17], [CLOSED, THROWN, THROWN, CLOSED], [40, 37, 7], 9, False, self.z5wait)
 
 # Zabreh - smer D
    #odjezd
    def zabreh_5_odj_d(self): self.trainOut([17], [THROWN], [38], 9, True)
    #prijezd
    def zabreh_5_vj_d(self): self.trainIn([17], [THROWN], [7], 9, False, self.z5wait)

 # Zabreh - kuse koleje
    #odjezd
    def zabreh_4k_odj(self): self.trainDeadTrack([2], [CLOSED], [3], True, self.z4wait_k)
    def zabreh_5ak_odj(self): self.trainDeadTrack([13, 12, 17], [CLOSED, CLOSED, CLOSED], [37, 7], False, self.z5wait)
    def zabreh_5bk_odj(self): self.trainDeadTrack([13, 12, 17], [THROWN, CLOSED, CLOSED], [37, 7], False, self.z5wait)
    #prijezd
    def zabreh_4k_vj(self): self.trainDeadTrack([2], [CLOSED], [8], False, self.z4kwait)
    def zabreh_5ak_vj(self): self.trainDeadTrack([13, 12, 17], [CLOSED, CLOSED, CLOSED], [37, 35], True, self.z5akwait)
    def zabreh_5bk_vj(self): self.trainDeadTrack([13, 12, 17], [THROWN, CLOSED, CLOSED], [37, 36], True, self.z5bkwait)

 # Hostejn - smer A
    # odjezd
    def hostejn_2_odj_a(self): self.trainOut([5], [CLOSED], [2], 8, True)
    def hostejn_4_odj_a(self): self.trainOut([5], [THROWN], [2], 8, True)
    # vjezd
    def hostejn_1_vj_a(self): self.trainIn([6], [CLOSED], [11], 7, False, self.h1wait)
    def hostejn_3_vj_a(self): self.trainIn([6], [THROWN], [12], 7, False, self.h3wait)
    # prujezd
    def hostejn_1_pjz_a(self): self.trainPass([6], [CLOSED], [11], [7], [CLOSED], [25], 7, 5, False,  self.h1wait)          
    def hostejn_3_pjz_a(self): self.trainPass([6], [THROWN], [12], [7], [THROWN], [25], 7, 5, False, self.h3wait)

 # Hostejn - smer B
    # odjezd
    def hostejn_1_odj_b(self): self.trainOut([7], [CLOSED], [25], 5, False)
    def hostejn_3_odj_b(self): self.trainOut([7], [THROWN], [25], 5, False)
    # vjezd
    def hostejn_2_vj_b(self): self.trainIn([8], [CLOSED], [10], 6, True, self.h2wait)
    def hostejn_4_vj_b(self): self.trainIn([8], [THROWN], [9], 6, True, self.h4wait)
    # prujezd 
    def hostejn_2_pjz(self): self.trainPass([8], [CLOSED], [10], [5], [CLOSED], [2], True, self.h2wait)          
    def hostejn_4_pjz(self): self.trainPass([8], [THROWN], [9], [5], [THROWN], [2], True, self.h4wait)

 # Trat
    def autoblock_zh_a(self): self.trainAutoblock([29, 31, 1], False, self.zh_a_1, self.zh_a_2, self.zh_a_3)
    def autoblock_hz_a(self): self.trainAutoblock([2, 32, 30], True, self.hz_a_1, self.hz_a_2, self.hz_a_3)
    def autoblock_zh_b(self): self.trainAutoblock([28, 23, 26], True, self.zh_b_1, self.zh_b_2, self.zh_b_3)
    def autoblock_hz_b(self): self.trainAutoblock([25, 24, 27], False, self.hz_b_1, self.hz_b_2, self.hz_b_3)


 # Petrov - smer Zabreh
    #odjezd
    def petrov_1_odj_z(self): self.trainOut([19], [THROWN], [18], 10, False, self.petrov_zabreh_wait)
    def petrov_2_odj_z(self): self.trainOut([19], [CLOSED], [18], 10, False, self.petrov_zabreh_wait)
    #vjezd
    def petrov_1_vj_z(self): self.trainIn([19], [THROWN], [14], 10, True, self.petrov1_zabreh_wait)
    def petrov_2_vj_z(self): self.trainIn([19], [CLOSED], [13], 10, True, self.petrov2_zabreh_wait)

 # Petrov - smer Sobotin
    #odjezd
    def petrov_1_odj_s(self): self.trainOut([18], [CLOSED], [17], 11, True)
    def petrov_2_odj_s(self): self.trainOut([18], [THROWN], [17], 11, True)
    #vjezd
    def petrov_1_vj_s(self): self.trainIn([18], [CLOSED], [14], 11, False, self.petrov1_sobotin_wait)
    def petrov_2_vj_s(self): self.trainIn([18], [THROWN], [13], 11, False, self.petrov2_sobotin_wait)

 # Petrov - kuse koleje
    #odjezd
    def petrov_2k_odj(self): self.trainDeadTrack([18], [CLOSED], [13], False, self.petrov2_sobotin_wait)
    #prijezd
    def petrov_2k_vj(self): self.trainDeadTrack([18], [CLOSED], [19], True, self.petrov2k_wait)

 # Sobotin
    #odjezd
    def sobotin_1_odj(self): self.trainOut([20], [THROWN], [17], 13, False)
    def sobotin_2ak_odj(self): self.trainOut([21, 20], [CLOSED, CLOSED], [20, 17], 13, False)
    def sobotin_2bk_odj(self): self.trainOut([21, 20], [THROWN, CLOSED], [20, 17], 13, False)
    #vjezd
    def sobotin_1_vj(self): self.trainIn([20], [THROWN], [39], 13, True, self.sobotin_wait)
    def sobotin_2ak_vj(self): self.trainIn([21, 20], [CLOSED, CLOSED], [20, 21], 13, True, self.sobotin2ak_wait)
    def sobotin_2bk_vj(self): self.trainIn([21, 20], [THROWN, CLOSED], [20, 22], 13, True, self.sobotin2bk_wait)

 # Autoblok navestidla

    def autoblock_signals(self):  
        self.signal_logic(32, ABS[1], ABS[2])
        self.signal_logic(30, ABS[2], NAV[37])
        
        self.signal_logic(31, ABS[3], ABS[4])
        self.signal_logic(1, ABS[4], NAV[33])

        self.signal_logic(23, ABS[5], ABS[6])
        self.signal_logic(26, ABS[6], NAV[39])

        self.signal_logic(24, ABS[7], ABS[8])
        self.signal_logic(27, ABS[8], NAV[4])

    def zabreh_sobotin_zabreh(self, kusa_odjezd, kusa_vjezd, odj_z, vj_z, outOfDeadTrack, track):

        while(dir_sobotin > 1 or track == True):
            self.waitMsec(zpozdeni_while)

        track = True
        dir_sobotin = dir_sobotin + 1

        if(outOfDeadTrack == True):
            kusa_odjezd()

        odj_z()
        track = False

        self.petrov_2_vj_z()
        self.petrov_2_odj_s()
        self.sobotin_1_vj()
        self.sobotin_1_odj()
        self.petrov_1_vj_s()
        dir_sobotin = dir_sobotin - 1
        while(track == True):
            self.waitMsec(zpozdeni_while)
        track = True

        self.petrov_1_odj_z()
        vj_z()
        
        if(outOfDeadTrack == True):
            kusa_vjezd()

        track = False        


# Trida pro vyber volnych koleji na konkretnich usecich s postupnou prioritou, nadstavba dcc_basic_routes
class dcc_automated_routes(dcc_basic_routes):

# Hostejn

    def hostejn_smer_a(self): self.trackSelect( 
        [   11, 12],   
        [   self.hostejn_1_vj_a, 
            self.hostejn_3_vj_a],                     
        
        [   self.hostejn_1_odj_b, 
            self.hostejn_3_odj_b])

    def hostejn_smer_a_31(self): self.trackSelect( 
        [   12, 11],   
        [   self.hostejn_3_vj_a, 
            self.hostejn_1_vj_a],                     
        
        [   self.hostejn_3_odj_b, 
            self.hostejn_1_odj_b])

    def hostejn_smer_b(self): self.trackSelect( 
        [   10, 9],   
        [   self.hostejn_2_vj_b, 
            self.hostejn_4_vj_b],                     
        
        [   self.hostejn_2_odj_a, 
            self.hostejn_4_odj_a])            
   

# Zabreh
  
    def zabreh_smer_b_135(self): self.trackSelect(  
        [   5, 6, 7],  
        [   self.zabreh_1_vj_b, 
            self.zabreh_3_vj_b, 
            self.zabreh_5_vj_b],   
            
        [   self.zabreh_1_odj_a, 
            self.zabreh_3_odj_a, 
            self.zabreh_5_odj_a])

    def zabreh_smer_b_all(self): self.trackSelect(  
        [   5, 6, 7, 4, 3],  
        [   self.zabreh_1_vj_b, 
            self.zabreh_3_vj_b, 
            self.zabreh_5_vj_b, 
            self.zabreh_2_vj_b, 
            self.zabreh_4_vj_b],  
            
        [   self.zabreh_1_odj_a, 
            self.zabreh_3_odj_a,
            self.zabreh_5_odj_a, 
            self.zabreh_2_odj_a,  
            self.zabreh_4_odj_a])

    def zabreh_smer_b_24351(self): self.trackSelect(  
        [   4, 3, 6, 7, 5],  
        [   self.zabreh_2_vj_b, 
            self.zabreh_4_vj_b, 
            self.zabreh_3_vj_b, 
            self.zabreh_5_vj_b, 
            self.zabreh_1_vj_b],  
            
        [   self.zabreh_2_odj_a, 
            self.zabreh_4_odj_a,
            self.zabreh_3_odj_a, 
            self.zabreh_5_odj_a,  
            self.zabreh_1_odj_a])

    def zabreh_smer_b_245(self): self.trackSelect(  
        [   4, 3, 7],  
        [   self.zabreh_2_vj_b, 
            self.zabreh_4_vj_b, 
            self.zabreh_5_vj_b],  
            
        [   self.zabreh_2_odj_a, 
            self.zabreh_4_odj_a,
            self.zabreh_5_odj_a])

    def zabreh_smer_a_124(self): self.trackSelect(  
        [   5, 4, 3],  
        [   self.zabreh_1_vj_a, 
            self.zabreh_2_vj_a, 
            self.zabreh_4_vj_a],  
                                                                         
        [   self.zabreh_1_odj_b, 
            self.zabreh_2_odj_b,
            self.zabreh_4_odj_b])

    def zabreh_smer_a_13524(self): self.trackSelect(  
        [   5, 6, 7, 4, 3],  
        [   self.zabreh_1_vj_a, 
            self.zabreh_3_vj_a, 
            self.zabreh_5_vj_a,
            self.zabreh_2_vj_a,
            self.zabreh_4_vj_a],  
                                                                         
        [   self.zabreh_1_odj_b, 
            self.zabreh_3_odj_b,
            self.zabreh_5_odj_b,
            self.zabreh_2_odj_b,
            self.zabreh_4_odj_b])

    def zabreh_smer_a_1324(self): self.trackSelect(  
        [   5, 6, 4, 3],  
        [   self.zabreh_1_vj_a, 
            self.zabreh_3_vj_a, 
            self.zabreh_2_vj_a,
            self.zabreh_4_vj_a],  
                                                                         
        [   self.zabreh_1_odj_b, 
            self.zabreh_3_odj_b,
            self.zabreh_2_odj_b,
            self.zabreh_4_odj_b])

# Petrov

    def petrov_s_z(self): self.trackSelect(     [14, 13],   [self.petrov_1_vj_s, self.petrov_2_vj_s],                       [self.petrov_1_odj_z, self.petrov_2_odj_z])
    def petrov_z_s(self): self.trackSelect(     [13, 14],   [self.petrov_2_vj_z, self.petrov_1_vj_z],                       [self.petrov_2_odj_s, self.petrov_1_odj_s])

    def zabreh5ak_sobotin_zabreh5ak(self):  self.zabreh_sobotin_zabreh(self.zabreh_5ak_odj, self.zabreh_5ak_vj, self.zabreh_5_odj_c, self.zabreh_5_vj_c, True, zabreh_5)
    def zabreh5bk_sobotin_zabreh5bk(self):  self.zabreh_sobotin_zabreh(self.zabreh_5bk_odj, self.zabreh_5bk_vj, self.zabreh_5_odj_c, self.zabreh_5_vj_c, True, zabreh_5)
    def zabreh5_sobotin_zabreh5(self):      self.zabreh_sobotin_zabreh(self.zabreh_5bk_odj, self.zabreh_5bk_vj, self.zabreh_5_odj_c, self.zabreh_5_vj_c, False, zabreh_5)
    def zabreh3_sobotin_zabreh3(self):      self.zabreh_sobotin_zabreh(self.zabreh_5bk_odj, self.zabreh_5bk_vj, self.zabreh_3_odj_c, self.zabreh_3_vj_c, False, zabreh_3)