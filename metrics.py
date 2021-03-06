import numpy as np
from scipy.optimize import curve_fit
import sys
import math
import bisect
import matplotlib as mpl
import matplotlib.pyplot as plt
class metrics:
    def __init__(self):
        self._confmetrics = dict()
        self._TP = 0


    def computeMetrics(self,sc,tstart,tend,times,nodes):
        # Add the metric function for each pairs in score
        # score, observation start time, observation end time, dict with the time of links for each pairs, dict with the neighbors of each nodes
        for metricsname in self._confmetrics: #launch each metrics in confmetrics

            if metricsname == "PairActivityExtrapolation":
                for link in sc._pair:
                    u,v=link
                    if link in times:
                        sc.addFunction(link,"PairActivityExtrapolation",self.PairActivityExtrapolation(times[link]))

            elif metricsname[:32] == "PairActivityExtrapolationNbLinks":
                n=int(metricsname[32:])
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link]) > n:
                        sc.addFunction(link,metricsname,self.PairActivityExtrapolationNbLinks(times[link],tend,n))
                    elif len(times[link]) > 1:
                        sc.addFunction(link,metricsname,self.PairActivityExtrapolationNbLinks(times[link],tend,len(times[link])))

            elif metricsname[:34] == "PairActivityExtrapolationTimeInter":
                n=float(metricsname[34:])
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link]) > 0:
                        sc.addFunction(link,metricsname,self.PairActivityExtrapolationTimeInter(times[link],tend,n))

            elif metricsname== "twopointExtrapolation":
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link]) > 0:
                        sc.addFunction(link,metricsname,self.twopointExtrapolation(times[link],tstart,tend))

            elif metricsname[:22]== "fitnPointExtrapolation":
                n=int(metricsname[22:])
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link]) > 0:
                        sc.addFunction(link,metricsname,self.fitnPointExtrapolation(times[link],tstart,tend,n))

            elif metricsname == "intercontactTimes":
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link])>1:
                        sc.addFunction(link,"intercontactTimes",self.intercontactTimes(times[link]))

            elif metricsname[:22] == "intercontactTimesRedux":
                n=int(metricsname[22:])
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link])>n:
                        sc.addFunction(link,metricsname,self.intercontactTimesRedux(times[link],n))
                    elif len(times[link])>1:
                        sc.addFunction(link,metricsname,self.intercontactTimes(times[link]))


            elif metricsname == "commonNeighbors":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"commonNeighbors",self.commonNeighbors(nodes[u],nodes[v]))

            elif metricsname[:23] == "exponentialInterContact":
                n=int(metricsname[23:])
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link])>n:
                        sc.addFunction(link,metricsname,self.exponentialInterContact(times[link],n))
                    elif len(times[link])>2:
                        sc.addFunction(link,metricsname,self.exponentialInterContact(times[link],2))

            elif metricsname == "exponentialLast":
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    sc.addFunction(link,"exponentialLast",self.exponentialLast(times[link],tend))

            elif metricsname == "jaccardIndex":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"jaccardIndex",self.jaccardIndex(nodes[u],nodes[v]))

            elif metricsname == "weightedCommonNeighbors":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"weightedCommonNeighbors",self.weightedCommonNeighbors(u,v,times,nodes[u],nodes[v]))


            elif metricsname == "resourceAlloc":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"resourceAlloc",self.resourceAlloc(u,v,nodes))

            elif metricsname == "weightedResourceAlloc":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"weightedResourceAlloc",self.weightedResourceAlloc(u,v,times,nodes))

            elif metricsname == "adamicAdar":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"adamicAdar",self.adamicAdar(u,v,nodes))

            elif metricsname == "weightedAdamicAdar":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"weightedAdamicAdar",self.weightedAdamicAdar(u,v,times,nodes))

            elif metricsname == "sorensenIndex":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"sorensenIndex",self.sorensenIndex(u,v,nodes))

            elif metricsname == "weightedSorensenIndex":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"weightedSorensenIndex",self.weightedSorensenIndex(u,v,times,nodes))



            else:
                sys.stderr.write("-- WARNING: metric Not Found: "+ metricsname+"--\n" )



    def PairActivityExtrapolation(self,time):
        s = len(time)
        return lambda t: s

    def PairActivityExtrapolationNbLinks(self,time,t,n):
        #n= number of link
        s = len(time[-n:])/(float(t-time[-n]))

        return lambda t: s

    def PairActivityExtrapolationTimeInter(self,time,t,n):
        # counts the links betwenn n and t

        nlinks=len([x for x in time if x>t-n and x<=t])

        return lambda t: nlinks/n

    def intercontactTimes(self,time):
        #Obsolete
        itc = np.array([j - i for i,j in zip(time[:-1], time[1:])])
        last=time[-1]
        mean = np.mean(itc)
        var = np.var(itc)
        #THATS UGLY:
        var=var+0.1
        return lambda t: np.exp(-pow((t-last-mean/2)%(mean)-mean/2,2)/(2*pow(var,2)))/(var*math.sqrt(2*math.pi))

    def intercontactTimesRedux(self,time,n):
        #Obsolete

        itc = np.array([j - i for i,j in zip(time[-n:-1], time[-n+1:])])
        last=time[-1]
        mean = np.mean(itc)
        var = np.var(itc)
        #THATS UGLY:
        var=var+0.1
        return lambda t: np.exp(-pow((t-last-mean/2)%(mean)-mean/2,2)/(2*pow(var,2)))/(var*math.sqrt(2*math.pi))

    def exponentialInterContact(self,time,n):
        #Obsolete

        itc = np.array([j - i for i,j in zip(time[-n:-1], time[-n+1:])])
        last=time[-1]
        mean = np.mean(itc)
        return lambda t: np.exp(-mean)

    def exponentialLast(self,time,t):
        #Obsolete

        last=float(time[-1])
        return lambda t: np.exp(-(t-last))

    def commonNeighbors(self,nodes_u,nodes_v):
        return lambda t: float(len(nodes_u.intersection(nodes_v))) #modif!

    def jaccardIndex(self,nodes_u,nodes_v):
        return lambda t: float(len(nodes_u.intersection(nodes_v)))/len(nodes_u.union(nodes_v)) #modif!



    def weightedCommonNeighbors(self,u,v,times,nodes_u,nodes_v):
        s=0.
        for k in nodes_u.intersection(nodes_v):
            s+=float(len(times[frozenset([u,k])])*len(times[frozenset([v,k])]))
        return lambda t:s

    def resourceAlloc(self,u,v,nodes):
        s=0.
        for k in nodes[u].intersection(nodes[v]):
            s+=1/float(len(nodes[k]))
        return lambda t:s
    def weightedResourceAlloc(self,u,v,times,nodes):
        s=0.
        for k in nodes[u].intersection(nodes[v]):
            W=0
            for j in nodes[k]:
                W += len(times[frozenset([j,k])])
            s+=1/float(W)
        return lambda t:s

    def adamicAdar(self,u,v,nodes):
        s=0.
        for k in nodes[u].intersection(nodes[v]):
            s+=1/math.log(len(nodes[k]))
        return lambda t:s

    def weightedAdamicAdar(self,u,v,times,nodes):
        s=0.
        for k in nodes[u].intersection(nodes[v]):
            W=0
            for j in nodes[k]:
                W += len(times[frozenset([j,k])])
            s+=1/math.log(W)
        return lambda t:s


    def sorensenIndex(self,u,v,nodes):
        return  lambda t:2.0*len(nodes[u].intersection(nodes[v]))/(len(nodes[v])+len(nodes[u]))


    def weightedSorensenIndex(self,u,v,times,nodes):
        s=0.
        Wu,Wv=0,0
        for j in nodes[u]:
            Wu+=float(len(times[frozenset([j,u])]))

        for i in nodes[v]:
            Wv+=float(len(times[frozenset([i,v])]))

        for k in nodes[u].intersection(nodes[v]):
            s+= float(len(times[frozenset([u,k])])+len(times[frozenset([v,k])]))
        return lambda t:s/(Wu+Wv)

    def twopointExtrapolation(self,time,tstart,tend):
        #Extrapolate the activity of the pair of node using the mean of the activity of each halves of the obsevation period
        tmid=(tstart+tend)/2
        nb_links1=len([x for x in time if x>tstart and x<=tmid])
        nb_links2=len([x for x in time if x>tmid and x<=tend])
        a=2*(nb_links2/(tend-tmid)-nb_links1/(tmid-tstart))/(tend-tstart)
        b=(nb_links1/(tmid-tstart)*(tmid+tend)-nb_links2/(tend-tmid)*(tstart+tmid))/(tend-tstart)
        return lambda t: max(0,a*t+b)

    def fitnPointExtrapolation(self,time,tstart,tendobs,n):
        #Extrapolate the activity of the pair of node using the mean of the activity of n parts of the observation period

        xedges=list(range(int(tstart),int(tendobs),int((tendobs-tstart)/n)))
        data=[0]*(len(xedges))
        for i in range(len(xedges)):

            data[i]=len([x for x in time if x>xedges[i] and x<=xedges[i]+(tendobs-tstart)/n])
            data[i]=data[i]/((tendobs-tstart)/n)
        popt, pcov = curve_fit(funcdroite,xedges, data)
        a,b=popt

        return lambda t: max(0,a*t+b)




#ACTIVITY EXTRAPOLATION:
    #same ACTIVITY
    def linearActivityExtrapolation(self,nb_lines,tstart,tmesure,tstartpred,tendpred):
        return float(nb_lines)*(tendpred-tstartpred)/float(tmesure-tstart)

    #extrapolate ACTIVITY with obs and training
    def twopointrActivityExtrapolation(self,nb_linksOBS,nb_linksTRAINING,tstart,tmesure,tendtraining,tstartpred,tendpred):
        a=2*(nb_linksTRAINING/(tendtraining-tmesure)-nb_linksOBS/(tmesure-tstart))/(tendtraining-tstart)
        b=(nb_linksOBS/(tmesure-tstart)*(tmesure+tendtraining)-nb_linksTRAINING/(tendtraining-tmesure)*(tstart+tmesure))/(tendtraining-tstart)
        return (a*(tstartpred+tendpred)/2+b)*(tendpred-tstartpred)

    def fitnPointrActivityExtrapolation(self,times,tstart,tendobs,tstartpred,tendpred,n):

        xedges=list(range(int(tstart),int(tendobs),int((tendobs-tstart)/n)))
        data=[0]*(len(xedges))
        for i in range(len(xedges)):

            for link in times:
                 data[i]=data[i]+len([x for x in times[link] if x>xedges[i] and x<=xedges[i]+(tendobs-tstart)/n])
            data[i]=data[i]/((tendobs-tstart)/n)
        popt, pcov = curve_fit(funcdroite,xedges, data)
        a,b=popt

        return (a*(tstartpred+tendpred)/2+b)*(tendpred-tstartpred)





























def funcdroite(t,A,B):
    g=A * t+B
    return g
