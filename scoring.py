from scipy import integrate
import numpy as np
import sys
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import operator
from evaluation import evaluate
import itertools
import random
class score:

    def __init__(self):
        self._pair_set = set()
        self._pair = dict()
        self._ranks = dict()
        self._maxByMetric = dict()


    def addPair(self,c):
        if not c in self._pair_set:
            self._pair[c]=dict()
            self._pair_set.add(c)


    def resetPairs(self):
        self._pair_set = set()
        self._pair=dict()

    def resetRanks(self):
        self._ranks=dict()

    def addFunction(self,c,name,fct):
	       self._pair[c][name]=fct


    def integrateMetrics(self,t1,t2): #using the function from metrics integrate
        for c in self._pair:
            for ID in self._pair[c]:
                #maybe a better integration?
                self._pair[c][ID] = integrate.quad(self._pair[c][ID],t1,t2)[0]

    def setMaxByMetric(self):
        for c in self._pair:
            for ID in self._pair[c]:
                if not ID in self._maxByMetric:
                    self._maxByMetric[ID]=0
                # print ID, self._maxByMetric[ID],self._pair[c][ID]
                self._maxByMetric[ID]=max(self._maxByMetric[ID],self._pair[c][ID])

    def normalizeMetrics(self):
        for c in self._pair:
            for ID in self._pair[c]:
                #normalize each metric with the max for the metric
                if self._maxByMetric[ID]!=0:
                    self._pair[c][ID]=self._pair[c][ID]/self._maxByMetric[ID]
        for ID in self._maxByMetric:
            if self._maxByMetric[ID]==0:
                sys.stderr.write("Warning: Max "+ID+"=0 \n")


    def normalizeranksbyintegral(self,linksinT):
        sumarea=0.
        for r in self._ranks: #nb of link for each unit of area (from integrate)
            sumarea= sumarea+self._ranks[r]
        if sumarea!=0:
            linkbyarea = linksinT / sumarea
        else:
            linkbyarea = 0
        hist=[]
        sumpredlink=0
        for r in self._ranks:
            self._ranks[r]=self._ranks[r]*linkbyarea

    def rankPairs(self,t1,t2,confmetrics):
        #print self._pair
        #combine the scores with parameters in confmetrics
        for c in self._pair:
            self._ranks[c] = 0
            for ID in self._pair[c]:
                if confmetrics[ID] is not None:
                    self._ranks[c] += confmetrics[ID]*self._pair[c][ID]
                else:
                    self._ranks[c] += self._pair[c][ID]


    def gridsearch(self,tstart,tend,tmesure,tendtraining,nb_links,trainingtimes,confmetrics):
        MFscore=-1.
        #ready to check various combinaison
        nbcalcul=len(list(itertools.product(*confmetrics.values())))
        cptcalcul = 0
        for i in itertools.product(*confmetrics.values()): #check all combinaison of parameters
            runmetrics={list(confmetrics.keys())[k]:i[k] for k in range(len(confmetrics.keys()))}
            allnull = True
            for metric in runmetrics:
                if runmetrics[metric]!=0:#avoid all null set of parameters
                    allnull = False
            cptcalcul +=1
            if cptcalcul%200 == 0:
                sys.stderr.write(str(cptcalcul)+ "/"+str(nbcalcul)+ " \n")

            if not allnull:

                self.rankPairs(tstart,tend,runmetrics) #compute combinaison
                self.normalizeranksbyintegral(nb_links) #dispach n link using the score computed

                ev = evaluate()

                ev.calculateScoreFromTimeAggreg(self._ranks,trainingtimes)

                if ev._F >= MFscore:
                    MFscore = ev._F
                    initconfmetrics = runmetrics #take the best set
        for metric in initconfmetrics:
            if metric not in self._maxByMetric or self._maxByMetric[metric]==0:
                initconfmetrics[metric]=0
        return initconfmetrics

    def gridsearchPLUS(self,tstart,tend,tmesure,tendtraining,nb_links,trainingtimes,confmetrics,sc1,sc2,sc3):
        MFscore=-1.
        #ready to check various combinaison
        nbcalcul=len(list(itertools.product(*confmetrics.values())))
        cptcalcul = 0
        for i in itertools.product(*confmetrics.values()): #check all combinaison of parameters
            runmetrics={list(confmetrics.keys())[k]:i[k] for k in range(len(confmetrics.keys()))}
            allnull = True
            for metric in runmetrics:
                if runmetrics[metric]!=0:#avoid all null set of parameters
                    allnull = False
            cptcalcul +=1
            if cptcalcul%200 == 0:
                sys.stderr.write(str(cptcalcul)+ "/"+str(nbcalcul)+ " \n")


            if not allnull:

                self.rankPairs(tstart,tend,runmetrics) #compute combinaison
                self.normalizeranksbyintegral(nb_links) #dispach n link using the score computed

                ev = evaluate()

                ev.calculateScoreFromTimeAggreg(self._ranks,trainingtimes)
                # ev.calculateScore(self._ranks,trainingtimes)

                if ev._F >= MFscore:
                    MFscore = ev._F
                    initconfmetrics = runmetrics #take the best set
        for metric in initconfmetrics:
            if metric not in self._maxByMetric or self._maxByMetric[metric]==0:
                initconfmetrics[metric]=0
        return initconfmetrics

    def randomExplo(self,tstart,tend,tmesure,tendtraining,nb_links,trainingtimes,confmetrics,nb_iter):
        MFscore=-1.

        cptcalcul = 0
        for i in range(nb_iter): #check all combinaison of parameters
            runmetrics={metric:random.random()*(confmetrics[metric][1]-confmetrics[metric][0])+confmetrics[metric][0] for metric in confmetrics}
            allnull = True
            for metric in runmetrics:
                if runmetrics[metric]!=0:#avoid all null set of parameters
                    allnull = False
            cptcalcul +=1
            if cptcalcul%200 == 0:
                sys.stderr.write(str(cptcalcul)+ "/"+str(nb_iter)+ " \n")


            if not allnull:

                self.rankPairs(tstart,tend,runmetrics) #compute combinaison
                self.normalizeranksbyintegral(nb_links) #dispach n link using the score computed

                ev = evaluate()

                ev.calculateScoreFromTimeAggreg(self._ranks,trainingtimes)

                if ev._F >= MFscore:
                    MFscore = ev._F
                    initconfmetrics = runmetrics #take the best set

        for metric in initconfmetrics:
            if metric not in self._maxByMetric or self._maxByMetric[metric]==0:
                initconfmetrics[metric]=0
        return initconfmetrics

    def randomExploPLUS(self,tstart,tend,tmesure,tendtraining,nb_links,trainingtimes,confmetrics,nb_iter,sc1,sc2,sc3):
        MFscore=-1.

        cptcalcul = 0
        for i in range(nb_iter): #check all combinaison of parameters
            runmetrics1={metric:random.random()*(confmetrics[metric][1]-confmetrics[metric][0])+confmetrics[metric][0] for metric in confmetrics}
            runmetrics2={metric:random.random()*(confmetrics[metric][1]-confmetrics[metric][0])+confmetrics[metric][0] for metric in confmetrics}
            runmetrics3={metric:random.random()*(confmetrics[metric][1]-confmetrics[metric][0])+confmetrics[metric][0] for metric in confmetrics}
            allnull = True
            for metric in runmetrics1:
                if runmetrics1[metric]!=0:#avoid all null set of parameters
                    allnull = False
            for metric in runmetrics2:
                if runmetrics2[metric]!=0:#avoid all null set of parameters
                    allnull = False
            for metric in runmetrics3:
                if runmetrics3[metric]!=0:#avoid all null set of parameters
                    allnull = False
            cptcalcul +=1
            if cptcalcul%200 == 0:
                sys.stderr.write(str(cptcalcul)+ "/"+str(nb_iter)+ " \n")


            if not allnull:

                sc1.rankPairs(tstart,tend,runmetrics1) #compute combinaison
                sc2.rankPairs(tstart,tend,runmetrics2) #compute combinaison
                sc3.rankPairs(tstart,tend,runmetrics3) #compute combinaison
                Mergeranks=sc1._ranks.copy()
                Mergeranks.update(sc2._ranks)
                Mergeranks.update(sc3._ranks)
                self._ranks=Mergeranks
                self.normalizeranksbyintegral(nb_links) #dispach n link using the score computed

                ev1 = evaluate()
                ev2 = evaluate()
                ev3 = evaluate()
                ev1.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc1._ranks},trainingtimes)
                ev2.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc2._ranks},trainingtimes)
                ev3.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc3._ranks},trainingtimes)
                meanF = meanFscore(ev1._F,ev2._F,ev3._F)

                if meanF >= MFscore:
                    MFscore = meanF
                    initconfmetrics1 = runmetrics1 #take the best set
                    initconfmetrics2 = runmetrics2 #take the best set
                    initconfmetrics3 = runmetrics3 #take the best set

        for metric in initconfmetrics1:
            print(self._maxByMetric)
            if metric not in sc1._maxByMetric or sc1._maxByMetric[metric]==0:
                initconfmetrics1[metric]=0
            if metric not in sc2._maxByMetric or sc2._maxByMetric[metric]==0:
                initconfmetrics2[metric]=0
            if metric not in sc3._maxByMetric or sc3._maxByMetric[metric]==0:
                initconfmetrics3[metric]=0

        return initconfmetrics1,initconfmetrics2,initconfmetrics3

    def gradDescent(self,tstart,tend,tpred,T,nb_links,testtimes,init,derstep,step):
        self.rankPairs(tpred,tpred+T,init) #initate (maybe not needed?)
        n=self.normalizeranksbyintegral(nb_links,tend,tstart)
        ev = evaluate()
        ev.calculateScoreFromTimeAggreg(self._ranks,testtimes)
        # ev.calculateScore(self._ranks,testtimes)

        ev.printeval()
        print(init)
        confmetrics=init.copy()
        derivconfmetrics = init.copy()
        iterconfmetrics = init.copy()
        for i in range(100):
            for metric in confmetrics:

                derivconfmetrics[metric] = confmetrics[metric] + derstep

                self.rankPairs(tpred,tpred+T,derivconfmetrics)
                n=self.normalizeranksbyintegral(nb_links,tend,tstart)
                ev = evaluate()
                ev.calculateScoreFromTimeAggreg(self._ranks,testtimes)

                Fplus=ev._F

                derivconfmetrics[metric]= confmetrics[metric]-derstep
                self.rankPairs(tpred,tpred+T,derivconfmetrics)
                n=self.normalizeranksbyintegral(nb_links,tend,tstart)
                ev = evaluate()
                ev.calculateScoreFromTimeAggreg(self._ranks,testtimes)

                Fminus=ev._F

                iterconfmetrics[metric] = confmetrics[metric] + float(step)*(Fplus-Fminus)/(2*float(derstep))
                derivconfmetrics = confmetrics.copy()

            confmetrics=iterconfmetrics.copy()
            derivconfmetrics = confmetrics.copy()

            self.rankPairs(tpred,tpred+T,confmetrics)
            n=self.normalizeranksbyintegral(nb_links,tend,tstart)
            ev = evaluate()
            ev.calculateScoreFromTimeAggreg(self._ranks,testtimes)

            print(confmetrics)
            print("Test",ev._F)

    def gradDescentLinExp(self,tstart,tend,tmesure,tendtraining,nb_links,trainingtimes,init,derstep,sizelinexptep,numlinexptep,GDMaxstep):
        self.rankPairs(tmesure,tendtraining,init)
        self.normalizeranksbyintegral(nb_links)
        ev = evaluate()
        ev.calculateScoreFromTimeAggreg(self._ranks,trainingtimes)

        confmetrics=init.copy()
        derivconfmetrics = init.copy()
        iterconfmetrics = init.copy()
        directmetrics = dict.fromkeys(init)
        maxindex=-1
        k=0
        maxstep=GDMaxstep

        while maxindex!=0 and k <maxstep: #no change or 100 step
            if k%2 == 0:
                sys.stderr.write(str(k)+ "/"+str(maxstep)+ " \n")
            for metric in confmetrics:
                #compute the gradient
                derivconfmetrics[metric] = confmetrics[metric] + derstep
                self.rankPairs(tmesure,tendtraining,derivconfmetrics)
                self.normalizeranksbyintegral(nb_links)
                ev = evaluate()
                ev.calculateScoreFromTimeAggreg(self._ranks,trainingtimes)

                Fplus=ev._F
                #no negative parameters
                if confmetrics[metric] - derstep >= 0:
                    derivconfmetrics[metric] = confmetrics[metric] - derstep
                else:
                    derivconfmetrics[metric]=0.0
                self.rankPairs(tmesure,tendtraining,derivconfmetrics)
                self.normalizeranksbyintegral(nb_links)
                ev = evaluate()
                ev.calculateScoreFromTimeAggreg(self._ranks,trainingtimes)

                Fminus=ev._F
                #maybe check when parameters<0
                directmetrics[metric] = (Fplus-Fminus)/(float(derstep)+float(min(confmetrics[metric],derstep)))
                derivconfmetrics = confmetrics.copy()
            maxev=evaluate()
            maxev._F=0
            maxindex=0

            for j in range(numlinexptep):
                #a step in the direction
                iterconfmetrics={metric:confmetrics[metric]+(j)*sizelinexptep*directmetrics[metric] for metric in confmetrics}
                for metric in iterconfmetrics:
                    #if iterconfmetrics[metric] > 1:
                    #    iterconfmetrics[metric]=1.0
                    if iterconfmetrics[metric] < 0:
                        iterconfmetrics[metric] = 0.0

                self.rankPairs(tmesure,tendtraining,iterconfmetrics)
                self.normalizeranksbyintegral(nb_links)
                ev = evaluate()
                ev.calculateScoreFromTimeAggreg(self._ranks,trainingtimes)

                if math.floor(ev._F*100000)/100000  > math.floor(maxev._F*100000)/100000 :
                    maxev=ev
                    maxconfmetrics= {metric:iterconfmetrics[metric] for metric in confmetrics}
                    maxindex=j

            # sys.stderr.write(str(maxindex)+" "+str(maxev._F)+" "+str(maxconfmetrics)+" "+str(directmetrics)+"\n")

            confmetrics={metric:maxconfmetrics[metric] for metric in confmetrics}
            derivconfmetrics = confmetrics.copy()


            k=k+1
        maxmetric=0
        for metric in confmetrics:
            if confmetrics[metric] > maxmetric:
                maxmetric=confmetrics[metric]
        for metric in confmetrics:
            confmetrics[metric]=confmetrics[metric]/maxmetric

        self.rankPairs(tmesure,tendtraining,confmetrics)
        self.normalizeranksbyintegral(nb_links)
        if k== maxstep:
            sys.stdout.write("WARNING: Nb max interation\n")
        return confmetrics,maxev


    def gradDescentLinExpPLUS(self,tstart,tend,tmesure,tendtraining,nb_links,trainingtimes,init1,init2,init3,derstep,sizelinexptep,numlinexptep,maxstep,sc1,sc2,sc3):
        sc1.rankPairs(tmesure,tendtraining,init1)
        sc2.rankPairs(tmesure,tendtraining,init2)
        sc2.rankPairs(tmesure,tendtraining,init3)
        Mergeranks=sc1._ranks.copy()
        Mergeranks.update(sc2._ranks)
        Mergeranks.update(sc3._ranks)
        self._ranks=Mergeranks
        self.normalizeranksbyintegral(nb_links)
        ev = evaluate()
        ev.calculateScoreFromTimeAggreg(self._ranks,trainingtimes)

        confmetrics1=init1.copy()
        derivconfmetrics1 = init1.copy()
        iterconfmetrics1 = init1.copy()
        directmetrics1 = dict.fromkeys(init1)

        confmetrics2=init2.copy()
        derivconfmetrics2 = init2.copy()
        iterconfmetrics2 = init2.copy()
        directmetrics2 = dict.fromkeys(init2)

        confmetrics3=init3.copy()
        derivconfmetrics3 = init3.copy()
        iterconfmetrics3 = init3.copy()
        directmetrics3 = dict.fromkeys(init3)

        maxindex=-1
        k=0
        while maxindex!=0 and k <maxstep: #no change or 100 step
            if k%2 == 0:
                sys.stderr.write(str(k)+ "/"+str(maxstep)+ " \n")
            for metric in confmetrics1:
                #compute the gradient
                derivconfmetrics1[metric] = confmetrics1[metric] + derstep
                sc1.rankPairs(tmesure,tendtraining,derivconfmetrics1)
                sc2.rankPairs(tmesure,tendtraining,derivconfmetrics2)
                sc3.rankPairs(tmesure,tendtraining,derivconfmetrics3)
                Mergeranks=sc1._ranks.copy()
                Mergeranks.update(sc2._ranks)
                Mergeranks.update(sc3._ranks)
                self._ranks=Mergeranks
                self.normalizeranksbyintegral(nb_links)
                ev1 = evaluate()
                ev2 = evaluate()
                ev3 = evaluate()
                ev1.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc1._ranks},trainingtimes)
                ev2.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc2._ranks},trainingtimes)
                ev3.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc3._ranks},trainingtimes)
                meanF = meanFscore(ev1._F,ev2._F,ev3._F)
                Fplus=meanF
                #no negative parameters
                if confmetrics1[metric] - derstep >= 0:
                    derivconfmetrics1[metric] = confmetrics1[metric] - derstep
                else:
                    derivconfmetrics1[metric]=0.0

                sc1.rankPairs(tmesure,tendtraining,derivconfmetrics1)
                sc2.rankPairs(tmesure,tendtraining,derivconfmetrics2)
                sc3.rankPairs(tmesure,tendtraining,derivconfmetrics3)
                Mergeranks=sc1._ranks.copy()
                Mergeranks.update(sc2._ranks)
                Mergeranks.update(sc3._ranks)
                self._ranks=Mergeranks
                self.normalizeranksbyintegral(nb_links)
                ev1 = evaluate()
                ev2 = evaluate()
                ev3 = evaluate()
                ev1.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc1._ranks},trainingtimes)
                ev2.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc2._ranks},trainingtimes)
                ev3.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc3._ranks},trainingtimes)
                meanF = meanFscore(ev1._F,ev2._F,ev3._F)
                Fminus=meanF
                #maybe check when parameters<0
                directmetrics1[metric] = (Fplus-Fminus)/(float(derstep)+float(min(confmetrics1[metric],derstep)))
                derivconfmetrics1 = confmetrics1.copy()

            for metric in confmetrics2:
                #compute the gradient
                derivconfmetrics2[metric] = confmetrics2[metric] + derstep
                sc1.rankPairs(tmesure,tendtraining,derivconfmetrics1)
                sc2.rankPairs(tmesure,tendtraining,derivconfmetrics2)
                sc3.rankPairs(tmesure,tendtraining,derivconfmetrics3)
                Mergeranks=sc1._ranks.copy()
                Mergeranks.update(sc2._ranks)
                Mergeranks.update(sc3._ranks)
                self._ranks=Mergeranks
                self.normalizeranksbyintegral(nb_links)
                ev1 = evaluate()
                ev2 = evaluate()
                ev3 = evaluate()
                ev1.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc1._ranks},trainingtimes)
                ev2.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc2._ranks},trainingtimes)
                ev3.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc3._ranks},trainingtimes)
                meanF = meanFscore(ev1._F,ev2._F,ev3._F)
                Fplus=meanF
                #no negative parameters
                if confmetrics2[metric] - derstep >= 0:
                    derivconfmetrics2[metric] = confmetrics2[metric] - derstep
                else:
                    derivconfmetrics2[metric]=0.0

                sc1.rankPairs(tmesure,tendtraining,derivconfmetrics1)
                sc2.rankPairs(tmesure,tendtraining,derivconfmetrics2)
                sc3.rankPairs(tmesure,tendtraining,derivconfmetrics3)
                Mergeranks=sc1._ranks.copy()
                Mergeranks.update(sc2._ranks)
                Mergeranks.update(sc3._ranks)
                self._ranks=Mergeranks
                self.normalizeranksbyintegral(nb_links)
                ev1 = evaluate()
                ev2 = evaluate()
                ev3 = evaluate()
                ev1.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc1._ranks},trainingtimes)
                ev2.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc2._ranks},trainingtimes)
                ev3.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc3._ranks},trainingtimes)
                meanF = meanFscore(ev1._F,ev2._F,ev3._F)
                Fminus=meanF
                #maybe check when parameters<0
                directmetrics2[metric] = (Fplus-Fminus)/(float(derstep)+float(min(confmetrics2[metric],derstep)))
                derivconfmetrics2 = confmetrics2.copy()

            for metric in confmetrics3:
                #compute the gradient
                derivconfmetrics3[metric] = confmetrics3[metric] + derstep
                sc1.rankPairs(tmesure,tendtraining,derivconfmetrics1)
                sc2.rankPairs(tmesure,tendtraining,derivconfmetrics2)
                sc3.rankPairs(tmesure,tendtraining,derivconfmetrics3)
                Mergeranks=sc1._ranks.copy()
                Mergeranks.update(sc2._ranks)
                Mergeranks.update(sc3._ranks)
                self._ranks=Mergeranks
                self.normalizeranksbyintegral(nb_links)
                ev1 = evaluate()
                ev2 = evaluate()
                ev3 = evaluate()
                ev1.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc1._ranks},trainingtimes)
                ev2.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc2._ranks},trainingtimes)
                ev3.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc3._ranks},trainingtimes)
                meanF = meanFscore(ev1._F,ev2._F,ev3._F)
                Fplus=meanF
                #no negative parameters
                if confmetrics3[metric] - derstep >= 0:
                    derivconfmetrics3[metric] = confmetrics3[metric] - derstep
                else:
                    derivconfmetrics3[metric]=0.0

                sc1.rankPairs(tmesure,tendtraining,derivconfmetrics1)
                sc2.rankPairs(tmesure,tendtraining,derivconfmetrics2)
                sc3.rankPairs(tmesure,tendtraining,derivconfmetrics3)
                Mergeranks=sc1._ranks.copy()
                Mergeranks.update(sc2._ranks)
                Mergeranks.update(sc3._ranks)
                self._ranks=Mergeranks
                self.normalizeranksbyintegral(nb_links)
                ev1 = evaluate()
                ev2 = evaluate()
                ev3 = evaluate()
                ev1.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc1._ranks},trainingtimes)
                ev2.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc2._ranks},trainingtimes)
                ev3.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc3._ranks},trainingtimes)
                meanF = meanFscore(ev1._F,ev2._F,ev3._F)
                Fminus=meanF
                #maybe check when parameters<0
                directmetrics3[metric] = (Fplus-Fminus)/(float(derstep)+float(min(confmetrics3[metric],derstep)))
                derivconfmetrics3 = confmetrics3.copy()


            maxev=evaluate()
            maxev._F=0
            maxindex=0
            for j in range(numlinexptep):
                #a step in the direction
                iterconfmetrics1={metric:confmetrics1[metric]+(j)*sizelinexptep*directmetrics1[metric] for metric in confmetrics1}
                iterconfmetrics2={metric:confmetrics2[metric]+(j)*sizelinexptep*directmetrics2[metric] for metric in confmetrics2}
                iterconfmetrics3={metric:confmetrics3[metric]+(j)*sizelinexptep*directmetrics3[metric] for metric in confmetrics3}

                for metric in iterconfmetrics1:
                    #if iterconfmetrics[metric] > 1:
                    #    iterconfmetrics[metric]=1.0
                    if iterconfmetrics1[metric] < 0:
                        iterconfmetrics1[metric] = 0.0
                    if iterconfmetrics2[metric] < 0:
                        iterconfmetrics2[metric] = 0.0
                    if iterconfmetrics3[metric] < 0:
                        iterconfmetrics3[metric] = 0.0
                sc1.rankPairs(tmesure,tendtraining,iterconfmetrics1)
                sc2.rankPairs(tmesure,tendtraining,iterconfmetrics2)
                sc3.rankPairs(tmesure,tendtraining,iterconfmetrics3)
                Mergeranks=sc1._ranks.copy()
                Mergeranks.update(sc2._ranks)
                Mergeranks.update(sc3._ranks)
                self._ranks=Mergeranks
                self.normalizeranksbyintegral(nb_links)
                ev1 = evaluate()
                ev2 = evaluate()
                ev3 = evaluate()
                ev1.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc1._ranks},trainingtimes)
                ev2.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc2._ranks},trainingtimes)
                ev3.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc3._ranks},trainingtimes)
                meanF = meanFscore(ev1._F,ev2._F,ev3._F)
                if math.floor(meanF*100000)/100000  > math.floor(maxev._F*100000)/100000:
                    maxev=ev
                    maxconfmetrics1= {metric:iterconfmetrics1[metric] for metric in confmetrics1}
                    maxconfmetrics2= {metric:iterconfmetrics2[metric] for metric in confmetrics2}
                    maxconfmetrics3= {metric:iterconfmetrics3[metric] for metric in confmetrics3}
                    maxindex=j
                    ev1 = evaluate()
                    ev2 = evaluate()
                    ev3 = evaluate()
                    ev1.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc1._ranks},trainingtimes)
                    ev2.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc2._ranks},trainingtimes)
                    ev3.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in sc3._ranks},trainingtimes)
                    maxev1 = ev1
                    maxev2 = ev2
                    maxev3 = ev3
                # sys.stderr.write(str(maxindex)+"\n")

            confmetrics1={metric:maxconfmetrics1[metric] for metric in confmetrics1}
            derivconfmetrics1 = confmetrics1.copy()
            confmetrics2={metric:maxconfmetrics2[metric] for metric in confmetrics2}
            derivconfmetrics2 = confmetrics2.copy()
            confmetrics3={metric:maxconfmetrics3[metric] for metric in confmetrics3}
            derivconfmetrics3 = confmetrics3.copy()
            k=k+1
        maxmetric=0
        for metric in confmetrics1:
            if confmetrics1[metric] > maxmetric:
                maxmetric=confmetrics1[metric]
            if confmetrics2[metric] > maxmetric:
                maxmetric=confmetrics2[metric]
            if confmetrics3[metric] > maxmetric:
                maxmetric=confmetrics3[metric]
        for metric in confmetrics1:
            confmetrics1[metric]=confmetrics1[metric]/maxmetric
            confmetrics2[metric]=confmetrics2[metric]/maxmetric
            confmetrics3[metric]=confmetrics3[metric]/maxmetric

        sc1.rankPairs(tmesure,tendtraining,confmetrics1)
        sc2.rankPairs(tmesure,tendtraining,confmetrics2)
        sc3.rankPairs(tmesure,tendtraining,confmetrics3)
        Mergeranks=sc1._ranks.copy()
        Mergeranks.update(sc2._ranks)
        Mergeranks.update(sc3._ranks)
        self._ranks=Mergeranks
        self.normalizeranksbyintegral(nb_links)
        for link in self._ranks:
        	if link in sc1._pair_set:
        		sc1._ranks[link] = self._ranks[link]
        	elif link in sc2._pair_set:
        		sc2._ranks[link] = self._ranks[link]
        	elif link in sc3._pair_set:
        		sc3._ranks[link] = self._ranks[link]

        if k== maxstep:
            sys.stdout.write("WARNING: Nb max interation\n")
        return confmetrics1,confmetrics2,confmetrics3,maxev,maxev1,maxev2,maxev3





    def traceScorehistogram(self,N):
        data=[]
        count=0
        for c in self._ranks:
            if self._ranks[c] !=0:
                data.append(self._ranks[c])
                count+=1
        n, bins, patches= plt.hist(data,50)
        #print count
        plt.show()

    def traceActivityhistogram(self,N,times):
        data=[]
        count=0
        for link in times:
            if times[link] !=0:
                data.append(len(times[link]))
                count+=1
        n, bins, patches= plt.hist(data,50)
        #print count
        plt.show()





    def printScore(self):
        for c in self._pair_set:
            sys.stdout.write(str(c)+" "+str(self._pair[c])+"\n")

    def traceScore(self,c,tm):

        t = np.arange(0,self._T,self._T/self._N)

        fctstr=self.rankMakeFunction(c)
        #fct=lambda t:eval(fctstr)
        def f(t):
            return eval(fctstr)-1

        #print t
        #print fctstr
        plt.plot(t, f(t))


        plt.axis([0, 10,0, 5])
        plt.show()

    def correlationMatrix(self,confmetrics):
        #une ligne une metrique
        value = []
        label=[]
        i=0
        for ID in confmetrics:
            label.append(ID)
            value.append([])
            for c in self._pair:
                if ID not in self._pair[c]:
                    value[i].append(0)
                else:
                    value[i].append(self._pair[c][ID])
            i=i+1

        corrMatrix = np.corrcoef(np.array(value))
        print(corrMatrix)
        # plt.subplot(211)
        plt.imshow(corrMatrix, cmap="hot_r", interpolation='nearest',vmin=0, vmax=1)
        # plt.subplot(212)
        # plt.imshow(np.random.random((100, 100)), cmap='hot')

        plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
        cax = plt.axes([0.85, 0.1, 0.075, 0.8])
        plt.colorbar(cax=cax)
        plt.show()

        # ax = plt.imshow(corrMatrix, cmap='hot', interpolation='nearest')
        # plt.show()


    def OnePred(self,tstart,tend,tmesure,tendtraining,nb_links,obstimes,trainingtimes,confmetrics):
        # print(confmetrics)
        runmetrics= {metric:confmetrics[metric][0] for metric in confmetrics}
        # print(runmetrics)
        self.rankPairs(tstart,tend,runmetrics) #compute combinaison
        self.normalizeranksbyintegral(nb_links) #dispach n link using the score computed

        sys.stdout.write("All\n")
        ev = evaluate()
        ev.calculateScoreFromTimeAggreg(self._ranks,trainingtimes)
        ev.printeval()

        sys.stdout.write("New\n")
        evnewlink = evaluate()
        evnewlink.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in self._ranks if x not in obstimes},trainingtimes)
        evnewlink.printeval()

        sys.stdout.write("Recurent\n")
        evrecurent = evaluate()
        evrecurent.calculateScoreFromTimeAggreg({x:self._ranks[x] for x in self._ranks if x in obstimes},trainingtimes)
        evrecurent.printeval()
        sys.exit()

    def extractMetric(self,confmetrics,filename):
        #une ligne une metrique

        metrictable = open(filename, 'w')
        metrictable.write("u ")
        metrictable.write("v ")

        for ID in confmetrics:
            metrictable.write(ID + " ")
        metrictable.write("\n")

        for c in self._pair:
            for u in c:
                metrictable.write(str(u) + " ")
            for ID in confmetrics:
                if ID not in self._pair[c]:
                    metrictable.write("0.0" + " ")
                else:
                    metrictable.write(str(self._pair[c][ID])+" ")
            metrictable.write("\n")

        metrictable.close()

    @staticmethod
    def extractCoef(init0,init1,init2,init3,filename):
        #une ligne une metrique

        table = open(filename, 'w')
        table.write("Class ")
        s=""
        for ID in init0:
            s+=ID + " "
        table.write(s[:-1]+"\n")

        s=""
        table.write("C0 ")
        for ID in init0:
            s+=str(init0[ID]) + " "
        table.write(s[:-1]+"\n")

        s=""
        table.write("C1 ")
        for ID in init0:
            s+=str(init1[ID]) + " "
        table.write(s[:-1]+"\n")

        s=""
        table.write("C2 ")
        for ID in init0:
            s+=str(init2[ID]) + " "
        table.write(s[:-1]+"\n")

        s=""
        table.write("C3 ")
        for ID in init0:
            s+=str(init3[ID]) + " "
        table.write(s[:-1]+"\n")
        table.close()

    def extractPrediction(self,filename):
        #une ligne une metrique

        table = open(filename, 'w')
        for c in self._ranks:
            for u in c:
                table.write(str(u) + " ")
            table.write(str(self._ranks[c]))
            table.write("\n")
        table.close()

    @staticmethod
    def extractTime(times,filename):
        #une ligne une metrique

        table = open(filename, 'w')
        for c in times:
            for u in c:
                table.write(str(u) + " ")
            s=""
            for t in times[c]:
                s=s+str(t)+","
            table.write(s[:-1]+"\n")
        table.close()













def meanFscore(x,y,z):
    if x==0 or y==0 or z==0:
        return 0
    else:
        return (3)/(1/x+1/y+1/z)
