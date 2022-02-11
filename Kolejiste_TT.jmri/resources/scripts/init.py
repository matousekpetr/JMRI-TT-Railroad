# Program se provadi pouze pri spusteni JMRI
# Definuji se vsechny promenne a provadi se nastaveni "Stuj" na navestidlech 

import jmri
import jarray

cekani_stanice = 10000
cekani_vyhybka = 2000
zpozdeni = 5000
zpozdeni_while = 1000

z5_petrov = memories.provideMemory("z5_petrov")
z3_petrov = memories.provideMemory("z3_petrov")
dir_sobotin = memories.provideMemory("dir_sobotin")
dir_zabreh = memories.provideMemory("dir_zabreh")

default_enable = sensors.provideSensor("IS8")
zabreh_kriz = sensors.provideSensor("IS9")

# Deklarace snimacu obsazeni do pole

XS = [ sensors.provideSensor("XS513"),
        sensors.provideSensor("XS513"),
        sensors.provideSensor("XS514"),
        sensors.provideSensor("XS515"),
        sensors.provideSensor("XS516"),
        sensors.provideSensor("XS517"),
        sensors.provideSensor("XS518"),
        sensors.provideSensor("XS519"),
        sensors.provideSensor("XS520"),
        sensors.provideSensor("XS521"),
        sensors.provideSensor("XS522"),
        sensors.provideSensor("XS523"),
        sensors.provideSensor("XS524"),
        sensors.provideSensor("XS525"),
        sensors.provideSensor("XS526"),
        sensors.provideSensor("XS527"),
        sensors.provideSensor("XS528"),
        sensors.provideSensor("XS529"),
        sensors.provideSensor("XS530"),
        sensors.provideSensor("XS531"),
        sensors.provideSensor("XS532"),
        sensors.provideSensor("XS533"),
        sensors.provideSensor("XS534"),
        sensors.provideSensor("XS535"),
        sensors.provideSensor("XS536"),
        sensors.provideSensor("XS537"),
        sensors.provideSensor("XS538"),
        sensors.provideSensor("XS539"),
        sensors.provideSensor("XS540"),
        sensors.provideSensor("XS541"),
        sensors.provideSensor("XS542"),
        sensors.provideSensor("XS543"),
        sensors.provideSensor("XS544"),
        sensors.provideSensor("XS545"),
        sensors.provideSensor("XS546"),
        sensors.provideSensor("XS547"),
        sensors.provideSensor("XS548"),
        sensors.provideSensor("XS549"),
        sensors.provideSensor("XS550"),
        sensors.provideSensor("XS551"),
        sensors.provideSensor("XS552")]    


# Deklarace alokacnich bloku do pole 

IS = [sensors.provideSensor("IS10"),
      sensors.provideSensor("IS10"),
      sensors.provideSensor("IS11"),
      sensors.provideSensor("IS12"),
      sensors.provideSensor("IS13"),
      sensors.provideSensor("IS14"),
      sensors.provideSensor("IS15"),
      sensors.provideSensor("IS16"),
      sensors.provideSensor("IS17"),
      sensors.provideSensor("IS18"),
      sensors.provideSensor("IS19"),
      sensors.provideSensor("IS20"),
      sensors.provideSensor("IS21"),
      sensors.provideSensor("IS22"),
      sensors.provideSensor("IS23"),
      sensors.provideSensor("IS24"),
      sensors.provideSensor("IS25"),
      sensors.provideSensor("IS26"),
      sensors.provideSensor("IS27"),
      sensors.provideSensor("IS28"),
      sensors.provideSensor("IS29"),
      sensors.provideSensor("IS30"),
      sensors.provideSensor("IS31"),
      sensors.provideSensor("IS32"),
      sensors.provideSensor("IS33"),
      sensors.provideSensor("IS34"),
      sensors.provideSensor("IS35"),
      sensors.provideSensor("IS36"),
      sensors.provideSensor("IS37"),
      sensors.provideSensor("IS38"),
      sensors.provideSensor("IS39"),
      sensors.provideSensor("IS40"),
      sensors.provideSensor("IS41"),
      sensors.provideSensor("IS42"),
      sensors.provideSensor("IS43"),
      sensors.provideSensor("IS44"),
      sensors.provideSensor("IS45"),
      sensors.provideSensor("IS46"),
      sensors.provideSensor("IS47"),
      sensors.provideSensor("IS48"),
      sensors.provideSensor("IS49")]     


# Deklarace vyhybek do pole

XT = [ turnouts.provideTurnout("XT200"),
       turnouts.provideTurnout("XT200"),
       turnouts.provideTurnout("XT201"),
       turnouts.provideTurnout("XT202"),
       turnouts.provideTurnout("XT203"),
       turnouts.provideTurnout("XT204"),
       turnouts.provideTurnout("XT205"),
       turnouts.provideTurnout("XT206"),
       turnouts.provideTurnout("XT207"),
       turnouts.provideTurnout("XT208"),
       turnouts.provideTurnout("XT209"),
       turnouts.provideTurnout("XT210"),
       turnouts.provideTurnout("XT211"),
       turnouts.provideTurnout("XT212"),
       turnouts.provideTurnout("XT213"),
       turnouts.provideTurnout("XT214"),
       turnouts.provideTurnout("XT215"),
       turnouts.provideTurnout("XT216"),
       turnouts.provideTurnout("XT217"),
       turnouts.provideTurnout("XT218"),
       turnouts.provideTurnout("XT219"),
       turnouts.provideTurnout("XT220")]    


# Deklarace navestidel do pole

NAV = [masts.getSignalMast("Nav-1-A"),
       masts.getSignalMast("Nav-1-A"),
       masts.getSignalMast("Nav-1-B"),
       masts.getSignalMast("Nav-1-C"),
       masts.getSignalMast("Nav-1-D"),
       masts.getSignalMast("Nav-1-E"),
       masts.getSignalMast("Nav-1-F"),
       masts.getSignalMast("Nav-1-G"),
       masts.getSignalMast("Nav-1-H"),
       masts.getSignalMast("Nav-1-I"),
       masts.getSignalMast("Nav-1-J"),
       masts.getSignalMast("Nav-1-K"),
       masts.getSignalMast("Nav-1-L"),
       masts.getSignalMast("Nav-1-M"),
       masts.getSignalMast("Nav-1-N"),
       masts.getSignalMast("Nav-1-O"),
       masts.getSignalMast("Nav-1-P"),
       masts.getSignalMast("Nav-2-A"),
       masts.getSignalMast("Nav-2-B"),
       masts.getSignalMast("Nav-2-C"),
       masts.getSignalMast("Nav-2-D"),
       masts.getSignalMast("Nav-2-E"),
       masts.getSignalMast("Nav-2-F"),
       masts.getSignalMast("Nav-2-G"),
       masts.getSignalMast("Nav-2-H"),
       masts.getSignalMast("Nav-2-I"),
       masts.getSignalMast("Nav-2-J"),
       masts.getSignalMast("Nav-2-K"),
       masts.getSignalMast("Nav-2-L"),
       masts.getSignalMast("Nav-2-M"),
       masts.getSignalMast("Nav-2-N"),
       masts.getSignalMast("Nav-2-O"),
       masts.getSignalMast("Nav-2-P"),
       masts.getSignalMast("Nav-3-A"),
       masts.getSignalMast("Nav-3-B"),
       masts.getSignalMast("Nav-3-C"),
       masts.getSignalMast("Nav-3-D"),
       masts.getSignalMast("Nav-3-E"),
       masts.getSignalMast("Nav-3-F"),
       masts.getSignalMast("Nav-3-G"),
       masts.getSignalMast("Nav-3-H"),
       masts.getSignalMast("Nav-3-I"),
       masts.getSignalMast("Nav-3-J"),
       masts.getSignalMast("Nav-3-K"),
       masts.getSignalMast("Nav-3-L")]   


# Deklarace ABS navestidel do pole

ABS = [masts.getSignalMast("Nav-AB-A"),
       masts.getSignalMast("Nav-AB-A"),
       masts.getSignalMast("Nav-AB-B"),
       masts.getSignalMast("Nav-AB-C"),
       masts.getSignalMast("Nav-AB-D"),
       masts.getSignalMast("Nav-AB-E"),
       masts.getSignalMast("Nav-AB-F"),
       masts.getSignalMast("Nav-AB-G"),
       masts.getSignalMast("Nav-AB-H")]   


# Deklarace osvetleni do pole 

OSV = [turnouts.provideTurnout("XT221"),
       turnouts.provideTurnout("XT221"),
       turnouts.provideTurnout("XT222"),
       turnouts.provideTurnout("XT223"),
       turnouts.provideTurnout("XT224"),
       turnouts.provideTurnout("XT225"),
       turnouts.provideTurnout("XT226")]    


# Deklarace radicu smeru

DIR_OUT =  [  sensors.provideSensor("IS100"),
              sensors.provideSensor("IS100"),
              sensors.provideSensor("IS103"),
              sensors.provideSensor("IS106"),
              sensors.provideSensor("IS109"),
              sensors.provideSensor("IS112"),
              sensors.provideSensor("IS115"),
              sensors.provideSensor("IS118"),
              sensors.provideSensor("IS121"),
              sensors.provideSensor("IS124"),
              sensors.provideSensor("IS127"),
              sensors.provideSensor("IS130"),
              sensors.provideSensor("IS133"),
              sensors.provideSensor("IS136")]

DIR_IN =   [  sensors.provideSensor("IS101"),
              sensors.provideSensor("IS101"),
              sensors.provideSensor("IS104"),
              sensors.provideSensor("IS107"),
              sensors.provideSensor("IS110"),
              sensors.provideSensor("IS113"),
              sensors.provideSensor("IS116"),
              sensors.provideSensor("IS119"),
              sensors.provideSensor("IS122"),
              sensors.provideSensor("IS125"),
              sensors.provideSensor("IS128"),
              sensors.provideSensor("IS131"),
              sensors.provideSensor("IS134"),
              sensors.provideSensor("IS137")]

DIR_STOP = [  sensors.provideSensor("IS102"),
              sensors.provideSensor("IS102"),
              sensors.provideSensor("IS105"),
              sensors.provideSensor("IS108"),
              sensors.provideSensor("IS111"),
              sensors.provideSensor("IS114"),
              sensors.provideSensor("IS117"),
              sensors.provideSensor("IS120"),
              sensors.provideSensor("IS123"),
              sensors.provideSensor("IS126"),
              sensors.provideSensor("IS129"),
              sensors.provideSensor("IS132"),
              sensors.provideSensor("IS135"),
              sensors.provideSensor("IS138")]


# Vychozi stavy

for i in range(len(OSV)):
       OSV[i].setState(CLOSED)

for i in range(len(NAV)):
       if (i == 13 or i == 15 or i == 27 or i == 28 or i == 29 or i == 32):
              NAV[i].setAspect("Posun zakázán".decode("UTF-8"))
       else:
              NAV[i].setAspect("Stůj".decode("UTF-8"))

for i in range(len(ABS)):
       ABS[i].setAspect("Stůj".decode("UTF-8"))

for i in range(len(DIR_STOP)):
       DIR_STOP[i].setKnownState(ACTIVE)       