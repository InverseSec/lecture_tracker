'''
script to note missed lectures and appropriate time to recover
'''
import re
import datetime

#defining file constants
snap = "snapshot.txt"#snapshot showing only relevant information for a person
log = "modulelog.txt"#longterm log for human
module = "modules.txt"#used to initialise the modules and their data (for computer)



class CSModule(object):
    NUM_FIELDS=6
    def __init__(self, priority = 0, name = "NA", plength = 0, llength = 0, pMissed = 0, lMissed = 0):
        self._priority = priority
        self._name = name
        self._pLength = plength
        self._lLength = llength
        self._pMissed = pMissed
        self._lMissed = lMissed

    def increasePriority(self):
        self._priority +=1

    def decreasePriority(self):
        self._priority -= 1
    def setPriority(self, p):
        self._priority  = p

    def increaseLectures(self, inc):
        self._lMissed += inc

    def increasePracticals(self, inc):
        self._pMissed += inc

    def decreaseLectures(self, dec):
        self._lMissed -= dec

    def decreasePracticals(self, dec):
        self._pMissed -= dec
        

class Program(object):
    def __init__(self, snapshot, log, modules):
        self._sFILE = snapshot
        self._lFILE = log
        self._mFILE = modules
        self._modules = []        

        self.initmodules()

    def initmodules(self):
        with open(self._mFILE, "r") as mds:
            d = mds.readlines()
            for counter in range(0, len(d), CSModule.NUM_FIELDS):
                args = []
                for index in range(counter, counter + CSModule.NUM_FIELDS):
                    args.append(d[index])
                self._modules.append(CSModule(int(args[0]),args[1][:len(args[1])-1],int(args[2]),int(args[3]),int(args[4]),int(args[5])))
                
    def normalisePriority(self):
        pass
        

    def dump(self,file,mode):
        now = datetime.datetime.now()
        with open(file, mode) as f:
            f.write(now.strftime("%Y-%m-%d %H:%M"))
            for module in self._modules:                    
                f.write("\n{0}\nPracticals Missed: {1}\nLectures Missed: {2}\nTotal Hours: {3}\n".format(module._name, module._lMissed, module._pMissed,
                                                                                                                (module._pLength*module._pMissed + module._lLength * module._lMissed )))
    def run(self):
        '''
user types a module, then lectures missed, then practicals missed. loops back to requesting a module
        '''
        with open(self._sFILE, "r") as f:
            dat = f.readlines()
            for line in dat:
                print(line)

        #more robust to create several patterns for the input string rather than one long and specific pattern
        names = [m._name for m in self._modules]
        pattern = "("  + "|".join(names) + ") (lecture|practical) ([0-9]+) (missed|caught)"
        print(pattern)
        while True:
            input_string = input("format to make an entry is [<module> <lecture|practical> <num> <missed|caught>] or type [quit] to quit\n")
            if input_string == "quit":
                break

            matches = re.match(pattern, input_string)
            if matches:
                for m in self._modules:
                    if matches.group(1) == m._name:
                        if matches.group(2) == "lecture":
                            if matches.group(4) == "missed":
                                m.increaseLectures(int(matches.group(3)))
                            else:
                                m.decreaseLectures(int(matches.group(3)))
                        else:
                            if matches.group(4) == "missed":
                                m.increasePracticals(int(matches.group(3)))
                            else:
                                m.decreasePracticals(int(matches.group(3)))
                        break
            else:
                print("error, input not in the correct format")
        self.dump(self._sFILE, "w")
        self.dump(self._lFILE, "a")

def main():
    p = Program(snap,log,module)
    p.run()

if __name__ == "__main__":
    main()
                            
                
