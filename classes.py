from scoring import score
import itertools
from evaluation import evaluate
from metrics import metrics
from operator import itemgetter
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import scipy.spatial.distance
import numpy as np
import math
import sys
import victor_purpura
import statistics
import operator
class classes:

    def __init__(self):
        self._classorder = list()
        self._classscore = dict()
        self._classUnion = score()
        self._threshold= None
        self._linkage = []
        self._label=[]
        self._VandPparameter= None
        self._nbcluster =None
        self._cuttree =None




    def classbythreshold(self,obstimes,obsnodes):

        #Class Making
        #3 Class : C1 = New link C2 = less than classthreshold link C3 more than classthreshold
        self._classorder = ["C1","C2","C3"]

        self._classscore["C1"] = score()
        self._classscore["C2"] = score()
        self._classscore["C3"] = score()

        # print(self._classthreshold)
        for u,v in itertools.combinations(obsnodes.keys(),2): #to predict new pair of nodes and initialize the classes
        	link = frozenset([u,v])
        	self._classUnion.addPair(link)
        	if link not in obstimes:
        		self._classscore["C1"].addPair(link)
        	elif len(obstimes[link]) < self._classthreshold:
        		self._classscore["C2"].addPair(link)
        	else:
        		self._classscore["C3"].addPair(link)


    def getnblinksTraining(self,trainingtimes):
        #Compute the number of link in the prediction period of the training phase
        nb_linksTRAINING =dict()
        for classID in self._classorder:
            nb_linksTRAINING[classID]=0

        for link in trainingtimes:
            for classID in self._classorder:
                if link in self._classscore[classID]._pair_set:
        		          nb_linksTRAINING[classID] += len(trainingtimes[link])

        return nb_linksTRAINING


    def classbyUPGMA(self,obstimes,trainingtimes,obsnodes):
        self._classorder=["C1"]
        self._classscore["C1"] = score()

        for u,v in itertools.combinations(obsnodes.keys(),2): #to predict new pair of nodes and initialize the classes
        	link = frozenset([u,v])
        	self._classUnion.addPair(link)
        	if link not in obstimes:
        		self._classscore["C1"].addPair(link)
        learningperiods=dict()
        for link in obstimes:
            if link in trainingtimes:
                learningperiods[link] = obstimes[link]+trainingtimes[link]
            else:
                learningperiods[link] = obstimes[link]
        Y,self._label=classes.Makedistmatx(learningperiods,self._VandPparameter,0,0)
        self._linkage=hierarchy.average(Y)
        cutree = hierarchy.cut_tree(self._linkage,self._nbcluster)


        for i in range(self._nbcluster):
            self._classscore["C"+str(i+2)] = score()
            self._classorder.append("C"+str(i+2))

        for i in range(len(self._label)):
            u=self._label[i]
            self._classscore["C"+str(cutree[i][0]+2)].addPair(u)
            # for t in times[u]:
                # hists[cutree[i]].append(t)

    def classbyUPGMASIZE(self,obstimes,trainingtimes,obsnodes):
        self._classorder=["C1"]
        self._classscore["C1"] = score()

        for u,v in itertools.combinations(obsnodes.keys(),2): #to predict new pair of nodes and initialize the classes
        	link = frozenset([u,v])
        	self._classUnion.addPair(link)
        	if link not in obstimes:
        		self._classscore["C1"].addPair(link)
        learningperiods=dict()
        for link in obstimes:
            if link in trainingtimes:
                learningperiods[link] = obstimes[link]+trainingtimes[link]
            else:
                learningperiods[link] = obstimes[link]
        Y,self._label=classes.Makedistmatx(learningperiods,self._VandPparameter,0,0)
        self._linkage=hierarchy.average(Y)


        n=len(self._label)

        # print(self._label)
        q=[]
        q.append(self._linkage[-1,0])
        q.append(self._linkage[-1,1])
        q.sort()
        for i in range(self._nbcluster-2):
            X=q.pop( q.index(max(q,key=lambda x: self._linkage[int(x-n),3])))
            q.append(self._linkage[int(X-n),0])
            q.append(self._linkage[int(X-n),1])
            q.sort()

        q.sort(key=lambda x: self._linkage[int(x-n),3],reverse=True)
        self._cuttree=   [-1] * n
        for i in range(self._nbcluster):
            self.getLeafID(q[i],i)

        # cutree = hierarchy.cut_tree(self._linkage,self._nbcluster)
        # print(cutree)

        for i in range(self._nbcluster):
            self._classscore["C"+str(i+2)] = score()
            self._classorder.append("C"+str(i+2))

        for i in range(len(self._label)):
            u=self._label[i]
            self._classscore["C"+str(self._cuttree[i]+2)].addPair(u)
            # for t in times[u]:
                # hists[cutree[i]].append(t)

    def getLeafID(self,cluster,startingcluster):
        n = len(self._label)
        if self._linkage[int(cluster-n),0] >= n:
            self.getLeafID(self._linkage[int(cluster-n),0],startingcluster)
        else:
            self._cuttree[int(self._linkage[int(cluster-n),0])]=startingcluster

        if self._linkage[int(cluster-n),1] >= n:
            self.getLeafID(self._linkage[int(cluster-n),1],startingcluster)
        else:
            self._cuttree[int(self._linkage[int(cluster-n),1])]=startingcluster

    def MatchclassbyUPGMA(self,obstimes,obsnodes,obstimesT,tstartobs,tendobs,tstartobsT,tendobsT):
        # self._classorder=["C1"]
        # self._classscore["C1"] = score()
        n=len(self._label)
        q=[]
        q.append(self._linkage[-1,0])
        q.append(self._linkage[-1,1])
        q.sort()
        for i in range(self._nbcluster-2):
            X=q.pop()
            q.append(self._linkage[int(X-n),0])
            q.append(self._linkage[int(X-n),1])
            q.sort()

        q.sort(key=lambda x: self._linkage[int(x-n),3])


        for u,v in itertools.combinations(obsnodes.keys(),2): #to predict new pair of nodes and initialize the classes
            link = frozenset([u,v])
            self._classUnion.addPair(link)
            if link not in obstimes:
                self._classscore["C1"].addPair(link)
            else:
                mindist=math.inf
                cluster = None
                for i in range(self._nbcluster):
                    dist = self.recursivdistance(q[i],link,obstimes,obstimesT,tstartobs,tendobs,tstartobsT,tendobsT)
                    if dist < mindist:
                        mindist=dist
                        cluster = i
                # print(self._linkage[int(q[cluster]-n)],self._nbcluster-cluster+1)

                self._classscore["C"+str(self._nbcluster-cluster+1)].addPair(link)


    def MatchclassbyUPGMASIZE(self,obstimes,obsnodes,obstimesT,tstartobs,tendobs,tstartobsT,tendobsT):
        # self._classorder=["C1"]
        # self._classscore["C1"] = score()
        n=len(self._label)
        q=[]
        q.append(self._linkage[-1,0])
        q.append(self._linkage[-1,1])
        q.sort()
        for i in range(self._nbcluster-2):
            X=q.pop( q.index(max(q,key=lambda x: self._linkage[int(x-n),3])))
            q.append(self._linkage[int(X-n),0])
            q.append(self._linkage[int(X-n),1])
            q.sort()

        q.sort(key=lambda x: self._linkage[int(x-n),3])


        for u,v in itertools.combinations(obsnodes.keys(),2): #to predict new pair of nodes and initialize the classes
            link = frozenset([u,v])
            self._classUnion.addPair(link)
            if link not in obstimes:
                self._classscore["C1"].addPair(link)
            else:
                mindist=math.inf
                cluster = None
                for i in range(self._nbcluster):
                    dist = self.recursivdistance(q[i],link,obstimes,obstimesT,tstartobs,tendobs,tstartobsT,tendobsT)
                    if dist < mindist:
                        mindist=dist
                        cluster = i
                # print(self._linkage[int(q[cluster]-n)],self._nbcluster-cluster+1)

                self._classscore["C"+str(self._nbcluster-cluster+1)].addPair(link)

    def recursivdistance(self,cluster,X,obstimes,obstimesT,tstartobs,tendobs,tstartobsT,tendobsT):
        n = len(self._label)
        if cluster >= n:
            if self._linkage[int(cluster-n),0] >= n :
                d0=self._linkage[int(self._linkage[int(cluster-n),0]-n),3]
            else:
                d0=1

            if self._linkage[int(cluster-n),1] >= n :
                d1=self._linkage[int(self._linkage[int(cluster-n),1]-n),3]
            else:
                d1=1

            return (d0 * self.recursivdistance(self._linkage[int(cluster-n),0],X,obstimes,obstimesT,tstartobs,tendobs,tstartobsT,tendobsT) + d1 * self.recursivdistance(self._linkage[int(cluster-n),1],X,obstimes,obstimesT,tstartobs,tendobs,tstartobsT,tendobsT) ) / self._linkage[int(cluster-n),3]
        else:
            timescluster=[t+(tendobs-tendobsT) for t in obstimesT[self._label[int(cluster)]]]
            return victor_purpura.distance(timescluster,obstimes[X],self._VandPparameter)





    def computeMetrics(self,metrics,tstartobsT,tendobsT,tstartpredT,tendpredT,obstimes,obsnodes):

        for sc in self._classorder:
            metrics.computeMetrics(self._classscore[sc],tstartobsT,tendobsT,obstimes,obsnodes) #compute all metrics
            self._classscore[sc].integrateMetrics(tstartpredT,tendpredT) #integrate metrics
            self._classscore[sc].setMaxByMetric()
            self._classscore[sc].normalizeMetrics()

        metrics.computeMetrics(self._classUnion,tstartobsT,tendobsT,obstimes,obsnodes) #compute all metrics
        self._classUnion.integrateMetrics(tstartpredT,tendpredT) #integrate metrics
        self._classUnion.setMaxByMetric()
        self._classUnion.normalizeMetrics()


    def resetclasslists(self):
        for classID in self._classorder:
            self._classscore[classID].resetPairs()
            self._classscore[classID].resetRanks()
        self._classUnion.resetPairs()
        self._classUnion.resetRanks()

    @staticmethod
    def computedist(time1,time2,bins,tstart,tend):
        densit=False
        hist1,bins = np.histogram(time1, bins=bins, range=(tstart,tend), density=densit)
        hist2,bins = np.histogram(time2, bins=bins, range=(tstart,tend), density=densit)
        dif=np.subtract(hist1, hist2 )
        # print(len(dif))
        squared = list(map(lambda x: x**2, dif))
        d= list(map(lambda x: math.sqrt(x), squared))
        # for t in range(tstart,tend,bins):
            # len([t1 for t1 in time1 if t< t1 and t1< t+bins ])
        return sum(d)

    @staticmethod
    def Makedistmatx(times,bins,tstart,tend):
        D=[]
        label=[]

        for pair1,pair2 in itertools.combinations(times.keys(),2): #to predict new pair of nodes
            # D.append(computedist(times[pair1],times[pair2],bins,tstart,tend))
            D.append(victor_purpura.distance(times[pair1],times[pair2],bins))

            s=""
            for u in pair1:
                s+=str(int(u))+" "

            for u in pair2:
                s+=str(int(u))+" "
            # print(pa<ir1,pair2)
            if len(label)==0 or label[-1] is not pair1:
                label.append(pair1)
        label.append(pair2)
        return D,label

    @staticmethod
    def dist(time1,time2):
        # print(timeu)
        d=math.sqrt((time1[0]-time2[0])**2)
        return d


























#
