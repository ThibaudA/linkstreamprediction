import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib import mlab


class evaluate:

    def __init__(self):
        self._TP = 0.
        self._FP = 0.
        self._FN = 0.
        self._TN = 0.
        self._Pr = -1.
        self._Rc = -1.
        self._F = -1.


    def calculateScoreFromTimeAggreg(self,ranks,timeaggr):
        for link in ranks:
            if link in timeaggr:
                self._TP += min(ranks[link],timeaggr[link])
                self._FP += max(ranks[link]-timeaggr[link],0.)
                self._FN += max(timeaggr[link]-ranks[link],0.)
            else:
                self._FP += ranks[link]
        # print(self._TP,self._FN,self._FP)

        if (self._TP+self._FP)!=0 and (self._TP+self._FN) !=0:
            if self._TP!=0:
                self._Pr = self._TP/(self._TP+self._FP)
                self._Rc = self._TP/(self._TP+self._FN)
                self._F = 2.*self._Pr*self._Rc/(self._Pr+self._Rc)
            else:
                self._Pr = 0
                self._Rc = 0
                self._F  = 0


        if self._TP < 0 or self._FP <0  or self._FN < 0:
            sys.stderr.write(str(self._TP) + " \n")
            sys.stderr.write(str(self._FP) + " \n")
            sys.stderr.write(str(self._FN) + " \n")



    def calculateScore(self,ranks,times):
        for link in ranks:
            if link in times:
                self._TP += min(ranks[link],len(times[link]))
                self._FP += max(ranks[link]-len(times[link]),0.)
                self._FN += max(len(times[link])-ranks[link],0.)
            else:
                self._FP += ranks[link]
        # print(self._TP,self._FN,self._FP)

        if (self._TP+self._FP)!=0 and (self._TP+self._FN) !=0:
            if self._TP!=0:
                self._Pr = self._TP/(self._TP+self._FP)
                self._Rc = self._TP/(self._TP+self._FN)
                self._F = 2.*self._Pr*self._Rc/(self._Pr+self._Rc)
            else:
                self._Pr = 0
                self._Rc = 0
                self._F  = 0


        if self._TP < 0 or self._FP <0  or self._FN < 0:
            sys.stderr.write(str(self._TP) + " \n")
            sys.stderr.write(str(self._FP) + " \n")
            sys.stderr.write(str(self._FN) + " \n")


    def printeval(self):
        sys.stdout.write("TP " + str(self._TP) + " \n")
        sys.stdout.write("FP " + str(self._FP) + " \n")
        sys.stdout.write("FN " + str(self._FN) + " \n")

        sys.stdout.write("Precision " + str(self._Pr) + " \n")
        sys.stdout.write("Recall "    + str(self._Rc) + " \n")
        sys.stdout.write("F score "   + str(self._F) + " \n")

    @staticmethod
    def extractQualitybypair(ranks,times,filename):
        table = open(filename, 'w')

        for link in ranks:
            for u in link:
                table.write(str(u) + " ")
            s=""
            if link in times:
                s=s+str(min(ranks[link],len(times[link])))+","+str(max(ranks[link]-len(times[link]),0.))+","+str(max(len(times[link])-ranks[link],0.))
            else:
                s="0,"+ str(ranks[link])+",0"

            table.write(s + "\n")
        table.close()
