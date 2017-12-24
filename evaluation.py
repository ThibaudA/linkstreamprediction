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
                #
                # if sc._ranks[link] >=1:
            	# 	ev._TP+=1.
            	# 	if not times.has_key(link):
            	# 		evnewlink._TP+=1
            	# 	else:
        		# 		evrecurent._TP += sc._ranks[link]
        		# elif sc._ranks[link] > 0:
        		# 	ev._TP += sc._ranks[link]
        		# 	if not times.has_key(link):
        		# 		evnewlink._TP += sc._ranks[link]
        		# 	else:
        		# 		evrecurent._TP += sc._ranks[link]
        		# sc._ranks[link]=sc._ranks[link]-1.



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
                #
                # if sc._ranks[link] >=1:
            	# 	ev._TP+=1.
            	# 	if not times.has_key(link):
            	# 		evnewlink._TP+=1
            	# 	else:
        		# 		evrecurent._TP += sc._ranks[link]
        		# elif sc._ranks[link] > 0:
        		# 	ev._TP += sc._ranks[link]
        		# 	if not times.has_key(link):
        		# 		evnewlink._TP += sc._ranks[link]
        		# 	else:
        		# 		evrecurent._TP += sc._ranks[link]
        		# sc._ranks[link]=sc._ranks[link]-1.

    def updateScore(self, t_pred, t_obs,lambd):
            self.updateTP(t_pred, t_obs,lambd)
            self.updateFP(t_pred, t_obs,lambd)
            self.updateFN(t_pred, t_obs,lambd)


    def updateTP(self, t_pred, t_obs,lambd):
            self._TP = self._TP + np.tanh(1.0/(lambd*(abs(t_pred-t_obs))))

    def updateFN(self, t_pred, t_obs,lambd):
        if t_pred-t_obs > 0 :
            self._FN = self._FN + 1-np.tanh(1.0/(lambd*(t_pred-t_obs)))

    def updateFP(self, t_pred, t_obs,lambd):
        if t_pred-t_obs < 0 :
            self._FP = self._FP + 1-np.tanh(1.0/(-lambd*(t_pred-t_obs)))

    def updateTN(self, t_pred, t_obs,lambd):
        if t_pred-t_obs < 0 :
            self._TN = self._TN + 1-np.tanh(1.0/(-lambd*(t_pred-t_obs)))

    def endScore(self, t_pred, t_obs,lambd):
            self.updateTN(t_pred, t_obs,lambd)

    def printeval(self):
        sys.stdout.write("TP " + str(self._TP) + " \n")
        sys.stdout.write("FP " + str(self._FP) + " \n")
        sys.stdout.write("FN " + str(self._FN) + " \n")
        # sys.stdout.write("TN " + str(self._TN) + " \n")

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
                # s=s+str(min(ranks[link],len(times[link])))+","+str(-)max(ranks[link]-len(times[link]),0.))+","+str(max(len(times[link])-ranks[link],0.))
                s=s+str(min(ranks[link],len(times[link])))+","+str(max(ranks[link]-len(times[link]),0.))+","+str(max(len(times[link])-ranks[link],0.))
            else:
                s="0,"+ str(ranks[link])+",0"

            table.write(s + "\n")
        # print(self._TP,self._FN,self._FP)
        table.close()




    def CumulTp(self,ranks,times):
        data=[]

        for link in ranks:
            if link in times:
                data.append(min(ranks[link],len(times[link])))
        return data
