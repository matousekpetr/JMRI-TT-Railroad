import jarray
import jmri

class abs_navestidla(dcc_automated_routes) :
   
    def handle(self):

        self.autoblock_signals()
        self.waitMsec(500)
        return 1

abs_navestidla().start()